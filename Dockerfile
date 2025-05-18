FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt to install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project
COPY . .

# Run migrations to create/initialize the SQLite database
RUN python manage.py migrate

# Expose port 8000 for the app
EXPOSE 8000

# Run gunicorn to serve the Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_cache.wsgi:application"]
