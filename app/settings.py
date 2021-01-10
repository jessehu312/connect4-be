"""Settings configuration - Configuration for environment variables can go in here."""

import os
import pathlib
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv('FLASK_ENV', default='production')
DEBUG = ENV == 'development'
SECRET_KEY = os.getenv('SECRET_KEY', default='octocat')

RADAR_PUBLISHABLE_KEY = os.getenv('RADAR_PUBLISHABLE_KEY')
RADAR_SECRET_KEY = os.getenv('RADAR_SECRET_KEY')