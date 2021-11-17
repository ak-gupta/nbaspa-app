"""Create a Flask configuration."""

import os

from nbaspa.data.endpoints.parameters import SEASONS

ASSETS_DEBUG = False
ASSETS_AUTO_BUILD = True

class Config:
    """Set the configuration."""

    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    API_TITLE = "NBA SPA web application"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.1.0"

    # Data location
    DATA_DIR = os.environ.get("DATA_DIR")
    SEASONS = {key: value for key, value in SEASONS.items() if key != "2005-06"}

class DevelopmentConfig(Config):
    """Development configuration."""

    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    FILESYSTEM = "file"

class ProductionConfig(Config):
    """Production configuration."""

    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    FILESYSTEM = "gcs"
