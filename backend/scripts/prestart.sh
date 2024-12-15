#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python app/backend_pre_start.py

# alembic revision --autogenerate

# Run migrations
alembic upgrade head

# Create initial data in DB
python app/initial_data.py
