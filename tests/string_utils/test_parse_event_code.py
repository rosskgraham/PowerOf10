import pytest

from power_of_10.string_utils import parse_event_code


@pytest.mark.parametrize(
        "event,expected", [("60",{"event_code": "60", "age_group": "-", "sex": "-"}),
                           ("100",{"event_code": "100", "age_group": "-", "sex": "-"}),
                           ("60HU13M",{"event_code": "60H", "age_group": "U13", "sex": "M"})]
)
def test_parse_event_code(event, expected):
    assert parse_event_code(event) == expected