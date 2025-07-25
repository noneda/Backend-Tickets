#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Apply a static files
python manage.py collectstatic

# Apply any outstanding database migrations
python manage.py migrate
