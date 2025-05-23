# Builder
FROM python:3.12-alpine AS builder

WORKDIR /usr/src/app

COPY requirements.txt .

RUN apk add --no-cache build-base gcc musl-dev libffi-dev openssl-dev postgresql-dev python3-dev

RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels gunicorn==23.0.0
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt

# Final stage
FROM python:3.12-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

COPY --from=builder /usr/src/app/wheels ./wheels

RUN apk add --no-cache bash postgresql-client postgis

# Create a non-root user and group
RUN addgroup -S django && adduser -S django -G django
# Change ownership of the directory to the new user
RUN chown -R django:django /usr/src/app
# Switch to the non-root user
USER django

ENV PATH="/home/django/.local/bin:$PATH"

RUN pip install --no-cache-dir --no-index --find-links=wheels gunicorn==23.0.0
RUN pip install --no-cache-dir --no-index --find-links=wheels -r requirements.txt

RUN rm -rf wheels
RUN mkdir staticfiles

EXPOSE 8000

# Define the default command to run the server
CMD ["bash", "-c", "if [ \"$DEBUG\" = \"true\" ]; then python3 manage.py runserver 0.0.0.0:8000; else gunicorn core.wsgi:application -b 0.0.0.0:8000; fi"]
