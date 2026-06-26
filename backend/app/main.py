from fastapi import FastAPI

from app.api.jobs import router as jobs_router
from app.api.report import router as report_router
from app.api.summary import router as summary_router
from app.core.config import settings

app = FastAPI(title="TG Backup Watchdog")

app.include_router(report_router)
app.include_router(jobs_router)
app.include_router(summary_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "database_configured": bool(settings.database_url),
        "api_token_configured": bool(settings.api_token),
        "telegram_configured": bool(settings.telegram_bot_token),
        "log_level": settings.log_level,
    }
