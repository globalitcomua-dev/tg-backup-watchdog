from fastapi import Header, HTTPException, status

from app.core.config import settings


def require_api_token(authorization: str | None = Header(default=None)) -> None:
    if not settings.api_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API token is not configured",
        )

    expected = f"Bearer {settings.api_token}"

    if authorization != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )