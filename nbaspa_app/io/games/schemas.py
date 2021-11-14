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
