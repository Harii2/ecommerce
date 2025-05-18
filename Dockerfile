FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

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

# Create directory for static files
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Make sure static files are accessible
RUN chmod -R 755 /app/staticfiles

# Expose port 8000 for the app
EXPOSE 8000

# Add entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Run gunicorn to serve the Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_cache.wsgi:application", "--log-level=debug"]
