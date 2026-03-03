import os


# Используем отдельную SQLite-базу для тестов.
# Важно выставить переменные окружения ДО импорта приложения,
# чтобы src.database.connect_db увидел правильный DATABASE_URL.
os.environ.setdefault("DATABASE_URL", "sqlite:///./tests/test.db")
os.environ.setdefault("SHORT_URL", "https://short.com")

