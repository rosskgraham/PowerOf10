from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from power_of_10.html_parser import _get_athlete
from power_of_10.po10_exceptions import (
    AthleteDetailsNotFoundException,
    AthleteNameNotFoundException,
)


@pytest.fixture
def good_soup() -> BeautifulSoup:
    html = (Path(__file__).parent.parent / "mock_data" / "athlete_profiles" / "1114055.html").read_text()
    return BeautifulSoup(html, "html.parser")


@pytest.fixture
def bad_soup_no_details() -> BeautifulSoup:
    html = (Path(__file__).parent.parent / "mock_data" / "athlete_profiles" / "no_athlete_details.html").read_text()
    return BeautifulSoup(html, "html.parser")


@pytest.fixture
def bad_soup_no_name() -> BeautifulSoup:
    html = (Path(__file__).parent.parent / "mock_data" / "athlete_profiles" / "no_athlete_name.html").read_text()
    return BeautifulSoup(html, "html.parser")


def test_get_athlete(good_soup):
    athlete = _get_athlete(good_soup)
    assert athlete.name == "Murray Graham"
    assert athlete.club == "North Ayrshire"


def test_get_athlete_name_not_found(bad_soup_no_name):
    with pytest.raises(AthleteNameNotFoundException) as err:
        _ = _get_athlete(bad_soup_no_name)
    assert err.match("Athlete name not found.")


def test_get_athlete_details_not_found(bad_soup_no_details):
    with pytest.raises(AthleteDetailsNotFoundException) as err:
        _ = _get_athlete(bad_soup_no_details)
    assert err.match("Athlete details not found.")
