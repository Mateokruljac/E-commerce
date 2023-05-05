Docker commands

# start
docker-compose up -d --build

# list active containers
docker ps

# turn off
docker-compose down

# logovi
docker_logs ecommerce-web

# create migrations
docker exec $(docker ps -qf "name=ecommerce-web") python3 manage.py makemigrations

# run migrations
docker exec $(docker ps -qf "name=ecommerce-web") python3 manage.py migrate

# run tests
docker exec $(docker ps -qf "name=ecommerce-web") python3 manage.py test




