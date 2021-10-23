"""Get season summary data."""

from pathlib import Path
from typing import Dict, List

from flask import Flask

from nbaspa.data.endpoints import AllPlayers

def get_all_players(app: Flask) -> List[Dict]:
    """Get all players.
    
    Parameters
    ----------
    app : Flask
        The current application.
    
    Returns
    -------
    List
        The JSON-ified output.
    """
    # Using 2019-20 season for the player directory
    loader = AllPlayers(
        output_dir=Path(app.config["DATA_DIR"], "2019-20"),
        Season="2019-20"
    )
    if not loader.exists():
        raise FileNotFoundError("Cannot find the roster info.")
    loader.load()
    df = loader.get_data()
    df.drop_duplicates(subset="PERSON_ID", keep="first", inplace=True)
    df["SECTION"] = df["DISPLAY_LAST_COMMA_FIRST"].str[0]
    df["TO_YEAR"] = df["TO_YEAR"].astype(int)
    df = df[df["TO_YEAR"] >= 2005].copy()

    output = {}
    for name, group in df.groupby("SECTION"):
        records = group.to_dict(orient="records")
        output[name] = [records[i:i+3] for i in range(0, len(records), 3)]

    return output
