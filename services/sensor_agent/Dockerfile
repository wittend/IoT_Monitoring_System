FROM python:3.11-slim

WORKDIR /app

# Copy shared package first so the agent can depend on it
COPY shared/ ./shared/
COPY services/sensor_agent/ ./sensor_agent/

# Install shared package, then the agent
RUN pip install --no-cache-dir ./shared && \
    pip install --no-cache-dir ./sensor_agent

CMD ["sensor-agent"]
