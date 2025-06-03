FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies including MySQL development libraries
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Ensure Python is in PATH
ENV PATH="/usr/local/bin:${PATH}"

# Copy requirements.txt to install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=django_cache.settings.local

# Copy the entire Django project
COPY . .

# Create directories with correct permissions
RUN mkdir -p /var/www/static/ \
    && mkdir -p /var/www/media/ \
    && mkdir -p /app/static/

# Ensure proper permissions
RUN chown -R www-data:www-data /var/www/ \
    && chmod -R 755 /var/www/ \
    && chown -R www-data:www-data /app/static/ \
    && chmod -R 755 /app/static/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000 for the app
EXPOSE 8000

# Add entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Run gunicorn to serve the Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_cache.wsgi:application", "--log-level=debug"]
