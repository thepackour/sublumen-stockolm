from app.core.error_code import ErrorCode


class ProjectException(Exception):

    def __init__(self, error_code: ErrorCode):
        self.status = error_code.status
        self.code = error_code.code
        self.message = error_code.message