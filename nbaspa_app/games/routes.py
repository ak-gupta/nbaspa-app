"""Game information."""

import io
import json
import base64

from flask import Blueprint, render_template
from flask import current_app as app

from .summary import get_data

game_bp = Blueprint(
    "game_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"],
    static_url_path=f"/games/{app.config['STATIC_FOLDER']}"
)

@game_bp.get("/game/<gameid>")
def game(gameid):
    """The overall game summary page.

    Parameters
    ----------
    gameid : str
        The game ID.
    """
    tbs, pbs, prediction = get_data(app=app, GameID=gameid)
    # TODO: Replace player boxscore with the survival ratings
    # Round the percentages
    tbs["FG_PCT"] = (tbs["FG_PCT"] * 100).round(2)
    tbs["FG3_PCT"] = (tbs["FG3_PCT"] * 100).round(2)
    tbs["FT_PCT"] = (tbs["FT_PCT"] * 100).round(2)

    chart_data = prediction.to_dict(orient="records")
    chart_data = json.dumps(chart_data, indent=2)

    return render_template(
        "game.html",
        title=f"{tbs.loc[1, 'TEAM_ABBREVIATION']} @ {tbs.loc[0, 'TEAM_ABBREVIATION']} Summary",
        teambox=tbs,
        playerbox=pbs,
        chart_data=chart_data
    )
