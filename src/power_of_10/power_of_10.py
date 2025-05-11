import httpx
from bs4 import BeautifulSoup

from power_of_10 import (
    Athlete,
    AthleteNotFoundException,
    html_parser,
)


class PowerOf10:
    def __init__(self):
        self._root_url = "https://www.thepowerof10.info"

    def get_athlete_by_id(self, athlete_id: int) -> Athlete:
        """Get an athlete's details by their athleteid."""
        url = f"{self._root_url}/athletes/profile.aspx?athleteid={athlete_id}"
        html = httpx.get(url, verify=False).text

        if "Profile not found" in html:
            err_msg = f"Profile not found for athleteid = {athlete_id}"
            raise AthleteNotFoundException(err_msg)

        soup = BeautifulSoup(html, "html.parser")

        return html_parser._get_athlete(soup)


