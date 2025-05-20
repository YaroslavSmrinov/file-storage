from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped
from app.extensions import db


if TYPE_CHECKING:
    # Для избежания циклических импортов при type checking
    from sqlalchemy.orm import Mapped
    from werkzeug.local import LocalProxy


class File(db.Model):
    """Модель для хранения информации о загруженных файлах.

    Attributes:
        id: Уникальный идентификатор файла в БД.
        hash: SHA-256 хеш содержимого файла.
        user_id: Ссылка на владельца файла.
        user: Связь с моделью User (backref: files).
    """
    id: 'Mapped[int]' = db.Column(db.Integer, primary_key=True)
    hash: 'Mapped[str]' = db.Column(db.String(64), nullable=False)
    user_id: 'Mapped[int]' = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user: 'Mapped["User"]' = db.relationship('User', backref=db.backref('files', lazy=True))
