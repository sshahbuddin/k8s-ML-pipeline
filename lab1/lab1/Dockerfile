FROM python:3.10-slim-buster as build

# install security updates
RUN apt-get update \
    && apt-get upgrade -y\
    && apt-get install -y \
        curl build-essential \
    && rm -rf /var/lib/apt/lists/*

#install poetry
ENV POETRY_version = 1.3.2
RUN  curl -sSL https://install.python-poetry.org | python3 -
ENV PATH /root/.local/bin:$PATH

#prepare venv
COPY pyproject.toml poetry.lock ./
RUN python -m venv --copies ./venv
RUN . /venv/bin/activate && poetry install --no-dev

# run stage
FROM python:3.10-slim-buster as run

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
        curl build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /venv /venv
ENV PATH /venv/bin:$PATH

# copy src
COPY . ./

#run uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]