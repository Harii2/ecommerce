# Django Cache Project

A Django e-commerce application demonstrating advanced caching techniques using Redis and django-cacheops.

## Project Overview

This project is a simple e-commerce platform with the following components:

- **Products App**: Manages product listings and details
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
