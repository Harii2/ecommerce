FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

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

# Expose port 8000 for the app
EXPOSE 8000

# Add entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Run gunicorn to serve the Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_cache.wsgi:application"]
