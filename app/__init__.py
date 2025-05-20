from typing import List, Dict
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from app.extensions import db, auth
from app.models.user import User
from app.routes.auth import auth_bp
from app.routes.files import files_bp


def create_app() -> Flask:
    """
    Создаёт и конфигурирует Flask приложение.

    Инициализирует расширения, регает блюпринты,
    создает таблицы в базе данных и инициализирует дефолтных пользователей.

    Returns:
        Flask: экземпляр Flask приложения.
    """
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)

    app.register_blueprint(files_bp, url_prefix='/files')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    _setup_logging(app)

    with app.app_context():
        db.create_all()
        _initialize_default_users()

    logging.info("Flask application created and initialized.")

    return app


def _initialize_default_users() -> None:
    """
    Создаёт дефолтных пользователей в базе, если они отсутствуют.
    """
    users: List[Dict[str, str]] = [
        {'username': 'user1', 'password': 'password1'},
        {'username': 'user2', 'password': 'password2'},
        {'username': 'user3', 'password': 'password3'}
    ]

    for user_data in users:
        if not User.query.filter_by(username=user_data['username']).first():
            user = User(username=user_data['username'])
            user.set_password(user_data['password'])
            db.session.add(user)
            logging.info(f"User '{user_data['username']}' created.")
    db.session.commit()


def _setup_logging(app):
    logs_dir = os.path.join(os.getcwd(), 'logs')
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)

    log_file = os.path.join(logs_dir, 'file_storage.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    app.logger.info('Application startup')