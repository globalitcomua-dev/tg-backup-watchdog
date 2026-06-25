from fastapi import APIRouter, Depends

from app.core.dependencies import get_watchdog_service
from app.core.security import require_api_token
from app.domain.backup_report import BackupReport
from app.schemas.report import BackupReportRequest, BackupRunResponse
from app.services.watchdog import WatchdogService

router = APIRouter(prefix="/api/v1", tags=["reports"])


@router.post("/report", response_model=BackupRunResponse)
def create_report(
    payload: BackupReportRequest,
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_api_token),
):
    report = BackupReport(**payload.model_dump())
    return service.ingest(report)


@router.get("/runs", response_model=list[BackupRunResponse])
def list_runs(
    limit: int = 100,
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_api_token),
):
    return service.history(limit=limit)