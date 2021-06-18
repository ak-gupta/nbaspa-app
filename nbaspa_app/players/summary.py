"""Get season summary data."""

from pathlib import Path
from typing import Dict, List

from flask import Flask
import pandas as pd

from nbaspa.data.endpoints import AllPlayers

def get_top_players(app: Flask, Season: str) -> List[Dict]:
    """Get the top players for a given season.

    Parameters
    ----------
    app : Flask
        The current application.
    Season : str
        The season to search for.
    
    Returns
    -------
    List
        The JSON-ified output.
    """
    loader = AllPlayers(
        output_dir=Path(app.config["DATA_DIR"], Season),
        Season=Season
    )
    if not loader.exists():
        raise FileNotFoundError("Cannot find the roster info.")
    loader.load()

    playerindex = loader.get_data()
    playerindex.set_index("PERSON_ID", inplace=True)
    gameratings = pd.concat(
        pd.read_csv(fpath, sep="|", index_col=0, dtype={"GAME_ID": str})
        for fpath in Path(app.config["DATA_DIR"], Season, "game-impact").glob("data_*.csv")
    )
    avg = gameratings.groupby("PLAYER_ID")["IMPACT"].agg(["sum", "mean"])
    avg["sum"] = avg["sum"].round(3)
    avg["mean"] = avg["mean"].round(3)
    avg["DISPLAY_FIRST_LAST"] = playerindex["DISPLAY_FIRST_LAST"]
    avg.reset_index(inplace=True)
    avg.sort_values(by="mean", ascending=False, inplace=True)

    return avg.to_dict(orient="records")[:25]
