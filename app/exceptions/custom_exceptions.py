class APIError(Exception):
    """Base exception for API errors"""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

class FileNotFoundInStorageError(APIError):
    def __init__(self, message="File not found"):
        super().__init__(message, 404)

class PermissionDeniedError(APIError):
    def __init__(self, message="Permission denied"):
        super().__init__(message, 403)

class AuthenticationError(APIError):
    def __init__(self, message="Authentication required"):
        super().__init__(message, 401)