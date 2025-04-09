from power_of_10 import PowerOf10
import httpx
from pathlib import Path
import pytest 


@pytest.fixture
def mock_request_fixture(request, monkeypatch):
    if request.config.getoption("--use-mock"):
        print("Using mock response")
        monkeypatch.setattr("httpx.get", mock_httpx_get_athlete)
        
def mock_httpx_get_athlete(url: str, verify: bool = True) -> httpx.Response:
    """Mock httpx Response with static HTML from file"""
    athelete_id = url.split("=")[1]
    test_path = (
        Path(__file__).parent.parent
        / "mock_data"
        / "athlete_profiles"
        / f"{athelete_id}.html"
    )
    not_found_path = (
        Path(__file__).parent.parent
        / "mock_data"
        / "athlete_profiles"
        / "not_found.html"
    )
    try:
        with open(test_path, "r") as html_file:
            html = html_file.read()
        return httpx.Response(text=html, status_code=200)
    except FileNotFoundError:
        with open(not_found_path, "r") as html_file:
            html = html_file.read()
        return httpx.Response(text=html, status_code=200)





def test_get_athlete_by_id():
    po10 = PowerOf10()
    athlete = po10.get_athlete_by_id(1114055)
    assert athlete.name == "Murray Graham"
    assert athlete.club == "North Ayrshire"
    assert athlete.gender == "Male"
    assert athlete.age_group == "U13"
    assert athlete.county == ""
    assert athlete.region == "Scotland"
    assert athlete.nation == "Scotland"


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


def test_get_athlete_valid_id(mock_request_fixture):
    """Get a valid athlete id"""
    po10 = PowerOf10()
    html_response = po10._get_page_html(
        "https://www.thepowerof10.info/athletes/profile.aspx?athleteid=1114055"
    )
    assert "Murray Graham" in html_response, "Expected 'Murray Graham' in response"


def test_get_athlete_invalid_id(mock_request_fixture):
    """Get an invalid athlete id"""
    po10 = PowerOf10()
    html_response = po10._get_page_html(
        "https://www.thepowerof10.info/athletes/profile.aspx?athleteid=999999999"
    )
    assert "Profile not found" in html_response, (
        "Expected 'Profile not found' in response"
    )
