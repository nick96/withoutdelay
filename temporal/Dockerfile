FROM python:3.8

WORKDIR /temporal

RUN pip install poetry

COPY poetry.lock pyproject.toml ./
RUN poetry version && poetry install --no-dev

COPY ./temporal/ ./temporal

CMD poetry run python -m temporal
