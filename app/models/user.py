from typing import TYPE_CHECKING
from app.extensions import db
from sqlalchemy.orm import Mapped
import bcrypt
from flask import current_app


if TYPE_CHECKING:
    # Для избежания циклических импортов при type checking
    from sqlalchemy.orm import Mapped
    from werkzeug.local import LocalProxy

class User(db.Model):
    """Модель пользователя системы.

    Attributes:
        id: Уникальный идентификатор пользователя.
        username: Логин пользователя (уникальный).
        password_hash: Хеш пароля (bcrypt).
    """
    id: 'Mapped[int]' = db.Column(db.Integer, primary_key=True)
    username: 'Mapped[str]' = db.Column(db.String(64), unique=True, nullable=False)
    password_hash: 'Mapped[str]' = db.Column(db.String(128), nullable=False)

    def set_password(self, password: str) -> None:
        """Генерирует и устанавливает хеш пароля.

        Args:
            password: Пароль в чистом виде.
        """
        try:
            self.password_hash = bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')
            current_app.logger.debug(f"Password hash set for user {self.username}")
        except Exception as e:
            current_app.logger.error(f"Password hashing failed for user {self.username}: {str(e)}")
            raise

    def check_password(self, password: str) -> bool:
        """Проверяет соответствие пароля хешу.

        Args:
            password: Пароль для проверки.

        Returns:
            bool: True если пароль верный, False в противном случае.
        """
        try:
            result = bcrypt.checkpw(
                password.encode('utf-8'),
                self.password_hash.encode('utf-8')
            )
            if not result:
                current_app.logger.warning(f"Invalid password attempt for user {self.username}")
            return result
        except Exception as e:
            current_app.logger.error(f"Password check failed for user {self.username}: {str(e)}")
            return False