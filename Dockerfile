ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV POST=8080

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Upgrade pip to ensure we have the latest version for installing dependencies
RUN pip install --upgrade pip

# Download dependencies.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Ensure migrations directory exists and has proper permissions
RUN mkdir -p /app/chat_app/migrations && \
    touch /app/chat_app/migrations/__init__.py && \
    chown -R appuser:appuser /app/chat_app/migrations && \
    chmod -R 755 /app/chat_app/migrations

# Switch to the non-privileged user to run the application.
USER appuser

# Expose the port that the application listens on.
EXPOSE $PORT

# Run the application.
CMD ["daphne", "-b", "0.0.0.0", "-p", "8080", "DjangoProject.asgi:application"]