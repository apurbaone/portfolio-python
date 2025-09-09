import os
import sys

# Ensure the project directory is on sys.path
PROJECT_DIR = os.path.dirname(__file__)
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

# Set default settings module if not already set by the environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')

# Import the WSGI application
from portfolio_site.wsgi import application

# Passenger will use the `application` object from this module.
