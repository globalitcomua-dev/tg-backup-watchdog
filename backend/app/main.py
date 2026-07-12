from fastapi import FastAPI

from app.api.admin import router as admin_router
from app.api.jobs import router as jobs_router
from app.api.producers import router as producers_router
from app.api.report import router as report_router
from app.api.summary import router as summary_router
from app.core.config import settings

app = FastAPI(title="TG Backup Watchdog")

app.include_router(admin_router)
app.include_router(report_router)
app.include_router(jobs_router)
app.include_router(producers_router)
app.include_router(summary_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "database_configured": bool(settings.database_url),
        "admin_token_configured": bool(settings.admin_api_token),
        "producer_auth_mode": "registry",
        "telegram_configured": bool(settings.telegram_bot_token),
        "telegram_chat_allowlist_configured": bool(settings.telegram_chat_id),
        "log_level": settings.log_level,
    }
