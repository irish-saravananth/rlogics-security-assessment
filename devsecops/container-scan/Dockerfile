FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd --create-home --uid 10001 appuser

COPY --chown=appuser:appuser \
    sast/sample-app/app.py /app/app.py

USER 10001:10001

CMD ["python", "/app/app.py"]
