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
    gameratings = pd.read_csv(
        Path(app.config["DATA_DIR"], Season, "impact-summary.csv"), sep="|", index_col=0
    )
    gameratings.set_index("PLAYER_ID", inplace=True)
    gameratings["TOTAL_IMPACT"] = gameratings["TOTAL_IMPACT"].round(3)
    gameratings["MEAN_IMPACT"] = gameratings["MEAN_IMPACT"].round(3)
    gameratings["DISPLAY_FIRST_LAST"] = playerindex["DISPLAY_FIRST_LAST"]
    gameratings.reset_index(inplace=True)
    gameratings.sort_values(by="MEAN_IMPACT", ascending=False, inplace=True)

    return gameratings.to_dict(orient="records")[:50]
