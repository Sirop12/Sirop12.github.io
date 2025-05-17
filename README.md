# Генератор токенов Дневник.ру

Простое веб-приложение на Flask для аутентификации пользователей через OAuth2 Дневник.ру и получения токена доступа для API Дневник.ру.

## Возможности

- Удобный интерфейс для запуска аутентификации через OAuth2 на Дневник.ру.
- Перенаправление на Дневник.ру для входа и получения токена доступа.
- Отображение токена для использования в API Дневник.ру (например, с библиотекой `pydnevnikruapi`).

## Структура проекта

```plaintext
dnevnik-token/
├── app.py                # Основное приложение Flask
├── static/
│   └── main.js           # Статический JavaScript (опционально)
├── templates/
│   ├── index.html        # Главная страница с кнопкой "Получить токен"
│   ├── callback.html     # Обработка callback от OAuth2
│   └── result.html       # Отображение полученного токена
├── requirements.txt      # Зависимости Python
└── README.md             # Этот файл
```

## Требования

- Python 3.8 или выше
- Учётная запись Дневник.ру для тестирования
- Зарегистрированное OAuth2-приложение Дневник.ру (client ID)

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/ваш-username/dnevnik-token.git
   cd dnevnik-token
   ```

2. Создайте и активируйте виртуальное окружение:

   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

## Локальный запуск

1. Запустите приложение Flask:

   ```bash
   python app.py
   ```

2. Откройте `http://localhost:8000` в браузере.
3. Нажмите **Получить токен**, авторизуйтесь на Дневник.ру и получите токен.

## Развёртывание

### PythonAnywhere

1. Загрузите файлы проекта в `/home/ваш-username/mysite/` на PythonAnywhere.
2. Обновите `RETURN_URL` в `app.py`:

   ```python
   RETURN_URL = (
       "https://login.dnevnik.ru/oauth2?response_type=token"
       "&client_id=bb97b3e445a340b9b9cab4b9ea0dbd6f"
       "&scope=CommonInfo,ContactInfo,FriendsAndRelatives,EducationalInfo"
       "&redirect_uri=https://ваш-username.pythonanywhere.com/callback"
   )
   ```

3. Обновите `index.html`, чтобы `redirect_uri` соответствовал.
4. Установите зависимости в консоли Bash на PythonAnywhere:

   ```bash
   pip install --user -r requirements.txt
   ```

5. Настройте WSGI-файл (`/var/www/ваш-username_pythonanywhere_com_wsgi.py`):

   ```python
   import sys
   path = '/home/ваш-username/mysite'
   if path not in sys.path:
       sys.path.append(path)
   from app import app as application
   ```

6. Перезагрузите веб-приложение через вкладку **Web** на PythonAnywhere.

### Heroku

1. Создайте файл `Procfile`:

   ```text
   web: gunicorn app:app
   ```

2. Разверните приложение:

   ```bash
   heroku login
   heroku create dnevnik-token
   git push heroku main
   ```

3. Обновите `RETURN_URL` и `index.html` с URL Heroku.

## Использование

1. Перейдите на развёрнутый сайт (например, `https://androsovpavel.pythonanywhere.com/`).
2. Нажмите **Получить токен** для аутентификации на Дневник.ру.
3. После входа токен будет отображён (например, `gu0CKxoJ1SM7OXEn2e4CYFXOOMdHvc5P`).
4. Используйте токен с библиотекой `pydnevnikruapi`:

   ```python
   from pydnevnikruapi.async_diary import DnevnikFormatter
   import asyncio

   async def test_token():
       formatter = DnevnikFormatter(token="ваш-токен")
       try:
           await formatter.initialize()
           print("Токен валиден!")
       except Exception as e:
           print(f"Ошибка токена: {e}")

   asyncio.run(test_token())
   ```

## Устранение неполадок

- **Перенаправление на `localhost:8000`**:
  Убедитесь, что `RETURN_URL` в `app.py` и `returnUrl` в `index.html` соответствуют URL развёрнутого сайта.
- **Проблемы с CORS**:
  Проверьте доступность `login.dnevnik.ru`:

   ```bash
   curl -I https://login.dnevnik.ru
   ```

- **Логи**:
  На PythonAnywhere проверяйте логи ошибок и сервера во вкладке **Web**.

## Лицензия

MIT License
