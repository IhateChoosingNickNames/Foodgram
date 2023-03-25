# Foodgram
[![YaMDb workflow](https://github.com/IhateChoosingNickNames/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/IhateChoosingNickNames/foodgram-project-react/actions/workflows/yamdb_workflow.yml)

Description: Application for recipe/ingredient management

Used technologies:
-
    - python 3.10.4
    - django 4.1
    - djangorestframework 3.14
    - django-filter 22.1
    - djoser 2.1.0
    - reportlab 3.6.12
    - pydantic 1.10.6
    - Postgresql
    - dotenv 0.21.1
    - Docker 20.10.22

Features:
-
    - Create new recipes
    - Filter recipes by tags
    - Add recipes to personal shopping card
    - Download pdf of all ingredients from shopping card
    - Populate DB with JSON or CSV files
    - Manage users and content with django admin-users


Instructions:

## enviroment:
Create .env file backend/.env and fill it with required keys:
- SECRET_KEY=...
- DB_ENGINE=...
- DB_NAME=...
- POSTGRES_USER=...
- POSTGRES_PASSWORD=...
- DB_HOST=db
- DB_PORT=5432

## Docker:
Build containers:
    #### docker-compose up -d --build
For now app is available at localhost

### Some additional commands: 
1. Fill DB's ingredient table with prepared data(should be placed in backend_static folder):
    #### docker-compose exec web python manage.py populate_db
2. Create admin-user:
    #### winpty docker-compose exec web python manage.py createsuperuser
3. To make dump of DB:
    #### docker-compose exec web python manage.py dumpdata > your_fixture_name.json
4. To load fixtures:
    #### docker-compose exec web python manage.py loaddata your_fixture_name.json

If you'll need any *manage.py* commands then you'll want to use prefix:

    docker-compose exec web python manage.py *comand*

All available endpoints and responses you can find in documentation:

    # http://your_ip:your_port/redoc


Author: Larkin Michael