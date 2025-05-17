from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydnevnikruapi.dnevnik.exceptions import DiaryError
from urllib.parse import urlparse, parse_qs, urlencode
import aiohttp
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

LOGIN_URL = "https://login.dnevnik.ru/login/"
RETURN_URL = (
    "https://login.dnevnik.ru/oauth2?response_type=token"
    "&client_id=bb97b3e445a340b9b9cab4b9ea0dbd6f"
    "&scope=CommonInfo,ContactInfo,FriendsAndRelatives,EducationalInfo"
    "&redirect_uri=http://localhost:8000/callback"
)

async def get_token_from_url(url: str) -> str:
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

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    """Отображает главную страницу."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/callback", response_class=HTMLResponse)
async def callback(request: Request):
    """Обрабатывает редирект от login.dnevnik.ru."""
    return templates.TemplateResponse("callback.html", {"request": request})

@app.post("/get-token", response_class=HTMLResponse)
async def fetch_token(request: Request, body: dict):
    """Обрабатывает URL от клиента и возвращает токен."""
    try:
        url = body.get("url")
        if not url:
            raise DiaryError("URL не предоставлен")

        token = await get_token_from_url(url)
        return templates.TemplateResponse(
            "result.html",
            {"request": request, "token": token}
        )
    except DiaryError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@app.post("/proxy", response_class=JSONResponse)
async def proxy_request(request: Request, body: dict):
    """Проксирует запрос к login.dnevnik.ru, чтобы обойти CORS."""
    try:
        login_url = body.get("loginUrl")
        return_url = body.get("returnUrl")
        if not login_url or not return_url:
            raise DiaryError("Некорректные параметры запроса")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                login_url,
                params={"ReturnUrl": return_url},
                allow_redirects=True,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
            ) as response:
                if response.status != 200:
                    logger.error(f"Статус ответа: {response.status}")
                    raise DiaryError("Сайт недоступен или ведутся технические работы")

                url = str(response.url)
                logger.info(f"Ответный URL: {url}")
                return {"url": url}
    except DiaryError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Ошибка проксирования: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)