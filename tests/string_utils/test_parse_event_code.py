import pytest

from power_of_10.models.event import Event
from power_of_10.string_utils import parse_event_code


@pytest.mark.parametrize(
    "event,expected",
    [
        pytest.param("60", Event(event_code="60"), id="60"),
        pytest.param("75", Event(event_code="75"), id="75"),
        pytest.param("80", Event(event_code="80"), id="80"),
        pytest.param("100", Event(event_code="100"), id="100"),
        pytest.param("150", Event(event_code="150"), id="150"),
        pytest.param("200", Event(event_code="200"), id="200"),
        pytest.param("600", Event(event_code="600"), id="600"),
        pytest.param("800", Event(event_code="800"), id="800"),
        pytest.param("1200", Event(event_code="1200"), id="1200"),
        pytest.param("1500", Event(event_code="1500"), id="1500"),
        *[
            pytest.param(
                f"60H{age}{sex}",
                Event(event_code="60H", age_group=age, sex=sex),
                id=f"60H{age}{sex}",
            )
            for age in ["U13", "U15", "U17", "U20"]
            for sex in ["M", "W"]
        ],
        *[
            pytest.param(
                f"75H{age}{sex}",
                Event(event_code="75H", age_group=age, sex=sex),
                id=f"75H{age}{sex}",
            )
            for age in ["U13", "U15", "U17", "U20"]
            for sex in ["M", "W"]
        ],
        pytest.param("HJ", Event(event_code="HJ"), id="HJ"),
        pytest.param("LJ", Event(event_code="LJ"), id="LJ"),
        pytest.param("SP3K", Event(event_code="SP3K"), id="SP3K"),
        pytest.param(
            "SP2.72K",
            Event(event_code="SP2.72K"),
            id="SP2.72K",
        ),
        pytest.param("JT400", Event(event_code="JT400"), id="JT400"),
        *[
            pytest.param(
                f"Pen{age}{sex}",
                Event(event_code="Pen", age_group=age, sex=sex),
                id=f"PenEvent{age}{sex}",
            )
            for age in ["U13", "U15", "U17", "U20"]
            for sex in ["M", "W"]
        ],
        *[
            pytest.param(
                f"PenI{age}{sex}",
                Event(event_code="PenI", age_group=age, sex=sex),
                id=f"PenI{age}{sex}",
            )
            for age in ["U13", "U15", "U17", "U20"]
            for sex in ["M", "W"]
        ],
        pytest.param("1K", Event(event_code="1K"), id="1K"),
        pytest.param("1KNAD", Event(event_code="1KNAD"), id="1KNAD"),
        pytest.param(
            "1.2KXC",
            Event(event_code="1.2KXC"),
            id="1.2KXC",
        ),
        pytest.param(
            "1.3KXC",
            Event(event_code="1.3KXC"),
            id="1.3KXC",
        ),
        pytest.param(
            "1.5KXCL",
            Event(event_code="1.5KXCL"),
            id="1.5KXCL",
        ),
        pytest.param(
            "2.5KXCL",
            Event(event_code="2.5KXCL"),
            id="2.5KXCL",
        ),
        pytest.param(
            "2.7KXC",
            Event(event_code="2.7KXC"),
            id="2.7KXC",
        ),
        pytest.param("3KNAD", Event(event_code="3KNAD"), id="3KNAD"),
        pytest.param(
            "3.2KXC",
            Event(event_code="3.2KXC"),
            id="3.2KXC",
        ),
        pytest.param(
            "parkrun",
            Event(event_code="parkrun"),
            id="parkrun",
        ),
        pytest.param(
            "foo",
            Event(event_code="foo"),
            id="foo",
        ),
    ],
)
def test_parse_event_code(event, expected):
    """Test event code parsing returns the expeced Event model."""
    assert parse_event_code(event) == expected
