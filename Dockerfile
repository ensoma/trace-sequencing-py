FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"

# Set up working directory
WORKDIR /app

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* /app/

# Configure poetry to not use virtualenvs inside Docker
RUN poetry config virtualenvs.create false

# Copy the rest of the application
COPY . /app/

# Install dependencies via Poetry
RUN poetry install --without dev --no-interaction --no-ansi

# Install the package with pip for command line access
RUN pip install -e .
