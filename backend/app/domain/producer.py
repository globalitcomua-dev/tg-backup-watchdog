from pydantic import BaseModel, Field


class ProducerDefinition(BaseModel):
    producer_name: str = Field(min_length=1, max_length=100)
    token: str = Field(min_length=1, max_length=512)
    allowed_hosts: list[str] = Field(default_factory=list)
    allowed_jobs: list[str] = Field(default_factory=list)
    description: str | None = Field(default=None, max_length=2000)
    enabled: bool = True


class ProducerUpdateDefinition(BaseModel):
    producer_name: str = Field(min_length=1, max_length=100)
    token: str | None = Field(default=None, min_length=1, max_length=512)
    allowed_hosts: list[str] = Field(default_factory=list)
    allowed_jobs: list[str] = Field(default_factory=list)
    description: str | None = Field(default=None, max_length=2000)
    enabled: bool = True


class ProducerIdentity(BaseModel):
    id: int
    producer_name: str
    allowed_hosts: set[str] = Field(default_factory=set)
    allowed_jobs: set[str] = Field(default_factory=set)
    enabled: bool = True

