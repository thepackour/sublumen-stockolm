from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ProjectException
from app.core.error_code import ErrorCode


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(ProjectException)
    async def project_exception_handler(
        request: Request, 
        exc: ProjectException
    ):
        return JSONResponse(
            status_code=exc.code,
            content={
                "code": exc.code,
                "message": exc.message,
                # "data": exc.data
            }
        )
    
    @app.exception_handler(Exception)
    async def exception_handler(
        request: Request, 
        exc: Exception
    ):
        return JSONResponse(
            status_code=ErrorCode.GENERAL500_1.status,
            content={
                "code": ErrorCode.GENERAL500_1.code,
                "message": ErrorCode.GENERAL500_1.message,
                "data": None
            }
        )