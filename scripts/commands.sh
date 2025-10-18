# Command to access the postgres container and family_recipes database
docker exec -it family_recipes_api-db-1 bash -c "psql -U postgres -d family_recipes"

# Command to acess the api container
docker compose run --rm api sh -c "django-admin startproject core ."