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
