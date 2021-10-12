"""Create a Flask configuration."""

import os

from nbaspa.data.endpoints.parameters import SEASONS

ASSETS_DEBUG = False
ASSETS_AUTO_BUILD = True

class Config:
    """Set the configuration."""

    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Data location
    DATA_DIR = os.environ.get("DATA_DIR")
    SEASONS = SEASONS

class DevelopmentConfig(Config):
    """Development configuration."""

    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    """Production configuration."""

    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
