@echo off
chcp 65001 > nul
setlocal

echo =====================================================
echo   Запуск магазина Zerde
echo =====================================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo [ОШИБКА] Python не найден.
    echo Установи Python 3.10+ с https://www.python.org/downloads/
    echo При установке поставь галочку "Add Python to PATH".
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Создаю виртуальное окружение...
    python -m venv .venv
    if errorlevel 1 (
        echo [ОШИБКА] Не удалось создать виртуальное окружение.
        pause
        exit /b 1
    )
) else (
    echo [1/3] Виртуальное окружение уже существует.
)

echo [2/3] Устанавливаю зависимости...
.venv\Scripts\python.exe -m pip install --upgrade pip >nul
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ОШИБКА] Не удалось установить зависимости.
    pause
    exit /b 1
)

echo [3/3] Применяю миграции базы данных...
.venv\Scripts\python.exe manage.py migrate

echo.
echo =====================================================
echo   Сервер запускается на http://127.0.0.1:8000/
echo   Для остановки нажми Ctrl + C
echo =====================================================
echo.

.venv\Scripts\python.exe manage.py runserver

pause
