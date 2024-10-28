#Dockerfile

# Base Image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Install Playwright dependencies
RUN apt-get update && apt-get install -y libnss3 libatk1.0-0 libcups2 libxcomposite1 libxrandr2 libxdamage1 libgdk-pixbuf2.0-0 libxkbcommon0 libx11-xcb1 libxcb-dri3-0 libgbm1
RUN python -m playwright install

# Set environment variables
ENV PLAYWRIGHT_BROWSERS_PATH=/app/playwright_browsers

# Expose port
EXPOSE 8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
