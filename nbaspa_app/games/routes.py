"""Game information."""

from datetime import datetime

from flask import Blueprint, render_template
from flask import current_app as app

TODAY = datetime.today()

game_bp = Blueprint(
    "game_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"],
    static_url_path=f"/games/{app.config['STATIC_FOLDER']}"
)



@game_bp.get(
    "/games",
    defaults={"day": TODAY.day, "month": TODAY.month, "year": TODAY.year}
)
@game_bp.get("/games/<int:day>/<int:month>/<int:year>")
def schedule(day: int, month: int, year: int):
    """The schedule page.
    
    Parameters
    ----------
    day : int
        The day of the games.
    month : int
        The month of the games.
    year : int
        The year of the games.
    """
    gamedate = datetime(year=year, month=month, day=day)
    return render_template(
        "schedule.html",
        title="Game Schedule",
        gamedate=gamedate.strftime("%A, %B %d, %Y"),
        day=day,
        month=month,
        year=year,
    )


@game_bp.get("/games/<int:day>/<int:month>/<int:year>/<gameid>")
def game(day: int, month: int, year: int, gameid: str):
    """The overall game summary page.

    Parameters
    ----------
    day : int
        The day of the games.
    month : int
        The month of the games.
    year : int
        The year of the games.
    gameid : str
        The game ID.
    """
    gamedate = datetime(year=year, month=month, day=day)
    return render_template(
        "game.html",
        year=gamedate.year,
        month=gamedate.month,
        day=gamedate.day,
        gameid=gameid
    )
