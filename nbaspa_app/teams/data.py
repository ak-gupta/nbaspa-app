"""Reading in the team data."""

from pathlib import Path
from typing import Dict, List

from flask import Flask
from nbaspa.data.endpoints import TeamStats
from nbaspa.data.endpoints.parameters import SEASONS

def gen_teamlist(app: Flask) -> List[Dict]:
    """Generate the team list.

    Parameters
    ----------
    app : Flask
        The current application.
    
    Returns
    -------
    List
        A list of dictionaries with the team ID and team name.
    """
    allseasons = list(SEASONS.keys())
    currseason = sorted(allseasons)[-1]
    loader = TeamStats(
        output_dir=Path(app.config["DATA_DIR"], currseason),
        Season=currseason
    )
    loader.load()
    data = loader.get_data()
    data.sort_values(by="TEAM_NAME", ascending=True, inplace=True)

    output = []
    for _, row in data.iterrows():
        output.append({"teamid": row["TEAM_ID"], "teamname": row["TEAM_NAME"]})
    
    return output
