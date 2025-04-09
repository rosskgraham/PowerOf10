from pathlib import Path

import httpx
import pytest

from power_of_10 import AthleteNotFoundException, PowerOf10

"""
# Murray Graham https://www.thepowerof10.info/athletes/profile.aspx?athleteid=1114055
{
    "name": "Murray Graham",
    "club": "North Ayrshire",
    "gender": "Male",
    "age_group": "U13",
    "county": "",
    "region": "Scotland",
    "nation": "Scotland"
}
"""


def mock_httpx_get(url: str, verify: bool = True) -> httpx.Response:
    """Mock httpx Response with static HTML from file"""
    athelete_id = url.split("=")[1]
    mock_athlete_profile_path = (
        Path(__file__).parent.parent
        / "mock_data"
        / "athlete_profiles"
        / f"{athelete_id}.html"
    )
    mock_athlete_not_found_path = (
        Path(__file__).parent.parent
        / "mock_data"
        / "athlete_profiles"
        / "not_found.html"
    )
    try:
        with open(mock_athlete_profile_path, "r") as html_file:
            html = html_file.read()
        return httpx.Response(text=html, status_code=200)
    except FileNotFoundError:
        # Unknown athlete, return profile not found page
        with open(mock_athlete_not_found_path, "r") as html_file:
            html = html_file.read()
        return httpx.Response(text=html, status_code=200)


@pytest.fixture
def mock_request_fixture(request, monkeypatch) -> None:
    """Monkeypatch httpx.get with mock file based response"""
    if request.config.getoption("--use-mock"):
        print(f"\nUsing mock response for {request.node.name}")
        monkeypatch.setattr("httpx.get", mock_httpx_get)
    else:
        print(f"\nUsing thepowerof10.info response for {request.node.name}")


def test_get_athlete_by_id(mock_request_fixture):
    """Test a known good athlete id returns expected athlete details"""
    po10 = PowerOf10()
    athlete = po10.get_athlete_by_id(1114055)
    assert athlete.name == "Murray Graham"
    assert athlete.club == "North Ayrshire"
    assert athlete.gender == "Male"
    assert athlete.age_group == "U13"
    assert athlete.county == ""
    assert athlete.region == "Scotland"
    assert athlete.nation == "Scotland"


def test_get_athlete_by_id_invalid(mock_request_fixture):
    """Test a known non existent athlete id returns profile not found page"""
    po10 = PowerOf10()

    with pytest.raises(AthleteNotFoundException) as e:
        _ = po10.get_athlete_by_id(999999999)
    assert e.match("Profile not found for athleteid = 999999999")
