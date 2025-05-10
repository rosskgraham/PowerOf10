from datetime import datetime

from pydantic import BaseModel

from .event import EventName


class BestPerformance(BaseModel):
    event_name: EventName
    personal_best: str
    year_bests: dict[int, str]


class Performance(BaseModel):
    event_name: EventName
    performance: str
    indoor: str
    position: str
    meeting: str
    date: datetime


class Athlete(BaseModel):
    name: str
    club: str
    gender: str
    age_group: str
    county: str | None
    region: str
    nation: str
    best_performances: dict[EventName, BestPerformance] | None
    all_performances: list[Performance] | None
