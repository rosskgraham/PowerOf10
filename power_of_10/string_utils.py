import re

from .models.event import Event


def parse_event_code(event_code: str) -> Event:
    """
    Parse the event code into.

    """
    matches = re.finditer(
        (
            r"^(60|75|80|100|150|200|600|800|1200|1500|60H|75H|HJ|LJ|SP3K|SP2.72K|JT400|Pen|PenI|1K|1KNAD|1.2KXC|1.3KXC|1.5KXCL|2.5KXCL|2.7KXC|3KNAD|3.2KXC|parkrun)"
            r"(U13|U15|U17|U20){0,1}"
            r"([MW]{0,1})$"
        ),
        event_code,
    )

    for match in matches:
        event_code_match = match.group(1)
        age_group_match = match.group(2) or None
        sex_match = match.group(3) or None
        return Event(
            event_code=event_code_match,
            age_group=age_group_match,
            sex=sex_match,
        )
    else:
        return Event(
            event_code=event_code,
            age_group=None,
            sex=None,
        )
