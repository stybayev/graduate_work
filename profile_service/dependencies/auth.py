from uuid import UUID
import uuid
from functools import wraps
from fastapi import HTTPException, status, Request
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.config import settings
from jose import jwt
import time
import http


def access_token_required(func):
    @wraps(func)
    async def wrapper(self, authorize: AuthJWT, *args, **kwargs):
        try:
            await authorize.jwt_required()
        except AuthJWTException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )
        return await func(self, authorize, *args, **kwargs)

    return wrapper


async def get_current_user(authorize: AuthJWT) -> UUID:
    await authorize.jwt_required()
    user_id = uuid.UUID(await authorize.get_jwt_subject())
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    return user_id


class JWTBearer(HTTPBearer):
    """
    Класс JWTBearer реализует метод __call__, который достает Bearer-токен из заголовка запроса.
    Если Bearer-токен отсутствует, то метод вернет ошибку.
    """

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    @staticmethod
    def decode_token(token: str) -> dict | None:
        """
        Функция декодирования токена
        """
        try:
            decoded_token = jwt.decode(token, settings.jwt.authjwt_secret_key,
                                       algorithms=[settings.jwt.authjwt_algorithm])
            return decoded_token if decoded_token['exp'] >= time.time() else None
        except Exception:
            return None

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='Invalid authorization code.')
        if not credentials.scheme == 'Bearer':
            raise HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail='Only Bearer token might be accepted')
        decoded_token = self.parse_token(credentials.credentials)
        if not decoded_token:
            raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='Invalid or expired token.')
        return decoded_token

    @staticmethod
    def parse_token(jwt_token: str) -> dict | None:
        return JWTBearer.decode_token(jwt_token)


security_jwt = JWTBearer()
