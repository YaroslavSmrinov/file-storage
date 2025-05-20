import logging
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

logger = logging.getLogger(__name__)

db = SQLAlchemy()  # Объект SQLAlchemy для работы с базой данных.


auth = HTTPBasicAuth()  # Объект HTTPBasicAuth для базовой HTTP-аутентификации.
