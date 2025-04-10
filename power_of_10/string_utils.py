import re


def parse_event_code(event_code) -> dict[str, str]:
    matches = re.finditer(r"^(60|100|60H)(U13|U15){0,1}([MW]{0,1})$", event_code)

    for match in matches:
        event_code = match.group(1)
        age_group = match.group(2) or "-"
        sex = match.group(3) or "-"
        return {"event_code": event_code, "age_group": age_group, "sex": sex}
    else:
        return None
