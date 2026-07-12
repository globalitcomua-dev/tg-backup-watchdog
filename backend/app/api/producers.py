from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_producer_registry_service
from app.core.security import require_admin_token
from app.domain.producer import ProducerDefinition, ProducerUpdateDefinition
from app.schemas.producer import ProducerRequest, ProducerResponse, ProducerUpdateRequest
from app.services.producer_registry import ProducerRegistryService

router = APIRouter(prefix="/api/v1", tags=["producers"])


@router.get("/producers", response_model=list[ProducerResponse])
def list_producers(
    service: ProducerRegistryService = Depends(get_producer_registry_service),
    _: None = Depends(require_admin_token),
):
    return service.list_producers()


@router.post("/producers", response_model=ProducerResponse)
def create_producer(
    payload: ProducerRequest,
    service: ProducerRegistryService = Depends(get_producer_registry_service),
    _: None = Depends(require_admin_token),
):
    definition = ProducerDefinition(**payload.model_dump())
    return service.create_producer(definition)


@router.put("/producers/{producer_id}", response_model=ProducerResponse)
def update_producer(
    producer_id: int,
    payload: ProducerUpdateRequest,
    service: ProducerRegistryService = Depends(get_producer_registry_service),
    _: None = Depends(require_admin_token),
):
    definition = ProducerUpdateDefinition(**payload.model_dump())
    producer = service.update_producer(producer_id, definition)
    if producer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producer not found",
        )
    return producer


@router.delete("/producers/{producer_id}", response_model=ProducerResponse)
def delete_producer(
    producer_id: int,
    service: ProducerRegistryService = Depends(get_producer_registry_service),
    _: None = Depends(require_admin_token),
):
    producer = service.delete_producer(producer_id)
    if producer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producer not found",
        )
    return producer
