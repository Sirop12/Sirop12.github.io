from flask import Flask, render_template, request, jsonify
from pydnevnikruapi.dnevnik.exceptions import DiaryError
from urllib.parse import urlparse, parse_qs, urlencode
import requests
import logging
from werkzeug.exceptions import BadRequest, InternalServerError

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="templates", static_folder="static")

LOGIN_URL = "https://login.dnevnik.ru/login/"
RETURN_URL = (
    "https://login.dnevnik.ru/oauth2?response_type=token"
    "&client_id=bb97b3e445a340b9b9cab4b9ea0dbd6f"
    "&scope=CommonInfo,ContactInfo,FriendsAndRelatives,EducationalInfo"
    "&redirect_uri=https://androsovpavel.pythonanywhere.com/callback"
)

def get_token_from_url(url: str) -> str:
    """Извлекает токен из URL, включая фрагмент."""
    try:
        logger.info(f"Полученный URL: {url}")
        # Разделяем URL на базовую часть и фрагмент
        if "#" in url:
            base_url, fragment = url.split("#", 1)
        else:
            base_url, fragment = url, ""

        parsed_url = urlparse(base_url)
        query = parse_qs(parsed_url.query)
        result = query.get("result")
        is_granted = query.get("is_granted", ["True"])[0].lower() == "true"

        if result is not None and result[0] != "success":
            logger.error(f"Некорректный result: {result}")
            raise DiaryError("Что-то не так с авторизацией")

        if not is_granted:
            logger.warning("Доступ не предоставлен (is_granted=False)")

        # Извлекаем токен из фрагмента
        token = ""
        if "access_token=" in fragment:
            token = fragment.split("access_token=")[1].split("&")[0]

        if not token:
            logger.error("Токен не найден в URL или фрагменте")
            raise DiaryError("Токен не найден в URL")

        logger.info(f"Извлечённый токен: {token}")
        return token
    except Exception as e:
        logger.error(f"Ошибка извлечения токена: {e}")
        raise DiaryError(f"Ошибка обработки URL: {str(e)}")

@app.route("/", methods=["GET"])
def get_form():
    """Отображает главную страницу."""
    return render_template("index.html")

@app.route("/callback", methods=["GET"])
def callback():
    """Обрабатывает редирект от login.dnevnik.ru."""
    return render_template("callback.html")

@app.route("/get-token", methods=["POST"])
def fetch_token():
    """Обрабатывает URL от клиента и возвращает токен."""
    try:
        data = request.get_json()
        url = data.get("url") if data else None
        if not url:
            raise DiaryError("URL не предоставлен")

        token = get_token_from_url(url)
        return render_template("result.html", token=token)
    except DiaryError as e:
        raise BadRequest(str(e))
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        raise InternalServerError("Внутренняя ошибка сервера")

@app.route("/proxy", methods=["POST"])
def proxy_request():
    """Проксирует запрос к login.dnevnik.ru, чтобы обойти CORS."""
    try:
        data = request.get_json()
        login_url = data.get("loginUrl") if data else None
        return_url = data.get("returnUrl") if data else None
        if not login_url or not return_url:
            raise DiaryError("Некорректные параметры запроса")

        response = requests.get(
            login_url,
            params={"ReturnUrl": return_url},
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
        )

        if response.status_code != 200:
            logger.error(f"Статус ответа: {response.status_code}")
            raise DiaryError("Сайт недоступен или ведутся технические работы")

        url = str(response.url)
        logger.info(f"Ответный URL: {url}")
        return jsonify({"url": url})
    except DiaryError as e:
        raise BadRequest(str(e))
    except Exception as e:
        logger.error(f"Ошибка проксирования: {e}")
        raise InternalServerError("Внутренняя ошибка сервера")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
