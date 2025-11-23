#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

cd school_map_project/schoolmap
python manage.py collectstatic --no-input --clear