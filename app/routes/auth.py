from flask import Blueprint, jsonify, current_app
from app.services import auth_service
from app import auth


auth_bp = Blueprint('auth', __name__)


@auth.error_handler
def auth_error(status: int):
    """
    Обработчик ошибок аутентификации.

    Args:
        status (int): HTTP статус ошибки.

    Returns:
        Response: JSON с описанием ошибки и HTTP статусом.
    """
    current_app.logger.warning(f"Authentication error with status: {status}")
    if status == 401:
        return jsonify({
            "error": "Authentication required",
            "message": "Invalid credentials or missing authorization header"
        }), 401
    return jsonify({"error": "Access denied"}), status

@auth_bp.route('/verify')
@auth.login_required
def verify():
    """
    Эндпоинт для проверки аутентификации текущего пользователя.

    Возвращает имя пользователя, если аутентификация прошла успешно.
    """
    username = auth.current_user().username
    current_app.logger.info(f"User verified: {username}")
    return {"username": username}, 200
