"""Game-picker information."""

from datetime import datetime

from flask import Blueprint, redirect, render_template, url_for
from flask import current_app as app
import pandas as pd

from .calendar import get_data, create_list

TODAY = datetime.today()

schedule_bp = Blueprint(
    "schedule_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"]
)

@schedule_bp.get(
    "/schedule", defaults={"day": TODAY.day, "month": TODAY.month, "year": TODAY.year}
)
@schedule_bp.get("/schedule/<int:day>/<int:month>/<int:year>")
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
    scoreboard = get_data(app=app, GameDate=gamedate)
    if scoreboard.exists():
        datalist = create_list(scoreboard)
    else:
        datalist = []

    return render_template(
        "schedule.html",
        title="Game Schedule",
        gamedate=gamedate.strftime("%A, %B %d, %Y"),
        data=[datalist[i:i+3] for i in range(0, len(datalist), 3)]
    )
