"""Game information."""

from datetime import datetime
import io
import json
import base64

from flask import Blueprint, render_template, redirect, url_for
from flask import current_app as app

from .calendar import get_scoreboard, create_list
from .forms import ScheduleDatePicker
from .summary import get_data

TODAY = datetime.today()

game_bp = Blueprint(
    "game_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"],
    static_url_path=f"/games/{app.config['STATIC_FOLDER']}"
)


@game_bp.post("/games")
def picker():
    """Using the datepicker to redirect to the correct day."""
    form = ScheduleDatePicker()
    gamedate = form.gamedate.data

    return redirect(
        url_for(
            "game_bp.schedule",
            day=gamedate.day,
            month=gamedate.month,
            year=gamedate.year
        )
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
    form = ScheduleDatePicker()
    gamedate = datetime(year=year, month=month, day=day)
    scoreboard = get_scoreboard(app=app, GameDate=gamedate)
    if scoreboard.exists():
        datalist = create_list(scoreboard)
    else:
        datalist = []

    return render_template(
        "schedule.html",
        title="Game Schedule",
        form=form,
        gamedate=gamedate.strftime("%A, %B %d, %Y"),
        day=day,
        month=month,
        year=year,
        data=[datalist[i:i+3] for i in range(0, len(datalist), 3)]
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
    tbs, pbs, prediction = get_data(app=app, GameID=gameid)
    gamedate = datetime(year=year, month=month, day=day)
    scoreboard = get_scoreboard(app=app, GameDate=gamedate)
    if scoreboard.exists():
        datalist = create_list(scoreboard)
        gameinfo = [itm for itm in datalist if itm["game_id"] == gameid][0]
    # TODO: Replace player boxscore with the survival ratings
    # Round the percentages
    tbs["FG_PCT"] = (tbs["FG_PCT"] * 100).round(2)
    tbs["FG3_PCT"] = (tbs["FG3_PCT"] * 100).round(2)
    tbs["FT_PCT"] = (tbs["FT_PCT"] * 100).round(2)

    prediction["WIN_PROB"] = prediction["WIN_PROB"].round(3)
    chart_data = prediction.to_dict(orient="records")
    chart_data = json.dumps(chart_data, indent=2)

    return render_template(
        "game.html",
        title=f"{gameinfo['visitor_abbrev']} @ {gameinfo['home_abbrev']} Summary",
        teambox=tbs,
        playerbox=pbs,
        chart_data=chart_data,
        gameinfo=gameinfo
    )
