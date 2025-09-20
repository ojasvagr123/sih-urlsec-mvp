FROM python:3.11-slim

WORKDIR /app

COPY cowrie_poller.py .
RUN pip install --no-cache-dir requests

CMD ["python", "cowrie_poller.py"]
