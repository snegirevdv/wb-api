from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings

security = HTTPBearer()


async def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Сверяет предоставленный пользователем токен с установленным в системе."""
    token = credentials.credentials

    if token != settings.api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный токен.",
        )

    return token
