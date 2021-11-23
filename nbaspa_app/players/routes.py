"""Player pages."""

from flask import Blueprint, render_template
from flask import current_app as app

players_bp = Blueprint(
    "players_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"],
    static_url_path=f"/players/{app.config['STATIC_FOLDER']}",
)


@players_bp.get("/players/directory")
def player_directory():
    """List all players in a given season."""
    return render_template(
        "directory.html",
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
    return render_template("summary.html", playerid=playerid)


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
        "season.html",
        playerid=playerid,
        season=season,
    )
