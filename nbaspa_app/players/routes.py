"""Player pages."""

from flask import Blueprint, render_template, request
from flask import current_app as app

from nbaspa.data.endpoints.parameters import CURRENT_SEASON

players_bp = Blueprint(
    "players_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"],
    static_url_path=f"/players/{app.config['STATIC_FOLDER']}"
)


@players_bp.get("/players/top", defaults={"season": CURRENT_SEASON, "page": 1})
@players_bp.get("/players/top/<season>/<int:page>")
def top_players(season: str, page: int):
    """Produce an ordered list of players based on page."""
    return render_template(
        "top_players.html",
        title=f"{season} MVP Tracker",
        season=season,
        page=page,
        mode=request.args.get("mode", "survival-plus"),
        sortBy=request.args.get("sortBy", "mean")
    )

@players_bp.get("/players/directory")
def player_directory():
    """List all players in a given season."""
    return render_template(
        "player_directory.html",
        title="Player directory",
    )

@players_bp.get("/players/<int:playerid>")
def player_summary(playerid: int):
    """Player summary page.

    Parameters
    ----------
    playerid : int
        The player identifier.
    """
    return render_template("player_summary.html", playerid=playerid)

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
    return render_template(
        "player_season_summary.html",
        playerid=playerid,
        season=season,
    )


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
