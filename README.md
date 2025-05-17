(
echo # Генератор токенов Дневник.ру
echo.
echo Простое веб-приложение на Flask для аутентификации пользователей через OAuth2 Дневник.ру и получения токена доступа для API Дневник.ру.
echo.
echo ## Возможности
echo - Удобный интерфейс для запуска аутентификации через OAuth2 на Дневник.ру.
echo - Перенаправление на Дневник.ру для входа и получения токена доступа.
echo - Отображение токена для использования в API Дневник.ру (например, с библиотекой `pydnevnikruapi`).
echo.
echo ## Структура проекта
echo ```
echo dnevnik-token/
echo ├── app.py                # Основное приложение Flask
echo ├── static/
echo │   └── main.js           # Статический JavaScript (опционально)
echo ├── templates/
echo │   ├── index.html        # Главная страница с кнопкой "Получить токен"
echo │   ├── callback.html     # Обработка callback от OAuth2
echo │   └── result.html       # Отображение полученного токена
echo ├── requirements.txt      # Зависимости Python
echo └── README.md             # Этот файл
echo ```
echo.
echo ## Требования
echo - Python 3.8 или выше
echo - Учётная запись Дневник.ру для тестирования
echo - Зарегистрированное OAuth2-приложение Дневник.ру (client ID)
echo.
echo ## Установка
echo 1. Клонируйте репозиторий:
echo    ```bash
echo    git clone https://github.com/ваш-username/dnevnik-token.git
echo    cd dnevnik-token
echo    ```
echo.
echo 2. Создайте и активируйте виртуальное окружение:
echo    ```bash
echo    python -m venv venv
echo    source venv/bin/activate  # На Windows: venv\Scripts\activate
echo    ```
echo.
echo 3. Установите зависимости:
echo    ```bash
echo    pip install -r requirements.txt
echo    ```
echo.
echo ## Локальный запуск
echo 1. Запустите приложение Flask:
echo    ```bash
echo    python app.py
echo    ```
echo.
echo 2. Откройте `http://localhost:8000` в браузере.
echo 3. Нажмите "Получить токен", авторизуйтесь на Дневник.ру и получите токен.
echo.
echo ## Развёртывание
echo ### PythonAnywhere
echo 1. Загрузите файлы проекта в `/home/ваш-username/mysite/` на PythonAnywhere.
echo 2. Обновите `RETURN_URL` в `app.py`:
echo    ```python
echo    RETURN_URL = (
echo        "https://login.dnevnik.ru/oauth2?response_type=token"
echo        "&client_id=bb97b3e445a340b9b9cab4b9ea0dbd6f"
echo        "&scope=CommonInfo,ContactInfo,FriendsAndRelatives,EducationalInfo"
echo        "&redirect_uri=https://ваш-username.pythonanywhere.com/callback"
echo    )
echo    ```
echo 3. Обновите `index.html`, чтобы `redirect_uri` соответствовал.
echo 4. Установите зависимости в консоли Bash на PythonAnywhere:
echo    ```bash
echo    pip install --user -r requirements.txt
echo    ```
echo 5. Настройте WSGI-файл (`/var/www/ваш-username_pythonanywhere_com_wsgi.py`):
echo    ```python
echo    import sys
echo    path = '/home/ваш-username/mysite'
echo    if path not in sys.path:
echo        sys.path.append(path)
echo    from app import app as application
echo    ```
echo 6. Перезагрузите веб-приложение через вкладку Web на PythonAnywhere.
echo.
echo ### Heroku
echo 1. Создайте файл `Procfile`:
echo    ```text
echo    web: gunicorn app:app
echo    ```
echo 2. Разверните приложение:
echo    ```bash
echo    heroku login
echo    heroku create dnevnik-token
echo    git push heroku main
echo    ```
echo 3. Обновите `RETURN_URL` и `index.html` с URL Heroku.
echo.
echo ## Использование
echo 1. Перейдите на развёрнутый сайт (например, `https://ваш-username.pythonanywhere.com/`).
echo 2. Нажмите "Получить токен" для аутентификации на Дневник.ру.
echo 3. После входа токен будет отображён (например, `gu0CKxoJ1SM7OXEn2e4CYFXOOMdHvc5P`).
echo 4. Используйте токен с библиотекой `pydnevnikruapi`:
echo    ```python
echo    from pydnevnikruapi.async_diary import DnevnikFormatter
echo    import asyncio
echo.
echo    async def test_token():
echo        formatter = DnevnikFormatter(token="ваш-токен")
echo        try:
echo            await formatter.initialize()
echo            print("Токен валиден!")
echo        except Exception as e:
echo            print(f"Ошибка токена: {e}")
echo.
echo    asyncio.run(test_token())
echo    ```
echo.
echo ## Устранение неполадок
echo - **Перенаправление на `localhost:8000`**: Убедитесь, что `RETURN_URL` в `app.py` и `returnUrl` в `index.html` соответствуют URL развёрнутого сайта.
echo - **Проблемы с CORS**: Проверьте доступность `login.dnevnik.ru`:
echo    ```bash
echo    curl -I https://login.dnevnik.ru
echo    ```
echo - **Логи**: На PythonAnywhere проверяйте логи ошибок и сервера во вкладке Web.
echo.
echo ## Лицензия
echo MIT License
) > README.md
