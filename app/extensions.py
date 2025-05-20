import logging
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

db = SQLAlchemy()  # Объект SQLAlchemy для работы с базой данных.


auth = HTTPBasicAuth()  # Объект HTTPBasicAuth для базовой HTTP-аутентификации.
