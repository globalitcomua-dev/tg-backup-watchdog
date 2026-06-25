from fastapi import APIRouter, Depends

from app.core.dependencies import get_watchdog_service
from app.core.security import require_api_token
from app.services.watchdog import WatchdogService

router = APIRouter(prefix="/api/v1", tags=["summary"])


@router.get("/summary")
def summary(
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_api_token),
):
    return service.summary()


@router.get("/check")
def check(
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_api_token),
):
    return service.check()