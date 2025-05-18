# Django E-commerce Application with Redis Caching

## Project Overview
This is a Django e-commerce application with Redis caching for improved performance. The application is containerized using Docker and deployed on AWS EC2.

## Architecture

### Application Components
- **Django Web Application**: Core application logic
- **MySQL Database**: Persistent data storage
- **Redis**: Caching layer using cacheops
- **Nginx**: Web server and reverse proxy

### Deployment Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                           EC2 Instance                           │
│                                                                 │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐    │
│  │  Nginx  │     │ Django  │     │  MySQL  │     │  Redis  │    │
│  │(Port 80)│────▶│  (Web)  │────▶│  (DB)   │     │ (Cache) │    │
│  └─────────┘     └─────────┘     └─────────┘     └─────────┘    │
│                       │                               ▲          │
│                       └───────────────────────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Key Files and Their Purpose

### Docker Configuration

#### `Dockerfile`
Defines the Django application container:
- Based on Python 3.11-slim
- Installs system dependencies for MySQL
- Sets up Python environment
- Configures static files
- Uses gunicorn as the WSGI server

```dockerfile
FROM python:3.11-slim

# Install system dependencies including MySQL development libraries
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ... other configurations
```

#### `docker-compose.yml`
Orchestrates all services:
- Web (Django application)
- DB (MySQL database)
- Redis (Caching)
- Nginx (Web server)

```yaml
version: '3'

services:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    # ... environment variables and volumes

  db:
    image: mysql:8.0
    # ... configuration and healthcheck

  redis:
    image: redis:alpine
    # ... configuration and healthcheck

  nginx:
    image: nginx:alpine
    # ... configuration
```

#### `entrypoint.sh`
Script that runs when the Django container starts:
- Waits for the database to be ready
- Applies database migrations
- Executes the main command (gunicorn)

```bash
#!/bin/sh

# Wait for database to be ready
echo "Waiting for database..."
sleep 10

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Execute the command passed to docker run
exec "$@"
```

### Nginx Configuration

#### `nginx/default.conf`
Configures Nginx as a reverse proxy:
- Serves static and media files directly
- Forwards other requests to Django

```nginx
server {
    listen 80;
    server_name ec2-13-233-73-63.ap-south-1.compute.amazonaws.com;
    client_max_body_size 100M;
    
    # Serve static files
    location /static/ {
        alias /var/www/static/;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }
    
    # ... other configurations
}
```

### Django Settings

#### `django_cache/settings/base.py`
Base settings for all environments:
- Defines BASE_DIR
- Configures static files
- Sets up installed apps

#### `django_cache/settings/production.py`
Production-specific settings:
- Disables DEBUG mode
- Configures MySQL database
- Sets up security settings

```python
# Database settings for MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'django_db'),
        'USER': os.environ.get('DB_USER', 'django_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your_secure_password'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}
```

#### `django_cache/settings/cache.py`
Caching configuration:
- Sets up Redis connection
- Configures cacheops for specific models
- Enables/disables caching based on environment variable

```python
# Enable/disable cacheops functionality
ENABLE_CACHEOPS = os.environ.get("ENABLE_CACHEOPS", "TRUE") == "TRUE"

CACHEOPS_REDIS = os.environ.get(
    "CACHEOPS_REDIS", "redis://localhost:6379/1"
)

# ... model-specific cache configurations

# Only apply caching if enabled
CACHEOPS = {}
if ENABLE_CACHEOPS:
    CACHEOPS.update(PRODUCT_APP_CACHEOPS)
    CACHEOPS.update(ORDER_APP_CACHEOPS)
    CACHEOPS.update(CART_APP_CACHEOPS)
```

### Deployment Scripts

#### `deploy.sh`
Automates the deployment process:
- Installs Docker and Docker Compose
- Sets up environment variables
- Starts the application

```bash
#!/bin/bash
# Deployment script for Django Cache application on EC2

# ... system setup

# Set up environment variables
if [ ! -f .env ]; then
  echo "Creating .env file from .env.example..."
  cp .env.example .env
  
  # Generate a secure random key for Django
  DJANGO_SECRET_KEY=$(openssl rand -base64 50 | tr -dc 'a-zA-Z0-9!@#$%^&*(-_=+)' | head -c50)
  # ... other environment variable setup
fi

# Start the application
docker-compose up -d

# ... other deployment steps
```

#### `.env.example`
Template for environment variables:
- Django settings
- Database credentials
- Redis configuration

```
# Django settings
DJANGO_SETTINGS_MODULE=django_cache.settings.production
DJANGO_SECRET_KEY=django-insecure-5k9pp7z8tj0u6r9y4hx3z6f2q9c8w7b5v4m3n2j1k8l7p6o5i4
DEBUG=FALSE

# Database settings
DB_ENGINE=django.db.backends.mysql
DB_NAME=django_db
DB_USER=django_user
DB_PASSWORD=Django@2025Secure
# ... other environment variables
- **Cart App**: Handles shopping cart functionality
- **Order App**: Processes customer orders
- **Common App**: Contains shared utilities and helpers

## Technologies Used

- **Django 5.1.1**: Core web framework
- **django-cacheops**: Advanced ORM caching using Redis
- **Redis**: In-memory data store for caching
- **SQLite**: Default development database

## Caching Strategy

This project demonstrates various caching techniques:

1. **ORM Caching**: Using django-cacheops to cache database queries
2. **Redis Backend**: Leveraging Redis for high-performance caching
3. **Selective Caching**: Configured to cache specific operations on product models

## Setup and Installation

### Prerequisites

- Python 3.10+
- Redis server

### Installation Steps

1. Clone the repository
   ```
   git clone <repository-url>
   cd django_cache
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run migrations
   ```
   python manage.py migrate
   ```

5. Start the Redis server
   ```
   # Install Redis if not already installed
   # On Windows, you can use Redis for Windows or WSL
   ```

6. Run the development server
   ```
   python manage.py runserver
   ```

## Deployment

This application can be deployed to AWS using:

- **AWS Elastic Beanstalk**: Recommended for easy deployment and management
- **AWS EC2**: For more control over the server environment

## Environment Variables

- `CACHEOPS_REDIS`: Redis connection string (default: "redis://localhost:6379/1")
- `CACHEOPS_DEFAULT_TIMEOUT`: Default cache timeout in seconds (default: 86400)
- `CACHEOPS_DEGRADE_ON_FAILURE`: Whether to degrade gracefully on Redis failure (default: TRUE)

## License

MIT
