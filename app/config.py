import os
from pathlib import Path
from typing import Optional


class Config:
    """
    Конфигурация приложения.

    Атрибуты:
        SECRET_KEY (str): Секретный ключ для сессий Flask.
        SQLALCHEMY_DATABASE_URI (str): URI для подключения к базе данных.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Отключение отслеживания изменений SQLAlchemy.
        STORAGE_PATH (str): Абсолютный путь к директории для хранения файлов.
        BASIC_AUTH_FORCE (bool): Флаг, требующий базовую аутентификацию для защищенных эндпоинтов.
    """

    SECRET_KEY: str = os.environ.get('SECRET_KEY') or 'dev-key-123'

    SQLALCHEMY_DATABASE_URI: str = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{Path(__file__).parent.parent / 'data' / 'data.db'}"

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    STORAGE_PATH: str = str(Path(__file__).parent.parent / 'store')

    BASIC_AUTH_FORCE: bool = True  # Надо требовать аутентификацию для протектед ручек
