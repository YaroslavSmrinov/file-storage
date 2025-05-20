
from typing import Optional

from flask import current_app

from app.models.user import User


class UserRepository:
    """Репозиторий для работы с сущностью User."""

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        """
        Получить пользователя по имени пользователя.

        Args:
            username (str): Имя пользователя.

        Returns:
            Optional[User]: Объект User или None, если не найден.
        """
        current_app.logger.debug(f"Поиск пользователя с username='{username}'")
        user = User.query.filter_by(username=username).first()
        if user:
            current_app.logger.debug(f"Пользователь найден: id={user.id}")
        else:
            current_app.logger.debug("Пользователь не найден")
        return user
