"""Marshmallow schemas for the game endpoints."""

from marshmallow import Schema, fields


class ScheduleQueryArgsSchema(Schema):
    GameDate = fields.DateTime(format="%Y-%m-%d")


class ScheduleOutputSchema(Schema):
    GAME_ID = fields.String()
    HOME_TEAM_ID = fields.Int()
    HOME_ABBREVIATION = fields.String()
    VISITOR_TEAM_ID = fields.Int()
    VISITOR_ABBREVIATION = fields.String()
    HOME_PTS = fields.Int()
    VISITOR_PTS = fields.Int()


class GameQueryArgsSchema(Schema):
    GameDate = fields.DateTime(format="%Y-%m-%d")
    GameID = fields.String()


class MomentsOutputSchema(Schema):
    TIME = fields.Int()
    PERIOD = fields.Int()
    PCTIMESTRING = fields.String()
    SCOREMARGIN = fields.Int()
    SURV_PROB = fields.Float()
    SURV_PROB_CHANGE = fields.Float()
    DESCRIPTION = fields.String()
    PLAYER1_ID = fields.Int()


class PlayByPlayOutputSchema(Schema):
    TIME = fields.Int()
    WIN_PROB = fields.Float()
    SCOREMARGIN = fields.Int()


class TeamBoxScoreOutputSchema(Schema):
    TEAM_ID = fields.Int()
    FG_PCT = fields.Float()
    FGM = fields.Int()
    FGA = fields.Int()
    FG3_PCT = fields.Float()
    FG3M = fields.Int()
    FG3A = fields.Int()
    FT_PCT = fields.Float()
    FTM = fields.Int()
    FTA = fields.Int()
    PTS = fields.Int()
    REB = fields.Int()
    OREB = fields.Int()
    DREB = fields.Int()
    AST = fields.Int()
    STL = fields.Int()
    BLK = fields.Int()
    TO = fields.Int()


class PlayerBoxScoreOutputSchema(Schema):
    TEAM_ID = fields.Int()
    TEAM_ABBREVIATION = fields.String()
    PLAYER_ID = fields.Int()
    PLAYER_NAME = fields.String()
    MIN = fields.String()
    IMPACT = fields.Float()
    FG_PCT = fields.Float()
    FGM = fields.Int()
    FGA = fields.Int()
    FG3_PCT = fields.Float()
    FG3M = fields.Int()
    FG3A = fields.Int()
    FT_PCT = fields.Float()
    FTM = fields.Int()
    FTA = fields.Int()
    PTS = fields.Int()
    REB = fields.Int()
    AST = fields.Int()
    STL = fields.Int()
    BLK = fields.Int()
    TO = fields.Int()


class BoxScoreOutputSchema(Schema):
    TEAM = fields.Nested(TeamBoxScoreOutputSchema(many=True))
    PLAYER = fields.Nested(PlayerBoxScoreOutputSchema(many=True))
