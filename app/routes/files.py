from flask import Blueprint, request, send_file, current_app
from app.exceptions.custom_exceptions import FileNotFoundInStorageError
from app.extensions import auth
from app.services.file_service import FileService


files_bp = Blueprint('files', __name__, url_prefix='/files')
"""
Blueprint для работы с загрузкой, удалением и скачиванием файлов.
"""

@files_bp.route('/upload', methods=['POST'])
@auth.login_required
def upload():
    """
    Эндпоинт для загрузки файла.

    Проверяет наличие файла в запросе, вызывает сервис для сохранения файла,
    возвращает хэш файла при успехе.
    """
    if 'file' not in request.files:
        current_app.logger.warning("Upload attempt without file part")
        return {'error': 'No file part'}, 400

    file = request.files['file']
    if file.filename == '':
        current_app.logger.warning("Upload attempt with empty filename")
        return {'error': 'No selected file'}, 400

    try:
        file_hash = FileService.upload_file(auth.current_user(), file)
        current_app.logger.info(f"File uploaded successfully: {file_hash} by user {auth.current_user().username}")
        return {'hash': file_hash}, 200
    except Exception as e:
        current_app.logger.error(f"Error during file upload: {e}")
        return {'error': str(e)}, 500


@files_bp.route('/<string:file_hash>', methods=['DELETE'])
@auth.login_required
def delete(file_hash):
    """
    Эндпоинт для удаления файла по его хэшу.

    Вызывает сервис удаления файла. Возвращает 204 при успехе.
    """
    try:
        FileService.delete_file(auth.current_user(), file_hash)
        current_app.logger.info(f"File deleted successfully: {file_hash} by user {auth.current_user().username}")
        return '', 204
    except FileNotFoundInStorageError:
        current_app.logger.warning(f"Delete attempt for non-existent file: {file_hash}")
        return {'error': 'File not found'}, 404
    except Exception as e:
        current_app.logger.error(f"Error during file deletion: {e}")
        return {'error': str(e)}, 500


@files_bp.route('/<string:file_hash>', methods=['GET'])
def download(file_hash):
    """
    Эндпоинт для скачивания файла по его хэшу.

    Возвращает файл, если он существует.
    """
    try:
        file_path = FileService.get_file_path(file_hash)
        current_app.logger.info(f"File download requested: {file_hash}")
        return send_file(file_path, as_attachment=True)
    except FileNotFoundInStorageError:
        current_app.logger.warning(f"Download attempt for non-existent file: {file_hash}")
        return {'error': 'File not found'}, 404
