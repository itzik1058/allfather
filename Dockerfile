FROM python:3.11-bookworm

WORKDIR /app

COPY pyproject.toml LICENSE README.md .
COPY allfather ./allfather

RUN pip install .

CMD allfather
