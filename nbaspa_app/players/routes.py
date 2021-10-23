"""Player pages."""

from flask import abort, Blueprint, render_template, url_for
from flask import current_app as app

from nbaspa.data.endpoints.parameters import CURRENT_SEASON, SEASONS

from .summary import (
    get_player_info,
    get_top_performances,
    get_all_players
)

players_bp = Blueprint(
    "players_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"],
    static_url_path=f"/players/{app.config['STATIC_FOLDER']}"
)


@players_bp.get("/players/directory")
def player_directory():
    """List all players in a given season."""
    return render_template(
        "player_directory.html",
        title="Player directory",
        data=get_all_players(app=app)
    )

@players_bp.get("/players/<int:playerid>")
def player_summary(playerid: int):
    """Player summary page.

    Parameters
    ----------
    playerid : int
        The player identifier.
    """
    try:
        info = get_player_info(app=app, PlayerID=playerid)
        # Get the available seasons
        seasons = []
        for idx in range(info["FROM_YEAR"], info["TO_YEAR"] + 1):
            for key in SEASONS:
                if idx == int(key.split("-")[0]):
                    seasons.append(key)
                    break
    except FileNotFoundError:
        return abort(404)

    return render_template(
        "player_summary.html",
        title=f"{info['DISPLAY_FIRST_LAST']} Summary",
        playerid=playerid,
        info=info,
        seasons=sorted(seasons)
    )

@players_bp.get("/players/<int:playerid>/<season>")
def player_season_summary(playerid: int, season: str):
    """Player summary page.

    Parameters
    ----------
    playerid : int
        The player identifier.
    season : str
        The season.
    """
    try:
        info = get_player_info(app=app, PlayerID=playerid)
        # Get the available seasons
        seasons = []
        for idx in range(info["FROM_YEAR"], info["TO_YEAR"] + 1):
            for key in SEASONS:
                if idx == int(key.split("-")[0]):
                    seasons.append(key)
                    break
    except FileNotFoundError:
        return abort(404)

    return render_template(
        "player_season_summary.html",
        title=f"{info['DISPLAY_FIRST_LAST']} Summary",
        playerid=playerid,
        season=season,
        seasons=seasons
    )


@players_bp.get("/performances/top", defaults={"season": CURRENT_SEASON})
@players_bp.get("/performances/top/<season>")
def top_performances(season: str):
    """Get the top performances in a given season.

    Parameters
    ----------
    season : str
        The season.
    """
    try:
        best = get_top_performances(app=app, Season=season)
        return render_template(
            "top_performances.html",
            title=f"{season} Top Performances",
            season=season,
            data=best[:50],
        )
    except FileNotFoundError:
        return abort(404)

@players_bp.get("/season/<season>")
def season_home(season: str):
    """Get the season summary page.
    
    Parameters
    ----------
    season : str
        The season.
    """
    return render_template(
        "season_home.html", title=f"{season} Summary", season=season,
    )
