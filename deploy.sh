#!/bin/bash
# Deployment script for Django Cache application on EC2

# Exit on error
set -e

echo "===== Starting deployment ====="

# Update system
echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install Docker and Docker Compose
echo "Installing Docker and Docker Compose..."
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# Create required directories
echo "Creating required directories..."
mkdir -p nginx logs certbot/conf certbot/www

# Set permissions
echo "Setting permissions..."
sudo chmod -R 755 logs
sudo chmod -R 755 nginx

# Set up environment variables
echo "Setting up environment variables..."
if [ ! -f .env ]; then
  echo "Creating .env file from .env.example..."
  cp .env.example .env
  
  # Generate a secure random key for Django
  DJANGO_SECRET_KEY=$(openssl rand -base64 50 | tr -dc 'a-zA-Z0-9!@#$%^&*(-_=+)' | head -c50)
  # Use perl instead of sed for better handling of special characters
  perl -i -pe "s/change_this_to_a_secure_random_key/$DJANGO_SECRET_KEY/g" .env
  
  # Prompt for database password
  echo "Enter a secure password for the database:"
  read -s DB_PASSWORD
  # Escape special characters in the password
  DB_PASSWORD_ESCAPED=$(echo "$DB_PASSWORD" | sed 's/[\/&]/\\&/g')
  perl -i -pe "s/change_this_to_secure_password/$DB_PASSWORD_ESCAPED/g" .env
  
  # Prompt for MySQL root password
  echo "Enter a secure password for MySQL root user:"
  read -s MYSQL_ROOT_PASSWORD
  # Escape special characters in the password
  MYSQL_ROOT_PASSWORD_ESCAPED=$(echo "$MYSQL_ROOT_PASSWORD" | sed 's/[\/&]/\\&/g')
  perl -i -pe "s/change_this_to_secure_root_password/$MYSQL_ROOT_PASSWORD_ESCAPED/g" .env
  
  echo "Environment variables set up successfully!"
else
  echo ".env file already exists. Using existing environment variables."
fi

# Start the application
echo "Starting the application with Docker Compose..."
docker-compose up -d

# Create superuser (interactive)
echo "Do you want to create a superuser? (y/n)"
read create_superuser
if [ "$create_superuser" = "y" ]; then
  docker-compose exec web python manage.py createsuperuser
fi

# Collect static files
echo "Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput

# Apply migrations
echo "Applying migrations..."
docker-compose exec web python manage.py migrate

echo "===== Deployment complete ====="
echo "Your application should now be running at http://your-ec2-ip"
echo "To check the status, run: docker-compose ps"
echo "To view logs, run: docker-compose logs"
