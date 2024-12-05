#!/bin/bash

# Define the container name
CONTAINER_NAME="postgresql"  # Replace with your container name

# Define database credentials
DB_NAME="rateit"
DB_USER="postgres"
DB_PASSWORD="postgres"

# Connect to the PostgreSQL container, drop the database if it exists, and create it
echo "Connecting to PostgreSQL container to drop and create the database..."

# Drop the database if it exists
docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -c "DROP DATABASE IF EXISTS $DB_NAME;"

# Create the database
docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -c "CREATE DATABASE $DB_NAME;"

# Run Django migrations
echo "Running Django migrations..."
python manage.py migrate

echo "Script execution completed."
