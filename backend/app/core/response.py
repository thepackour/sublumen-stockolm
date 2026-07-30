from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.core.error_code import ErrorCode
from app.core.logger import logger
from app.core.success_code import SuccessCode

def success(code: SuccessCode, data = None):
    logger.info(
        "API 응답 (%s): %s (%s)",
        code.code,
        code.message,
        "" if data is None else str(data),
    )
    return JSONResponse(
        status_code=code.status,
        content=jsonable_encoder({
            "status": code.status,
            "message": code.message,
            "data": data
        })
    )

def error(code: ErrorCode, data = None):
    logger.warning(
        "API 응답 (%d): %s (%s)",
        code.code,
        code.message,
        "" if data is None else str(data),
    )
    return JSONResponse(
        status_code=code.status,
        content=jsonable_encoder({
            "status": code.status,
            "message": code.message,
            "data": data
        })
    )