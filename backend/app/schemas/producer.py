from datetime import datetime

from pydantic import BaseModel, Field


class ProducerRequest(BaseModel):
    producer_name: str = Field(min_length=1, max_length=100)
    token: str = Field(min_length=1, max_length=512)
    allowed_hosts: list[str] = Field(default_factory=list)
    allowed_jobs: list[str] = Field(default_factory=list)
    description: str | None = Field(default=None, max_length=2000)
    enabled: bool = True


class ProducerUpdateRequest(BaseModel):
    producer_name: str = Field(min_length=1, max_length=100)
    token: str | None = Field(default=None, min_length=1, max_length=512)
    allowed_hosts: list[str] = Field(default_factory=list)
    allowed_jobs: list[str] = Field(default_factory=list)
    description: str | None = Field(default=None, max_length=2000)
    enabled: bool = True


class ProducerResponse(BaseModel):
    id: int
    producer_name: str
    allowed_hosts: list[str]
    allowed_jobs: list[str]
    description: str | None = None
    enabled: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }

