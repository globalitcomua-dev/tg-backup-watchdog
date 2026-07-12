from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import (
    get_ingest_service,
    get_watchdog_service,
)
from app.core.security import require_admin_token, require_producer_identity
from app.domain.producer import ProducerIdentity
from app.schemas.report import (
    BackupRunResponse,
    RawMessageIn,
)
from app.services.ingest import BackupIngestService
from app.services.watchdog import WatchdogService

router = APIRouter(prefix="/api/v1", tags=["reports"])


@router.post("/report/raw")
def report_raw(
    payload: RawMessageIn,
    service: BackupIngestService = Depends(get_ingest_service),
    producer: ProducerIdentity = Depends(require_producer_identity),
):
    try:
        return service.ingest_raw_message(payload.text, producer)
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


@router.get("/runs", response_model=list[BackupRunResponse])
def list_runs(
    limit: int = 100,
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_admin_token),
):
    return service.history(limit=limit)


@router.delete("/runs/{run_id}", response_model=BackupRunResponse)
def delete_run(
    run_id: int,
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_admin_token),
):
    run = service.delete_run(run_id)

    if run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Run not found",
        )

    return run
