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
    # League-page bundle
    league_js_bundle = Bundle(
        "league_bp/src/js/awards.js",
        "league_bp/src/js/compare/*.js",
        filters="rjsmin",
        output="dist/js/league.min.js"
    )
    # Player-page bundle
    player_js_bundle = Bundle(
        "players_bp/src/js/base.js",
        "players_bp/src/js/directory.js",
        "players_bp/src/js/player/*.js",
        filters="rjsmin",
        output="dist/js/players.min.js",
    )
    # Team bundle
    team_js_bundle = Bundle(
        "teams_bp/src/js/teamlist.js",
        filters="rjsmin",
        output="dist/js/teams.min.js"
    )
    # Register bundles
    assets.register("shared_js", shared_js_bundle)
    assets.register("league_js", league_js_bundle)
    assets.register("player_js", player_js_bundle)
    assets.register("teams_js", team_js_bundle)
    # Build
    if app.config["FLASK_ENV"] == "development":
        shared_js_bundle.build()
        league_js_bundle.build()
        player_js_bundle.build()
        team_js_bundle.build()
