"""Game routes."""

from pathlib import Path
from typing import Dict, List

from flask import current_app as app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import pandas as pd

from nbaspa.data.endpoints import Scoreboard
from nbaspa.data.endpoints.pbp import EventTypes

EVT = EventTypes()

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

@io_game.route("/moments")
class TopMoments(MethodView):
    """Retrieve the top moments for a given game."""

    @io_game.arguments(sc.GameQueryArgsSchema, location="query")
    @io_game.response(200, sc.MomentsOutputSchema(many=True))
    def get(self, args):
        """Retrieve the top moments for a given game."""
        # Determine the season of the game
        for season, cfg in app.config["SEASONS"].items():
            if args["GameDate"] >= cfg["START"] and args["GameDate"] <= cfg["END"]:
                gseason = season
                break
        else:
            abort(404, message="Unable to determine the season of the game.")
        
        # Read the play-by-play impact data
        pbp = pd.read_csv(
            Path(app.config["DATA_DIR"], gseason, "pbp-impact", f"data_{args['GameID']}.csv"),
            sep="|",
            index_col=0,
            dtype={"GAME_ID": str}
        )
        # Remove duplicates and team events
        pbp = pbp[~pbp.duplicated(subset="TIME", keep="first")].copy()
        teamevents = [
            EVT.SUBSTITUTION,
            EVT.TIMEOUT,
            EVT.JUMP_BALL,
            EVT.PERIOD_BEGIN,
            EVT.UNKNOWN,
            EVT.REPLAY,
        ]
        pbp = pbp[(pbp["PLAYER1_IMPACT"] != 0) & (~pbp["EVENTMSGTYPE"].isin(teamevents))]
        pbp.sort_values(by="SURV_PROB_CHANGE", ascending=False, key=abs, inplace=True)
        # Reduce to the top 5 moments
        pbp = pbp.head(n=5).copy()
        pbp["DESCRIPTION"] = pbp[["HOMEDESCRIPTION", "VISITORDESCRIPTION"]].bfill(axis=1).iloc[:, 0]

        return pbp[
            [
                "TIME",
                "PERIOD",
                "PCTIMESTRING",
                "SCOREMARGIN",
                "SURV_PROB",
                "SURV_PROB_CHANGE",
                "DESCRIPTION",
                "PLAYER1_ID"
            ]
        ].to_dict(orient="records")

@io_game.route("/playbyplay")
class PlayByPlay(MethodView):
    """Retrieve play-by-play data for graphing."""

    @io_game.arguments(sc.GameQueryArgsSchema, location="query")
    @io_game.response(200, sc.PlayByPlayOutputSchema(many=True))
    def get(self, args):
        """Retrieve play-by-play data for graphing."""
        # Determine the season of the game
        for season, cfg in app.config["SEASONS"].items():
            if args["GameDate"] >= cfg["START"] and args["GameDate"] <= cfg["END"]:
                gseason = season
                break
        else:
            abort(404, message="Unable to determine the season of the game.")
        # Read in the play-by-play survival data
        data = pd.read_csv(
            Path(app.config["DATA_DIR"], gseason, "survival-prediction", f"data_{args['GameID']}.csv"),
            sep="|",
            index_col=0,
            dtype={"GAME_ID": str}
        )
        
        return data[["TIME", "WIN_PROB", "SCOREMARGIN"]].to_dict(orient="records")
