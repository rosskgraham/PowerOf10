import pytest

from power_of_10.models.event import Event
from power_of_10.string_utils import parse_event_code


@pytest.mark.parametrize(
    "event,expected",
    [
        pytest.param("60", Event(event_code="60", age_group="-", sex="-"), id="60"),
        pytest.param("75", {"event_code": "75", "age_group": "-", "sex": "-"}, id="75"),
        pytest.param("80", {"event_code": "80", "age_group": "-", "sex": "-"}, id="80"),
        pytest.param(
            "100", {"event_code": "100", "age_group": "-", "sex": "-"}, id="100"
        ),
        pytest.param(
            "150", {"event_code": "150", "age_group": "-", "sex": "-"}, id="150"
        ),
        pytest.param(
            "200", {"event_code": "200", "age_group": "-", "sex": "-"}, id="200"
        ),
        pytest.param(
            "600", {"event_code": "600", "age_group": "-", "sex": "-"}, id="600"
        ),
        pytest.param(
            "800", {"event_code": "800", "age_group": "-", "sex": "-"}, id="800"
        ),
        pytest.param(
            "1200", {"event_code": "1200", "age_group": "-", "sex": "-"}, id="1200"
        ),
        pytest.param(
            "1500", {"event_code": "1500", "age_group": "-", "sex": "-"}, id="1500"
        ),
        *[
            pytest.param(
                f"60H{age}{sex}",
                {"event_code": "60H", "age_group": age, "sex": sex},
                id=f"60H{age}{sex}",
            )
            for age in ["U13", "U15", "U17", "U20"]
            for sex in ["M", "W"]
        ],
        *[
            pytest.param(
                f"75H{age}{sex}",
                {"event_code": "75H", "age_group": age, "sex": sex},
                id=f"75H{age}{sex}",
            )
            for age in ["U13", "U15", "U17", "U20"]
            for sex in ["M", "W"]
        ],
        pytest.param("HJ", {"event_code": "HJ", "age_group": "-", "sex": "-"}, id="HJ"),
        pytest.param("LJ", {"event_code": "LJ", "age_group": "-", "sex": "-"}, id="LJ"),
        pytest.param(
            "SP3K", {"event_code": "SP3K", "age_group": "-", "sex": "-"}, id="SP3K"
        ),
        pytest.param(
            "SP2.72K",
            {"event_code": "SP2.72K", "age_group": "-", "sex": "-"},
            id="SP2.72K",
        ),
        pytest.param(
            "JT400", {"event_code": "JT400", "age_group": "-", "sex": "-"}, id="JT400"
        ),
        *[
            pytest.param(
                f"Pen{age}{sex}",
                {"event_code": "Pen", "age_group": age, "sex": sex},
                id=f"Pen{age}{sex}",
            )
            for age in ["U13", "U15", "U17", "U20"]
            for sex in ["M", "W"]
        ],
        *[
            pytest.param(
                f"PenI{age}{sex}",
                {"event_code": "PenI", "age_group": age, "sex": sex},
                id=f"PenI{age}{sex}",
            )
            for age in ["U13", "U15", "U17", "U20"]
            for sex in ["M", "W"]
        ],
        pytest.param("1K", {"event_code": "1K", "age_group": "-", "sex": "-"}, id="1K"),
        pytest.param(
            "1KNAD", {"event_code": "1KNAD", "age_group": "-", "sex": "-"}, id="1KNAD"
        ),
        pytest.param(
            "1.2KXC",
            {"event_code": "1.2KXC", "age_group": "-", "sex": "-"},
            id="1.2KXC",
        ),
        pytest.param(
            "1.3KXC",
            {"event_code": "1.3KXC", "age_group": "-", "sex": "-"},
            id="1.3KXC",
        ),
        pytest.param(
            "1.5KXCL",
            {"event_code": "1.5KXCL", "age_group": "-", "sex": "-"},
            id="1.5KXCL",
        ),
        pytest.param(
            "2.5KXCL",
            {"event_code": "2.5KXCL", "age_group": "-", "sex": "-"},
            id="2.5KXCL",
        ),
        pytest.param(
            "2.7KXC",
            {"event_code": "2.7KXC", "age_group": "-", "sex": "-"},
            id="2.7KXC",
        ),
        pytest.param(
            "3KNAD", {"event_code": "3KNAD", "age_group": "-", "sex": "-"}, id="3KNAD"
        ),
        pytest.param(
            "3.2KXC",
            {"event_code": "3.2KXC", "age_group": "-", "sex": "-"},
            id="3.2KXC",
        ),
        pytest.param(
            "parkrun",
            {"event_code": "parkrun", "age_group": "-", "sex": "-"},
            id="parkrun",
        ),
        pytest.param(
            "foo",
            Event(event_code="foo", age_group="-", sex="-"),
            id="foo",
        ),
    ],
)
def test_parse_event_code(event, expected):
    p = parse_event_code(event)
    assert parse_event_code(event) == expected
