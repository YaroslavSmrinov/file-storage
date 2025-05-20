from typing import Optional

from flask import current_app

from app import auth
from app.repositories.user_repository import UserRepository
from app.models.user import User


class AuthService:
    """
    Сервис аутентификации пользователей, реализующий проверку логина и пароля.
    """

    @staticmethod
    @auth.verify_password
    def verify_password(username: str, password: str) -> Optional[User]:
        """
        Проверяет имя пользователя и пароль.

        :param username: Имя пользователя из запроса
        :param password: Пароль из запроса
        :return: Объект User, если аутентификация успешна, иначе None
        """
        current_app.logger.debug(f"Authentication attempt for user: {username}")

        user = UserRepository.get_by_username(username)
        if not user:
            current_app.logger.warning(f"Authentication failed: user '{username}' not found")
            return None

        if not user.check_password(password):
            current_app.logger.warning(f"Authentication failed: invalid password for user '{username}'")
            return None

        current_app.logger.info(f"User '{username}' authenticated successfully")
        return user
