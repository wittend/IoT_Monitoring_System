"""FastAPI application for the collector service."""

from __future__ import annotations

import logging
import os
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from iot_shared.models import Alert, AlertSeverity, SensorReading, SensorType

from .store import ReadingStore

logger = logging.getLogger(__name__)


def create_app(store: ReadingStore | None = None) -> FastAPI:
    """Application factory — accepts an optional store for testing."""
    if store is None:
        store = ReadingStore()

    app = FastAPI(
        title="IoT Collector",
        description=(
            "Ingests sensor readings, stores them, evaluates alert rules, "
            "and serves a REST API."
        ),
        version="0.1.0",
    )

    # CORS origins are restricted to a configurable list.
    # Set CORS_ORIGINS to a comma-separated list of allowed origins, e.g.
    # "https://dashboard.example.com,https://admin.example.com".
    # Defaults to an empty list (no cross-origin requests allowed).
    cors_origins_env = os.getenv("CORS_ORIGINS", "")
    cors_origins = [o.strip() for o in cors_origins_env.split(",") if o.strip()]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_methods=["GET", "POST", "PATCH"],
        allow_headers=["Content-Type"],
    )

    # ------------------------------------------------------------------
    # Readings
    # ------------------------------------------------------------------

    @app.post("/readings", response_model=SensorReading, status_code=status.HTTP_201_CREATED)
    async def ingest_reading(reading: SensorReading) -> SensorReading:
        """Accept a sensor reading and store it. Returns the stored reading."""
        alerts = store.add_reading(reading)
        if alerts:
            logger.info("Reading %s triggered %d alert(s)", reading.id, len(alerts))
        return reading

    @app.get("/readings", response_model=list[SensorReading])
    async def list_readings(
        sensor_id: str | None = Query(default=None),
        sensor_type: SensorType | None = Query(default=None),
        since: datetime | None = Query(default=None),
        limit: int = Query(default=100, ge=1, le=1000),
    ) -> list[SensorReading]:
        """Return stored readings, optionally filtered."""
        return store.get_readings(
            sensor_id=sensor_id,
            sensor_type=sensor_type,
            since=since,
            limit=limit,
        )

    # ------------------------------------------------------------------
    # Alerts
    # ------------------------------------------------------------------

    @app.get("/alerts", response_model=list[Alert])
    async def list_alerts(
        acknowledged: bool | None = Query(default=None),
        severity: AlertSeverity | None = Query(default=None),
        limit: int = Query(default=100, ge=1, le=1000),
    ) -> list[Alert]:
        """Return stored alerts, optionally filtered."""
        return store.get_alerts(acknowledged=acknowledged, severity=severity, limit=limit)

    @app.patch("/alerts/{alert_id}/acknowledge", response_model=Alert)
    async def acknowledge_alert(alert_id: str) -> Alert:
        """Mark an alert as acknowledged."""
        alert = store.acknowledge_alert(alert_id)
        if alert is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found",
            )
        return alert

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    @app.get("/health")
    async def health() -> dict:
        """Liveness check."""
        return {"status": "ok"}

    return app


app = create_app()


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    )
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("collector.app:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
