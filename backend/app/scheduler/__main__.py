from app.scheduler.service import BackupMonitorScheduler


if __name__ == "__main__":
    BackupMonitorScheduler.from_settings().run_forever()
