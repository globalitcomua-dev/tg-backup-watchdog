FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app/backend
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml .
COPY backend ./backend
COPY alembic.ini .

RUN pip install --no-cache-dir -e .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]