from typing import IO

from flask import current_app

from app import db
from app.exceptions.custom_exceptions import FileNotFoundInStorageError
from app.models.file import File
from app.repositories.file_repository import FileRepository
from app.utils.hashing import FileHasher
from app.utils.storage import FileStorage
from app.models.user import User


class FileService:
    """
    Сервис для работы с файлами: загрузка, удаление и получение пути к файлу.
    """

    @staticmethod
    def upload_file(user: User, file_stream: IO) -> str:
        """
        Загружает файл в хранилище, если такого файла еще нет,
        связывает файл с пользователем в базе.

        :param user: Пользователь, загружающий файл
        :param file_stream: Поток файла (werkzeug FileStorage или похожий)
        :return: Хэш файла
        """
        file_hash = FileHasher.compute_hash(file_stream)
        current_app.logger.debug(f"Uploading file with hash: {file_hash} for user id: {user.id}")

        existing_files = FileRepository.get_by_hash(file_hash)
        if not existing_files:
            current_app.logger.info(f"Saving new file to storage: {file_hash}")
            FileStorage.save_file(file_stream, file_hash)
        else:
            current_app.logger.debug(f"File with hash {file_hash} already exists in storage")

        if not any(f.user_id == user.id for f in existing_files):
            new_file = File(hash=file_hash, user_id=user.id)
            db.session.add(new_file)
            db.session.commit()
            current_app.logger.info(f"Linked file {file_hash} to user {user.id}")

        return file_hash

    @staticmethod
    def delete_file(user: User, file_hash: str) -> None:
        """
        Удаляет файл у пользователя и, если файл больше не связан ни с кем,
        удаляет его из хранилища.

        :param user: Пользователь, пытающийся удалить файл
        :param file_hash: Хэш файла для удаления
        :raises FileNotFoundInStorageError: если у пользователя нет файла с таким хэшем
        """
        current_app.logger.debug(f"Deleting file with hash {file_hash} for user id: {user.id}")

        user_files = [f for f in FileRepository.get_by_hash(file_hash) if f.user_id == user.id]
        if not user_files:
            current_app.logger.warning(f"File {file_hash} not found for user {user.id}")
            raise FileNotFoundInStorageError()

        for file in user_files:
            db.session.delete(file)
        db.session.commit()
        current_app.logger.info(f"Deleted file records {file_hash} for user {user.id}")

        if FileRepository.count_by_hash(file_hash) == 0:
            current_app.logger.info(f"No more references to file {file_hash}, deleting from storage")
            FileStorage.delete_file(file_hash)

    @staticmethod
    def get_file_path(file_hash: str) -> str:
        """
        Возвращает путь к файлу в локальном хранилище.

        :param file_hash: Хэш файла
        :return: Абсолютный путь к файлу
        """
        path = FileStorage.get_file_path(file_hash)
        current_app.logger.debug(f"Getting file path for hash {file_hash}: {path}")
        return path

