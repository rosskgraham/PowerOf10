from pydantic import BaseModel

events = {
    "60": {"name": "60m", "type": "track", "result_type": "time"},
    "75": {"name": "75m", "type": "track", "result_type": "time"},
    "80": {"name": "80m", "type": "track", "result_type": "time"},
    "150": {"name": "150m", "type": "track", "result_type": "time"},
    "200": {"name": "200m", "type": "track", "result_type": "time"},
    "600": {"name": "600m", "type": "track", "result_type": "time"},
    "800": {"name": "800m", "type": "track", "result_type": "time"},
    "1200": {"name": "1200m", "type": "track", "result_type": "time"},
    "1500": {"name": "1500m", "type": "track", "result_type": "time"},
    "60H": {"name": "60m Hurdles", "type": "track", "result_type": "time"},
    "75H": {"name": "75m Hurdles", "type": "track", "result_type": "time"},
    "HJ": {"name": "High Jump", "type": "field", "result_type": "float"},
    "LJ": {"name": "Long Jump", "type": "field", "result_type": "float"},
    "SP2K": {"name": "Shot Putt 2kg", "type": "field", "result_type": "float"},
    "SP2.72K": {"name": "Shot Putt 2.72kg", "type": "field", "result_type": "float"},
    "SP3K": {"name": "Shot Putt 3kg", "type": "field", "result_type": "float"},
    "Pen": {"name": "Pentathlon", "type": "multi", "result_type": "int"},
    "PenI": {"name": "Indoor Pentathlon", "type": "multi", "result_type": "int"},
}


class Event(BaseModel):
    event_code: str
    age_group: str | None = None
    sex: str | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if event_properties := events.get(self.event_code):
            self._event_name = f"{event_properties.get("name")}{f' {self.age_group}' if self.age_group else ''}{f' {self.sex}' if self.sex else ''}"
        else:
            self._event_name = self.event_code
    
    @property
    def event_name(self) ->str:
        return self._event_name