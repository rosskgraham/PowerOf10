import pytest
from bs4 import BeautifulSoup

from power_of_10.html_parser import get_athlete_details
from power_of_10.po10_exceptions import (
    AthleteDetailsNotFoundException,
    AthleteNameNotFoundException,
)


@pytest.fixture
def good_soup() -> BeautifulSoup:
    html = """
        <html>
            <table width="100%" cellspacing="0" cellpadding="0">
                <tr class="athleteprofilesubheader">
                    <td>
                        <h2>Athlete Name</h2>
                    </td>
                    <td style="text-align: right">
                        <b>
                            <a id="cphBody_lnkEditAthlete" href="/submit/notify.aspx?athleteid=123&amp;returnto=%2fathletes%2fprofile.aspx%3fathleteid%3d123">
                                <img src="/images/pot/email.gif" alt="notify us of amends"/>
                            </a>
                        </b>
                        &nbsp;
                    </td>
                </tr>
            </table>
            <div id="cphBody_pnlAthleteDetails">
                <table width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                        <td style="font-size: 2pt">&nbsp;</td>
                    </tr>
                </table>
                <table width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                        <td width="50%" valign="top">
                            <table cellspacing="0" cellpadding="2">
                                <tr>
                                    <td>
                                        <b>Club:</b>
                                    </td>
                                    <td>My Club</td>
                                </tr>
                                <tr>
                                    <td>
                                        <b>Gender:</b>
                                    </td>
                                    <td>Male</td>
                                </tr>
                                <tr>
                                    <td>
                                        <b>Age Group:</b>
                                    </td>
                                    <td>U13</td>
                                </tr>
                                <tr>
                                    <td>
                                        <b>County:</b>
                                    </td>
                                    <td></td>
                                </tr>
                                <tr>
                                    <td>
                                        <b>Region:</b>
                                    </td>
                                    <td>Scotland</td>
                                </tr>
                                <tr>
                                    <td>
                                        <b>Nation:</b>
                                    </td>
                                    <td>Scotland</td>
                                </tr>
                            </table>
                        </td>
                        <td width="50%" valign="top">
                            <table cellspacing="0" cellpadding="2">
                                <tr>
                                    <td>
                                        <b>Lead Coach:</b>
                                    </td>
                                    <td>Unknown</td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </div>
        </html>
    """
    return BeautifulSoup(html, "html.parser")


@pytest.fixture
def bad_soup_no_details() -> BeautifulSoup:
    html = """
        <html>
            <table width="100%" cellspacing="0" cellpadding="0">
                <tr class="athleteprofilesubheader">
                    <td>
                        <h2>Athlete Name</h2>
                    </td>
                    <td style="text-align: right">
                        <b>
                            <a id="cphBody_lnkEditAthlete" href="/submit/notify.aspx?athleteid=123&amp;returnto=%2fathletes%2fprofile.aspx%3fathleteid%3d123">
                                <img src="/images/pot/email.gif" alt="notify us of amends"/>
                            </a>
                        </b>
                        &nbsp;
                    </td>
                </tr>
            </table>
            <div id="cphBody_pnlAthleteDetails">
                <table width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                        <td style="font-size: 2pt">&nbsp;</td>
                    </tr>
                </table>
            </div>
        </html>
    """
    return BeautifulSoup(html, "html.parser")


@pytest.fixture
def bad_soup_no_name() -> BeautifulSoup:
    html = """
        <table width="100%" cellspacing="0" cellpadding="0">
            <tr class="athleteprofilesubheader">
                <td>
                    <span>foo</span>
                </td>
                <td style="text-align: right">
                    <b>
                        <a id="cphBody_lnkEditAthlete" href="/submit/notify.aspx?athleteid=123&amp;returnto=%2fathletes%2fprofile.aspx%3fathleteid%3d123">
                            <img src="/images/pot/email.gif" alt="notify us of amends"/>
                        </a>
                    </b>
                    &nbsp;
                </td>
            </tr>
        </table>
    """
    return BeautifulSoup(html, "html.parser")


def test_get_athlete_details(good_soup):
    athlete = get_athlete_details(good_soup)
    assert athlete.name == "Athlete Name"
    assert athlete.club == "My Club"


def test_get_athlete_details_name_not_found(bad_soup_no_name):
    with pytest.raises(AthleteNameNotFoundException) as err:
        _ = get_athlete_details(bad_soup_no_name)
    assert err.match("Athlete name not found.")


def test_get_athlete_details_details_not_found(bad_soup_no_details):
    with pytest.raises(AthleteDetailsNotFoundException) as err:
        _ = get_athlete_details(bad_soup_no_details)
    assert err.match("Athlete details not found.")
