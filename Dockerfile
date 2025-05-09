FROM python:3.11-alpine

# Install build dependencies for any packages that might need compilation
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    && pip install --no-cache-dir -U pip

# Explicitly upgrade setuptools to a patched version to fix CVE-2024-6345
RUN pip install --no-cache-dir -U "setuptools>=67.0.0"

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies with specific version constraints
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "werkzeug==2.0.1" \
    && apk del .build-deps

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000



# Set Flask to listen on all interfaces
ENV FLASK_RUN_HOST=0.0.0.0

# Run as non-root user for better security
RUN adduser -D appuser
USER appuser

# Command to run the application
CMD ["python", "run.py"]