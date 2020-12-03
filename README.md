# TestingPlatform

## Copy .env
'''sh
    cp .env.example .env
'''

## Build project
'''sh
    docker-compose build
'''

## Migrate database
'''sh
    docker-compose run server python manage.py migrate
'''

### Superuser created automatically
username: admin
password: sets in .env (default: qweqweqwe)

## Load 2 tickets from fixture
'''sh
    docker-compose run server python manage.py loaddata tickets/fixtures/two_tickets.json
'''

## Run project
'''sh
    docker-compose up
'''
