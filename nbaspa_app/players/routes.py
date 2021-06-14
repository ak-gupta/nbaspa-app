"""Player pages."""

from flask import Blueprint, render_template
from flask import current_app as app

players_bp = Blueprint(
    "players_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"]
)

@players_bp.get("/players/<int:playerid>")
def player_summary(playerid: int):
    """Player summary page.

    Parameters
    ----------
    playerid : int
        The player identifier.
    """
    return render_template(
        "player_summary.html",
        title=f"{playerid} Summary",
        playerid=playerid,
        playername=playerid, # TODO: Get player meta
    )
