"""Game routes."""

from pathlib import Path
from typing import Dict, List

from flask import current_app as app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from nbaspa.data.endpoints import Scoreboard

from . import schemas as sc

io_game = Blueprint(
    "io_game", __name__, url_prefix="/api/game", description="Load game data"
)

@io_game.route("/schedule")
class Schedule(MethodView):
    """Load basic information about every game on a given day."""

    @io_game.arguments(sc.ScheduleQueryArgsSchema, location="query")
    @io_game.response(200, sc.ScheduleOutputSchema(many=True))
    def get(self, args):
        """Load information about every game on a given day."""
        # Determine the season of the game
        for season, cfg in app.config["SEASONS"].items():
            if args["GameDate"] >= cfg["START"] and args["GameDate"] <= cfg["END"]:
                gseason = season
                break
        else:
            abort(404, message="Offseason. No games.")
        
        loader = Scoreboard(
            output_dir=Path(app.config["DATA_DIR"], gseason),
            filesystem=app.config["FILESYSTEM"],
            GameDate=args["GameDate"].strftime("%m/%d/%Y")
        )
        if not loader.exists():
            abort(404, message="No games found on this day.")
        loader.load()
        # Parse and create output
        header = loader.get_data("GameHeader")
        linescore = loader.get_data("LineScore")

        output: List[Dict] = []
        for _, row in header.iterrows():
            home = linescore[linescore["TEAM_ID"] == row["HOME_TEAM_ID"]]
            visitor = linescore[linescore["TEAM_ID"] == row["VISITOR_TEAM_ID"]]
            output.append(
                {
                    "GAME_ID": row["GAME_ID"],
                    "HOME_TEAM_ID": row["HOME_TEAM_ID"],
                    "HOME_ABBREVIATION": home["TEAM_ABBREVIATION"].values[0],
                    "VISITOR_TEAM_ID": row["VISITOR_TEAM_ID"],
                    "VISITOR_ABBREVIATION": visitor["TEAM_ABBREVIATION"].values[0],
                    "HOME_PTS": home["PTS"].values[0],
                    "VISITOR_PTS": visitor["PTS"].values[0]
                }
            )
        
        return output
