#!/bin/sh

echo "Connection to DB"

while ! nc -z ${SQL_HOST} ${SQL_PORT}; do
  sleep .2s
done

echo "Connected!"

python ./agora/manage.py makemigrations
python ./agora/manage.py makemigrations back_api
python ./agora/manage.py migrate
python ./agora/manage.py migrate back_api
python ./agora/manage.py base_configuration

exec "$@"