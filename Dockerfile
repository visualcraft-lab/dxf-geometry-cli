FROM python:3.12-slim
WORKDIR /app
COPY cli.py /app/cli.py
ENTRYPOINT ["python3", "/app/cli.py"]
