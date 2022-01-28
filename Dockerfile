FROM python:3.9.10

RUN sudo apt-get install build-essential libssl-dev libffi-dev python3-dev cargo
RUN pip install poetry
WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN poetry install
COPY ./telegram_bot/ /code/

