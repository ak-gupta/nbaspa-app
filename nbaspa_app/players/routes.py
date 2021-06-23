"""Player pages."""

from flask import abort, Blueprint, render_template
from flask import current_app as app
from flask.helpers import make_response

from nbaspa.data.endpoints.parameters import CURRENT_SEASON

from .summary import get_top_players, get_player_info

players_bp = Blueprint(
    "players_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"]
)

@players_bp.get("/players/top", defaults={"season": CURRENT_SEASON})
@players_bp.get("/players/top/<season>")
def top_players(season: str):
    """Get the top players in a given season.

    Parameters
    ----------
    season : str
        The season.
    """
    try:
        best = get_top_players(app=app, Season=season)
        return render_template(
            "top_players.html",
            title=f"{season} Top Players",
            season=season,
            data=best,
        )
    except FileNotFoundError:
        return abort(404)

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
    except FileNotFoundError:
        return abort(404)

    return render_template(
        "player_summary.html",
        title=f"{info['DISPLAY_FIRST_LAST']} Summary",
        playerid=playerid,
        info=info
    )
