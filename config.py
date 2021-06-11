"""Create a Flask configuration."""

import os

class Config:
    """Set the configuration."""

    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Data location
    DATA_DIR = os.environ.get("DATA_DIR")

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
