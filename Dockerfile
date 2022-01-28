FROM python:3.9.10

RUN pip install poetry
WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN poetry install
COPY ./telegram_bot/ /code/

