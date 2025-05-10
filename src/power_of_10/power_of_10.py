import httpx
from bs4 import BeautifulSoup

from power_of_10 import (
    Athlete,
    AthleteNotFoundException,
    html_parser,
)


class PowerOf10:
    def __init__(self):
        pass

    def get_athlete_by_id(self, athlete_id: int) -> Athlete:
        """Get an athlete's details by their athleteid."""
        url = f"https://www.thepowerof10.info/athletes/profile.aspx?athleteid={athlete_id}"
        html = httpx.get(url, verify=False).text

        if "Profile not found" in html:
            err_msg = f"Profile not found for athleteid = {athlete_id}"
            raise AthleteNotFoundException(err_msg)

        soup = BeautifulSoup(html, "html.parser")

        athlete = html_parser._get_athlete_details(soup)

        athlete.best_performances = html_parser._get_best_performances(soup)

        athlete.all_performances = html_parser._get_all_performances(soup)

        return athlete


