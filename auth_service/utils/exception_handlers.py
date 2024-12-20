from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException


def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "detail": exc.message
        }
    )
