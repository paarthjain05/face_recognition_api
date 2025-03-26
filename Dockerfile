# Use Python 3.9 for compatibility
FROM python:3.9

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    make \
    libopenblas-dev \
    liblapack-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libgtk2.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the Flask app port
EXPOSE 5000

# Start the API with Gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
