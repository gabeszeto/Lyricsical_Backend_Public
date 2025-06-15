FROM python:3.11-rc-slim-bullseye

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Generate Prisma client only (safe at build time)
RUN prisma generate

# Expose port
EXPOSE 8080

# Run DB push + start server at runtime
CMD prisma db push && gunicorn -w 1 --threads 4 -b 0.0.0.0:$PORT api:app
