FROM python:3.9-alpine3.13
LABEL maintainer="rabehrabie"
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /tmp/requirements.txt
COPY ./core /core
WORKDIR /core
EXPOSE 8000
RUN python3 -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev &&\
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev &&\
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps &&\
    adduser \
        --disabled-password \
        --no-create-home \
        django-user &&\
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static &&\
    chown -R django-user:django-user /vol &&\
    chmod -R 755 /vol
ENV PATH="/py/bin:$PATH"
USER django-user