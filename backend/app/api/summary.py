from fastapi import APIRouter, Depends

from app.core.dependencies import get_watchdog_service
from app.core.security import require_admin_token
from fastapi import HTTPException, status

from app.schemas.state import BackupStateDetailView, BackupStateView, UntrackedBackupRunView
from app.services.watchdog import WatchdogService

router = APIRouter(prefix="/api/v1", tags=["summary"])


@router.get("/summary")
def summary(
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_admin_token),
):
    return service.summary()


@router.get("/check")
def check(
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_admin_token),
):
    return service.check()


@router.get("/states", response_model=list[BackupStateView])
def states(
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_admin_token),
):
    return service.list_states()


@router.get("/runs/untracked", response_model=list[UntrackedBackupRunView])
def untracked_runs(
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_admin_token),
):
    return service.list_untracked_runs()


@router.get("/states/{job_id}", response_model=BackupStateDetailView)
def state_detail(
    job_id: int,
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_admin_token),
):
    detail = service.get_state_detail(job_id)
    if detail is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="State not found",
        )

    return detail
