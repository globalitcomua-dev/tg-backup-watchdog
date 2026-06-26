from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_watchdog_service
from app.core.security import require_api_token
from app.domain.job import BackupJobDefinition
from app.schemas.job import BackupJobRequest, BackupJobResponse
from app.services.watchdog import WatchdogService

router = APIRouter(prefix="/api/v1", tags=["jobs"])


@router.post("/jobs", response_model=BackupJobResponse)
def create_job(
    payload: BackupJobRequest,
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_api_token),
):
    definition = BackupJobDefinition(**payload.model_dump())
    return service.create_or_update_job(definition)


@router.get("/jobs", response_model=list[BackupJobResponse])
def list_jobs(
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_api_token),
):
    return service.list_jobs()


@router.put("/jobs/{job_id}", response_model=BackupJobResponse)
def update_job(
    job_id: int,
    payload: BackupJobRequest,
    service: WatchdogService = Depends(get_watchdog_service),
    _: None = Depends(require_api_token),
):
    definition = BackupJobDefinition(**payload.model_dump())
    job = service.update_job(job_id, definition)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return job
