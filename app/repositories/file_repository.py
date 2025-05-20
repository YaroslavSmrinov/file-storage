from flask import current_app

from typing import List
from app.models.file import File


class FileRepository:
    """Репозиторий для работы с сущностью File."""

    @staticmethod
    def get_by_hash(file_hash: str) -> List[File]:
        """
        Получить список файлов по хэшу.

        Args:
            file_hash (str): Хэш файла.

        Returns:
            List[File]: Список объектов File с данным хэшем.
        """
        current_app.logger.debug(f"Запрос файлов с hash={file_hash}")
        files = File.query.filter_by(hash=file_hash).all()
        current_app.logger.debug(f"Найдено {len(files)} файлов")
        return files

    @staticmethod
    def count_by_hash(file_hash: str) -> int:
        """
        Подсчитать количество файлов с данным хэшем.

        Args:
            file_hash (str): Хэш файла.

        Returns:
            int: Количество файлов с этим хэшем.
        """
        count = File.query.filter_by(hash=file_hash).count()
        current_app.logger.debug(f"Количество файлов с hash={file_hash}: {count}")
        return count
