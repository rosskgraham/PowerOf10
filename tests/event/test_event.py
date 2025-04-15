import pytest

from power_of_10.models.event import Event


@pytest.mark.parametrize(
    "event,expected_event_name",
    [
        pytest.param({"event_code":"60"}, "60m", id="60m"),
        pytest.param({"event_code":"60", "age":None, "sex":None}, "60m", id="60m with Nones"),
        pytest.param({"event_code":"60H", "age_group":"U13", "sex":"M"}, "60m Hurdles U13 M", id="60HU13M"),
    ]
)
def test_event_name(event,expected_event_name):
    assert Event(**event).event_name == expected_event_name