from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ProducerCredential


class ProducerCredentialRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        producer_name: str,
        token_hash: str,
        allowed_hosts: list[str],
        allowed_jobs: list[str],
        description: str | None,
        enabled: bool,
    ) -> ProducerCredential:
        producer = ProducerCredential(
            producer_name=producer_name,
            token_hash=token_hash,
            allowed_hosts=allowed_hosts,
            allowed_jobs=allowed_jobs,
            description=description,
            enabled=enabled,
        )
        self.db.add(producer)
        self.db.flush()
        return producer

    def list(self) -> list[ProducerCredential]:
        stmt = select(ProducerCredential).order_by(ProducerCredential.producer_name)
        return list(self.db.scalars(stmt))

    def get_by_id(self, producer_id: int) -> ProducerCredential | None:
        return self.db.get(ProducerCredential, producer_id)

    def get_by_name(self, producer_name: str) -> ProducerCredential | None:
        stmt = select(ProducerCredential).where(ProducerCredential.producer_name == producer_name)
        return self.db.scalars(stmt).first()

    def get_by_token_hash(self, token_hash: str) -> ProducerCredential | None:
        stmt = select(ProducerCredential).where(ProducerCredential.token_hash == token_hash)
        return self.db.scalars(stmt).first()

    def delete_by_id(self, producer_id: int) -> ProducerCredential | None:
        producer = self.get_by_id(producer_id)
        if producer is None:
            return None
        self.db.delete(producer)
        return producer

