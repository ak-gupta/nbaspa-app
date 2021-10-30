"""Compile assets to minified bundles using Flask-Assets."""

from flask import current_app as app
from flask_assets import Bundle

def compile_assets(assets):
    """Configure and build bundles."""
    # Shared bundle
    shared_js_bundle = Bundle(
        "src/js/search.js",
        filters="rjsmin",
        output="dist/js/shared.min.js"
    )
    # Player-page bundle
    player_js_bundle = Bundle(
        "players_bp/src/js/awards.js",
        "players_bp/src/js/base.js",
        "players_bp/src/js/directory.js",
        "players_bp/src/js/compare/*.js",
        "players_bp/src/js/player/*.js",
        filters="rjsmin",
        output="dist/js/players.min.js",
    )
    # Register bundles
    assets.register("shared_js", shared_js_bundle)
    assets.register("player_js", player_js_bundle)
    # Build
    if app.config["FLASK_ENV"] == "development":
        shared_js_bundle.build()
        player_js_bundle.build()
