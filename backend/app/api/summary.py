from fastapi import APIRouter, Depends

from app.core.dependencies import get_watchdog_service
from app.core.security import require_api_token
from app.schemas.state import BackupStateView, UntrackedBackupRunView
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


@router.get("/states", response_model=list[BackupStateView])
def states(
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_api_token),
):
    return service.list_states()


@router.get("/runs/untracked", response_model=list[UntrackedBackupRunView])
def untracked_runs(
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_api_token),
):
    return service.list_untracked_runs()
