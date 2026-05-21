Это твой проект магазина на Django. Ниже короткий гайд, как поднять его на ПК.---
Что нужно установить заранее
Python 3.10+ — https://www.python.org/downloads/ (при установке поставь галочку Add Python to PATH)
Git — https://git-scm.com/downloads
---
Запуск (Windows)
Самый простой способ — одним двойным кликом
Распакуй архив (или склонируй репозиторий).
Открой папку проекта.
Дважды кликни по `start.bat`.
Скрипт сам создаст виртуальное окружение, установит зависимости и запустит сервер.
Открой в браузере: http://127.0.0.1:8000/
Если хочется вручную
Открой `cmd` или `PowerShell` в папке проекта:
```bat
python -m venv .venv
.venv\\\\Scripts\\\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
---
Запуск (macOS / Linux)
```bash
chmod +x start.sh
./start.sh
```
или вручную:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
---
Готовые учётки для входа
Логин	Пароль	Роль
zerde	zerde123	Складовик
amina	amina123	Кассир
sizi	sizi123	Кассир
Регистрация новых сотрудников — на странице `/register/`.
---
Что умеют роли
Складовик — добавляет и редактирует товары на складе.
Кассир — оформляет продажи (списывает товар со склада).
---
Полезное
Админка Django: `/admin/` (нужен суперпользователь — `python manage.py createsuperuser`)
Остановить сервер: `Ctrl + C` в терминале
Если порт 8000 занят: `python manage.py runserver 8001`
