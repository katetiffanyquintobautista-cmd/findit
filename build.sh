#!/usr/bin/env bash
# exit on error
set -o errexit

# Use pip cache for faster builds
pip install --upgrade pip
pip install -r requirements.txt --cache-dir /opt/render/project/.pip-cache

cd school_map_project/schoolmap
python manage.py collectstatic --no-input
python manage.py migrate