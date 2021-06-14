"""Create some summary plotting for each game."""

import os
from pathlib import Path
from typing import Tuple

from flask import Flask
import pandas as pd

from nbaspa.data.endpoints import BoxScoreTraditional
from nbaspa.model.tasks.meta import META

def get_data(app: Flask, GameID: str) -> Tuple:
    """Load the summary data.

    Parameters
    ----------
    app : Flask
        The current application.
    GameID : str
        The game identifier.
    """
    season = GameID[2] + "0" + GameID[3:5] + "-" + str(int(GameID[3:5]) + 1)
    boxscore = BoxScoreTraditional(
        output_dir=os.path.join(app.config["DATA_DIR"], season),
        GameID=GameID
    )

    boxscore.load()
    tdata = boxscore.get_data("TeamStats")
    pdata = boxscore.get_data("PlayerStats")

    prediction = pd.read_csv(
        Path(app.config["DATA_DIR"], season, "survival-prediction", f"data_{GameID}.csv"),
        sep="|",
        index_col=0,
        dtype={"GAME_ID": str}
    )

    return tdata, pdata, prediction
