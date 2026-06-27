from app.domain.status import BackupStatus
from app.parsers.dispatcher import BackupParserDispatcher


def test_parse_cobian_english_warning():
    dispatcher = BackupParserDispatcher()

    report = dispatcher.parse(
        "[24.06.2026 2:39] backup: TopFace     2026-06-24 02:39:26 "
        "** Number of errors: 2. Time elapsed: 1 hours, 49 minutes, 24 seconds. **"
    )

    assert report.host == "TopFace"
    assert report.job == "TopFace"
    assert report.engine == "cobian"
    assert report.parser_name == "cobian"
    assert report.status == BackupStatus.WARNING
    assert report.error_count == 2
    assert report.duration_seconds == 6564


def test_parse_cobian_ukrainian_success():
    dispatcher = BackupParserDispatcher()

    report = dispatcher.parse(
        "[24.06.2026 14:32] backup: Vivere     2026-06-24 14:32:11 "
        "** Кількість помилок: 0. Витрачено часу: 0 год, 2 хв, 9 сек. **"
    )

    assert report.host == "Vivere"
    assert report.engine == "cobian"
    assert report.parser_name == "cobian"
    assert report.status == BackupStatus.SUCCESS
    assert report.error_count == 0
    assert report.duration_seconds == 129


def test_parse_custom_ok():
    dispatcher = BackupParserDispatcher()

    report = dispatcher.parse(
        "[24.06.2026 23:47] backup: [OK] Vartovi Backup process completed and uploaded to SB2."
    )

    assert report.host == "Vartovi"
    assert report.engine == "custom"
    assert report.parser_name == "custom-ok"
    assert report.status == BackupStatus.SUCCESS


def test_parse_restic_ok():
    dispatcher = BackupParserDispatcher()

    report = dispatcher.parse(
        "[24.06.2026 19:13] backup: [Ideatech] [Ideatech] ✅ Restic backup OK "
        "on WIN-8QG8UG99BG9\n"
        "• Snapshot: snapshot 098343e9"
    )

    assert report.host == "Ideatech"
    assert report.engine == "restic"
    assert report.parser_name == "restic"
    assert report.status == BackupStatus.SUCCESS
    assert report.snapshot_id == "098343e9"


def test_parse_restic_watchdog_canonical_format():
    dispatcher = BackupParserDispatcher()

    report = dispatcher.parse(
        "[WIN-272627A7S64] [Amstar] ✅ OK Restic backup via smb\n"
        "Files:          0 new,     12 changed, 152340 unmodified\n"
        "Dirs:           0 new,     3 changed, 20110 unmodified\n"
        "Added to the repository: 1.288 GiB (1.234 GiB stored)\n"
        "processed 152352 files, 103.916 GiB in 1:23:54\n"
        "Snapshot: snapshot 37231659\n"
        "Warnings: 2\n"
        "Transport: smb\n"
        "Repo: X:\\\n"
        "Log: C:\\backup\\Amstar\\logs\\backup_2026-06-26_20-00-06.log"
    )

    assert report.host == "WIN-272627A7S64"
    assert report.job == "Amstar"
    assert report.engine == "restic"
    assert report.parser_name == "restic"
    assert report.status == BackupStatus.SUCCESS
    assert report.snapshot_id == "37231659"
    assert report.duration_seconds == 5034
    assert report.destination == "X:\\"
    assert report.error_count == 0


def test_parse_restic_watchdog_warning_format():
    dispatcher = BackupParserDispatcher()

    report = dispatcher.parse(
        "[WIN-272627A7S64] [Amstar] ⚠️ WARNING Restic backup via sftp\n"
        "processed 152352 files, 103.916 GiB in 27:14\n"
        "Snapshot: snapshot 37231659\n"
        "Warnings: 3\n"
        "Transport: sftp\n"
        "Repo: sftp://repo.example/amstar"
    )

    assert report.host == "WIN-272627A7S64"
    assert report.job == "Amstar"
    assert report.status == BackupStatus.WARNING
    assert report.duration_seconds == 1634
    assert report.destination == "sftp://repo.example/amstar"
    assert report.error_count == 3
