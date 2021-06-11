"""Game information."""

import io
import base64

from flask import Blueprint, render_template
from flask import current_app as app
import matplotlib.pyplot as plt

from .summary import get_data, create_lineplot

game_bp = Blueprint(
    "game_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"]
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

    plot = create_lineplot(data=prediction)
    img = io.BytesIO()
    plt.savefig(img, format="png")
    plt.close()
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode("utf-8")

    return render_template(
        "game.html",
        title=f"{tbs.loc[1, 'TEAM_ABBREVIATION']} @ {tbs.loc[0, 'TEAM_ABBREVIATION']} Summary",
        plot_url=plot_url,
        teambox=tbs
    )
