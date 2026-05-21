#!/usr/bin/env bash
set -e

echo "====================================================="
echo "  Запуск магазина Zerde"
echo "====================================================="

PYTHON=python3
if ! command -v $PYTHON >/dev/null 2>&1; then
    PYTHON=python
fi

if [ ! -x ".venv/bin/python" ]; then
    echo "[1/3] Создаю виртуальное окружение..."
    $PYTHON -m venv .venv
else
    echo "[1/3] Виртуальное окружение уже существует."
fi

echo "[2/3] Устанавливаю зависимости..."
.venv/bin/python -m pip install --upgrade pip >/dev/null
.venv/bin/python -m pip install -r requirements.txt

echo "[3/3] Применяю миграции..."
.venv/bin/python manage.py migrate

echo
echo "====================================================="
echo "  Сервер запускается на http://127.0.0.1:8000/"
echo "  Для остановки нажми Ctrl + C"
echo "====================================================="

.venv/bin/python manage.py runserver
