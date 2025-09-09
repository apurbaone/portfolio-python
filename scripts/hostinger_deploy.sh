#!/usr/bin/env bash
# Helper script for Hostinger hPanel Git deployment (shared hosting)
# Usage: run on the server after the git repo is deployed by hPanel.

set -euo pipefail

echo "Activating virtualenv (if exists)..."
if [ -d ".venv" ]; then
  source .venv/bin/activate
elif [ -d "venv" ]; then
  source venv/bin/activate
else
  echo "No virtualenv found in .venv or venv. Create one and install requirements." >&2
fi

echo "Installing requirements..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Deployment script finished. If you're using Passenger, the app should reload automatically." 
