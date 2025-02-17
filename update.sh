#! /bin/sh

set -e

echo "----- Clearing Python cache -----"
# https://stackoverflow.com/a/30659970
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

echo "----- Updating Python Dependencies -----"
pipenv install --dev --keep-outdated
pip install -r requirements.production.txt

echo "----- Updating Node Dependencies -----"
yarn install --modules-folder /node_modules --frozen-lockfile

echo "----- Rebuilding GraphQL queries -----"
yarn querybuilder

echo "----- Migrating Database -----"
python manage.py migrate --noinput
python manage.py initgroups
