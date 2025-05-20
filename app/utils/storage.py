import os
from typing import IO

from flask import current_app

from app.config import Config
from app.exceptions.custom_exceptions import FileNotFoundInStorageError

class FileStorage:
    """
    Класс для работы с файловым хранилищем: формирование путей, сохранение и удаление файлов.
    """

    @staticmethod
    def get_file_path(file_hash: str) -> str:
        """
        Формирует полный путь к файлу по его хэшу.

        :param file_hash: Хэш файла
        :return: Полный путь к файлу в файловой системе
        """
        return os.path.join(
            Config.STORAGE_PATH,
            file_hash[:2],
            file_hash
        )

    @staticmethod
    def save_file(file_stream: IO, file_hash: str) -> str:
        """
        Сохраняет файл из потока в хранилище по пути, основанному на хэше.

        :param file_stream: Поток файла для сохранения
        :param file_hash: Хэш файла для имени и пути
        :return: Путь к сохранённому файлу
        """
        path = FileStorage.get_file_path(file_hash)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            with open(path, 'wb') as f:
                file_stream.seek(0)
                f.write(file_stream.read())
            current_app.logger.info(f"File saved successfully at {path}")
        except Exception as e:
            current_app.logger.error(f"Failed to save file {file_hash} at {path}: {e}")
            raise
        return path

    @staticmethod
    def delete_file(file_hash: str) -> None:
        """
        Удаляет файл из хранилища по хэшу.

        :param file_hash: Хэш файла для удаления
        :raises FileNotFoundInStorageError: Если файл не найден для удаления
        """
        path = FileStorage.get_file_path(file_hash)
        if os.path.exists(path):
            try:
                os.remove(path)
                current_app.logger.info(f"File {file_hash} deleted from storage.")
            except Exception as e:
                current_app.logger.error(f"Failed to delete file {file_hash} at {path}: {e}")
                raise
        else:
            current_app.logger.warning(f"File {file_hash} not found in storage at {path}")
            raise FileNotFoundInStorageError(f"File not found: {file_hash}")
