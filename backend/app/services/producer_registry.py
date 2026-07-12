from __future__ import annotations

import hashlib

from sqlalchemy.orm import Session

from app.domain.producer import ProducerDefinition, ProducerIdentity, ProducerUpdateDefinition
from app.repositories.producer_credential import ProducerCredentialRepository


class ProducerRegistryService:
    def __init__(self, db: Session):
        self.db = db
        self.credentials = ProducerCredentialRepository(db)

    def list_producers(self):
        return self.credentials.list()

    def create_producer(self, definition: ProducerDefinition):
        producer = self.credentials.create(
            producer_name=definition.producer_name.strip(),
            token_hash=self._hash_token(definition.token),
            allowed_hosts=self._normalize_values(definition.allowed_hosts),
            allowed_jobs=self._normalize_values(definition.allowed_jobs),
            description=self._normalize_description(definition.description),
            enabled=definition.enabled,
        )
        self.db.commit()
        self.db.refresh(producer)
        return producer

    def update_producer(self, producer_id: int, definition: ProducerUpdateDefinition):
        producer = self.credentials.get_by_id(producer_id)
        if producer is None:
            return None

        producer.producer_name = definition.producer_name.strip()
        producer.allowed_hosts = self._normalize_values(definition.allowed_hosts)
        producer.allowed_jobs = self._normalize_values(definition.allowed_jobs)
        producer.description = self._normalize_description(definition.description)
        producer.enabled = definition.enabled

        if definition.token is not None:
            producer.token_hash = self._hash_token(definition.token)

        self.db.commit()
        self.db.refresh(producer)
        return producer

    def delete_producer(self, producer_id: int):
        producer = self.credentials.delete_by_id(producer_id)
        if producer is None:
            return None
        self.db.commit()
        return producer

    def authenticate(self, token: str) -> ProducerIdentity | None:
        producer = self.credentials.get_by_token_hash(self._hash_token(token))
        if producer is None or not producer.enabled:
            return None

        return ProducerIdentity(
            id=producer.id,
            producer_name=producer.producer_name,
            allowed_hosts=set(producer.allowed_hosts or []),
            allowed_jobs=set(producer.allowed_jobs or []),
            enabled=producer.enabled,
        )

    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @staticmethod
    def _normalize_values(values: list[str]) -> list[str]:
        normalized: list[str] = []
        seen: set[str] = set()

        for value in values:
            item = value.strip()
            if not item or item in seen:
                continue
            normalized.append(item)
            seen.add(item)

        return normalized

    @staticmethod
    def _normalize_description(value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip()
        return normalized or None
