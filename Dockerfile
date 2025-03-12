# Use Python 3.12.2 image based on Debian Bullseye in its slim variant as the base image
FROM python:3.12.2-slim

# Set environment variables using key=value format
ENV PYTHONBUFFERED=1
ENV PORT=8080

# Set the working directory within the container to /app for any subsequent commands
WORKDIR /app

# Copy the entire current directory contents into the container at /app
COPY . /app/

# Upgrade pip to ensure we have the latest version for installing dependencies
RUN pip install --upgrade pip

# Install dependencies from the requirements.txt file to ensure our Python environment is ready
RUN pip install -r requirements.txt

# Migrate database
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Use JSON format for CMD to allow proper signal handling
CMD ["gunicorn", "DjangoProject.wsgi:application", "--bind", "0.0.0.0:8080"]

# Inform Docker that the container listens on the specified network port at runtime
EXPOSE $PORT