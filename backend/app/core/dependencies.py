from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.watchdog import WatchdogService


def get_watchdog_service(db: Session = Depends(get_db)) -> WatchdogService:
    return WatchdogService(db)