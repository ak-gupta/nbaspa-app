"""Initialize flask app."""

from flask import Flask, render_template
from flask_assets import Environment
from flask_smorest import Api

from .assets import compile_assets

assets = Environment()
api = Api()

def not_found(e):
    """Not found error page."""
    return render_template(
        "not_found.html", title="Data Not Found"
    )


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
    
    assets.init_app(app)
    api.init_app(app)


    with app.app_context():
        # Include the routes
        from .games.routes import game_bp
        from .home.routes import home_bp
        from .io.players.routes import io_players
        from .players.routes import players_bp
        from .teams.routes import teams_bp

        app.register_error_handler(404, not_found)
        app.register_blueprint(game_bp)
        app.register_blueprint(home_bp)
        app.register_blueprint(io_players)
        app.register_blueprint(players_bp)
        app.register_blueprint(teams_bp)

        compile_assets(assets)

        return app
