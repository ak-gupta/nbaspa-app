"""Initialize flask app."""

__version__ = "2021.11.3"
__description__ = "NBA SPA web application"

import os

from flask import Flask
from flask_assets import Environment
from flask_smorest import Api

from .assets import compile_assets

assets = Environment()
api = Api()


def create_app(config: str = "development"):
    """Create the core application.

    Parameters
    ----------
    config : str, optional (default "development")
        Whether to use the production configuration or the development.

    Returns
    -------
    Flask
        The initialized application.
    """
    app = Flask(__name__, instance_relative_config=False)
    if "FLASK_CONFIG" in os.environ:
        config = os.environ["FLASK_CONFIG"]
    if config == "production":
        app.config.from_object("config.ProductionConfig")
    elif config == "development":
        app.config.from_object("config.DevelopmentConfig")
    else:
        raise ValueError("Please provide a valid value for ``config``")

    assets.init_app(app)
    api.init_app(app)

    with app.app_context():
        # Include the routes
        from .games.routes import game_bp
        from .home.routes import home_bp
        from .io.games.routes import io_game
        from .io.league.routes import io_league
        from .io.players.routes import io_players
        from .io.teams.routes import io_teams
        from .league.routes import league_bp
        from .players.routes import players_bp
        from .teams.routes import teams_bp

        app.register_blueprint(game_bp)
        app.register_blueprint(home_bp)
        app.register_blueprint(io_game)
        app.register_blueprint(io_league)
        app.register_blueprint(io_players)
        app.register_blueprint(io_teams)
        app.register_blueprint(players_bp)
        app.register_blueprint(league_bp)
        app.register_blueprint(teams_bp)

        compile_assets(assets)

        return app
