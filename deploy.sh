#!/bin/bash

# Build the Docker image
docker compose -f docker-compose-deploy.yml up -d

# Generate static files
docker compose -f docker-compose-deploy.yml run --rm api sh -c "python manage.py collectstatic --noinput"

echo "Deployment complete!"