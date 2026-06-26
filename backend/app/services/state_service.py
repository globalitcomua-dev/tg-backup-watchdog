from app.repositories.backup_state import BackupStateRepository
from app.services.state_engine import BackupStateEngine


class BackupStateService:

    def __init__(self, repository: BackupStateRepository):
        self.repository = repository
        self.engine = BackupStateEngine()

    def detect(self, check_result):

        previous = {
            f"{s.host}::{s.job}": s.status
            for s in self.repository.list_all()
        }

        changes = self.engine.detect_changes(
            check_result,
            previous,
        )

        for item in check_result.items:
            self.repository.save(
                host=item.host,
                job=item.job,
                status=str(item.status),
                message=item.message,
            )

        return changes