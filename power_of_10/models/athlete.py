from pydantic import BaseModel


class BestKnownPerformances(BaseModel):
    personal_best: str
    year_best: dict[int, str]


class Event(BaseModel):
    event_name: str
    best_known_performances: BestKnownPerformances


class Athlete(BaseModel):
    name: str
    club: str
    gender: str
    age_group: str
    county: str | None
    region: str
    nation: str
    events: dict[str, Event] | None
