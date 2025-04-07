from pydantic import BaseModel

class Athlete(BaseModel):
    name: str
    club: str
    gender: str
    age_group: str
    county: str | None
    region: str 
    nation: str