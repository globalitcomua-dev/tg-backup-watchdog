from datetime import datetime, timezone

from app.domain.check_result import BackupCheckItem, BackupCheckResult
from app.services.state_engine import BackupStateEngine


def make_result(status: str) -> BackupCheckResult:
    return BackupCheckResult(
        counters={
            "ok": 0,
            "warning": 0,
            "missing": 0,
            "failed": 0,
            "unknown": 0,
            "total": 1,
        },
        items=[
            BackupCheckItem(
                host="TopFace",
                job="TopFace",
                engine="cobian",
                expected_every_hours=24,
                status=status,
            )
        ],
    )


def test_no_change_when_status_same():
    engine = BackupStateEngine()

    changes = engine.detect_changes(
        check_result=make_result("ok"),
        previous_states={"TopFace::TopFace": "ok"},
        now=datetime(2026, 6, 25, 8, 0, tzinfo=timezone.utc),
    )

    assert changes == []


def test_change_when_status_changed():
    engine = BackupStateEngine()

    changes = engine.detect_changes(
        check_result=make_result("warning"),
        previous_states={"TopFace::TopFace": "ok"},
        now=datetime(2026, 6, 25, 8, 0, tzinfo=timezone.utc),
    )

    assert len(changes) == 1
    assert changes[0].host == "TopFace"
    assert changes[0].old_status == "ok"
    assert changes[0].new_status == "warning"


def test_no_initial_change_by_default():
    engine = BackupStateEngine()

    changes = engine.detect_changes(
        check_result=make_result("ok"),
        previous_states={},
        now=datetime(2026, 6, 25, 8, 0, tzinfo=timezone.utc),
    )

    assert changes == []


def test_initial_change_when_enabled():
    engine = BackupStateEngine()

    changes = engine.detect_changes(
        check_result=make_result("ok"),
        previous_states={},
        notify_on_initial=True,
        now=datetime(2026, 6, 25, 8, 0, tzinfo=timezone.utc),
    )

    assert len(changes) == 1
    assert changes[0].old_status is None
    assert changes[0].new_status == "ok"