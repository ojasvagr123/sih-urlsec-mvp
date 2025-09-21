FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /cowrie

COPY . /cowrie

# Install minimal python deps (logger/parser are stdlib-only; keep twisted optional)
RUN pip install --no-cache-dir -r python/requirements.txt || true

EXPOSE 2222

CMD ["/bin/bash", "/cowrie/bin/run-cowrie.sh"]
