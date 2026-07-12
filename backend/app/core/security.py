import logging

from fastapi import Depends, Header, HTTPException, status

from app.core.config import settings
from app.domain.producer import ProducerIdentity
from app.services.producer_registry import ProducerRegistryService
from app.core.dependencies import get_producer_registry_service


logger = logging.getLogger(__name__)


def _extract_bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header",
        )

    return token.strip()


def require_admin_token(authorization: str | None = Header(default=None)) -> None:
    if not settings.admin_api_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin API token is not configured",
        )

    token = _extract_bearer_token(authorization)

    if token != settings.admin_api_token:
        logger.warning("Admin token authorization failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )


def require_producer_identity(
    authorization: str | None = Header(default=None),
    registry: ProducerRegistryService = Depends(get_producer_registry_service),
) -> ProducerIdentity:
    token = _extract_bearer_token(authorization)
    producer = registry.authenticate(token)

    if producer is None:
        logger.warning("Producer token authorization failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    return producer
