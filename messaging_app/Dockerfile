# Use Python 3.10 as base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . /app/

# Expose port 8000
# To run: docker run -p 8000:8000 <image-name>
EXPOSE 8000

# Run migrations and start server
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000

