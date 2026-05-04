FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY app/requirements.txt ./requirements.txt
RUN uv pip install --system --no-cache -r requirements.txt

COPY app/ ./app/
COPY frontend/ ./frontend/

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
