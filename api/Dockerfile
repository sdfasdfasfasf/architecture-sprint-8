FROM python:3.11.9-slim as python-stage
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PYTHONPYCACHEPREFIX=/requirements/

FROM python-stage as requirements-stage
WORKDIR /requirements/
COPY requirements.txt /requirements/

FROM python-stage as base-stage
WORKDIR /API/
ENV PYTHONPATH=$PYTHONPATH:/API/application/
COPY --from=requirements-stage /requirements/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY application ./application/

FROM base-stage as api-stage