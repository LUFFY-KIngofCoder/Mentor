FROM python:3.10-slim

WORKDIR /app

# Install system dependencies that might be needed by libraries like pg_config/asyncpg
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy the requirements file from the Backend directory on your computer
COPY Backend/requirements.txt ./

# Install python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files from your computer to the container
COPY Backend/ ./

EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
