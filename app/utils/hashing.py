import hashlib
from typing import IO

class FileHasher:
    """
    Утилита для вычисления SHA-256 хэша файла из потока.
    """

    @staticmethod
    def compute_hash(file_stream: IO) -> str:
        """
        Вычисляет SHA-256 хэш для переданного файлового потока.

        :param file_stream: Поток файла, который нужно прочитать для хэширования
        :return: Хэш в виде строки шестнадцатеричных символов
        """
        sha256 = hashlib.sha256()
        while chunk := file_stream.read(4096):
            sha256.update(chunk)
        file_stream.seek(0)
        return sha256.hexdigest()