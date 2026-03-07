FROM python:3.11-slim

WORKDIR /app

# Copy shared package and the collector service
COPY shared/ ./shared/
COPY services/collector/ ./collector/

# Install shared package, then the collector
RUN pip install --no-cache-dir ./shared && \
    pip install --no-cache-dir ./collector

EXPOSE 8000

CMD ["collector"]
