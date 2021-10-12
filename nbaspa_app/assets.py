"""Compile assets to minified bundles using Flask-Assets."""

from flask import current_app as app
from flask_assets import Bundle

def compile_assets(assets):
    """Configure and build bundles."""
    # Player-page bundle
    player_js_bundle = Bundle(
        "players_bp/src/js/*.js",
        "players_bp/src/js/compare/*.js",
        filters="rjsmin",
        output="dist/js/players.min.js",
    )
    assets.register("player_js", player_js_bundle)
    if app.config["FLASK_ENV"] == "development":
        player_js_bundle.build()
