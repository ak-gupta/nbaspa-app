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


def gen_summarymetrics(app: Flask, teamid: int) -> List[Dict]:
    """Generate summary metrics for each team.

    Parameters
    ----------
    app : Flask
        The current application.
    teamid : int
        The team identifier.
    
    Returns
    -------
    List
        A list with one dictionary per team.
    """
    output = []
    allseasons = list(SEASONS.keys())
    allseasons.sort(reverse=True)
    for season in allseasons:
        loader = TeamStats(
            output_dir=Path(app.config["DATA_DIR"], season),
            Season=season
        )
        loader.load()
        data = loader.get_data()
        data.set_index("TEAM_ID", inplace=True)
        output.append(
            {
                "season": season,
                "record": f"{data.loc[teamid, 'W']}-{data.loc[teamid, 'L']}",
                "net_rating": data.loc[teamid, "E_NET_RATING"],
            }
        )

    return output
