"""Initialize flask app."""

from flask import Flask

def create_app(config: str = "development"):
    """Create the core application.

    Parameters
    ----------
    prod : str, optional (default "development")
        Whether to use the production configuration or the development.

    Returns
    -------
    Flask
        The initialized application.
    """
    app = Flask(__name__, instance_relative_config=False)
    if config == "production":
        app.config.from_object("config.ProductionConfig")
    elif config == "development":
        app.config.from_object("config.DevelopmentConfig")
    else:
        raise ValueError("Please provide a valid value for ``config``")

    with app.app_context():
        # Include the routes
        from .games.routes import game_bp
        from .home.routes import home_bp
        from .schedule.routes import schedule_bp
        from .teams.routes import teams_bp

        app.register_blueprint(game_bp)
        app.register_blueprint(home_bp)
        app.register_blueprint(schedule_bp)
        app.register_blueprint(teams_bp)

        return app
