"""File I/O paths."""

import json
from pathlib import Path

from flask import Blueprint, request
from flask import current_app as app
import pandas as pd

io_bp = Blueprint("io_bp", __name__)

@io_bp.get("/players/time-series")
def player_time_series():
    """Retrieve player impact time-series."""

    performances = pd.read_csv(
        Path(
            app.config["DATA_DIR"],
            request.args["Season"],
            "impact-timeseries",
            f"data_{request.args['PlayerID']}.csv"
        ),
        sep="|",
        index_col=0,
        dtype={"GAME_ID": str}
    )
    performances.rename(columns={"IMPACT+": "IMPACT_ADJ"}, inplace=True)
    performances = performances[(performances["IMPACT"] != 0) & (performances["IMPACT_ADJ"] != 0)].copy()
    performances.dropna(inplace=True)
    performances["IMPACT"] = performances["IMPACT"].round(3)
    performances["IMPACT_ADJ"] = performances["IMPACT_ADJ"].round(3)
    # Date parsing
    performances["GAME_DATE_PARSED"] = pd.to_datetime(performances["GAME_DATE"])
    performances["DAY"] = performances["GAME_DATE_PARSED"].dt.day
    performances["MONTH"] = performances["GAME_DATE_PARSED"].dt.month
    performances["YEAR"] = performances["GAME_DATE_PARSED"].dt.year

    columns = [
        "PLAYER_ID",
        "IMPACT",
        "IMPACT_ADJ",
        "SEASON",
        "GAME_ID",
        "GAME_DATE",
        "DAY",
        "MONTH",
        "YEAR",
    ]

    return json.dumps(performances[columns].to_dict(orient="records"))
