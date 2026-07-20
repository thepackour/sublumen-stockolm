from fastapi.responses import JSONResponse

from app.core.error_code import ErrorCode
from app.core.success_code import SuccessCode

def success(code: SuccessCode, data=None):
    return JSONResponse(
        status_code=code.status,
        content={
            "status": code.status,
            "message": code.message,
            "data": data
        }
    )

def error(code: ErrorCode, data=None):
    return JSONResponse(
        status_code=code.status,
        content={
            "status": code.status,
            "message": code.message,
            "data": data
        }
    )