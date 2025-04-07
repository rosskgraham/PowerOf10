from bs4 import BeautifulSoup
import httpx
from power_of_10.models.athlete import Athlete


class PowerOf10:
    def __init__(self):
        pass

    def get_athlete_by_id(self, athlete_id: int):
        """Get an athlete's details by their athleteid."""
        url = f"https://www.thepowerof10.info/athletes/profile.aspx?athleteid={athlete_id}"

        html = httpx.get(url)

        soup = BeautifulSoup(html.text, "html.parser")

        athlete_name = (
            soup.find("tr", {"class": "athleteprofilesubheader"})
            .find("td")
            .find("h2")
            .text.strip()
        )

        athlete_details = (
            soup.find("div", {"id": "cphBody_pnlAthleteDetails"})
            .find_all("table")[1]
            .find("table")
            .find_all("tr")
        )
        club = athlete_details[0].find_all("td")[1].text.strip()
        gender = athlete_details[1].find_all("td")[1].text.strip()
        age_group = athlete_details[2].find_all("td")[1].text.strip()
        county = athlete_details[3].find_all("td")[1].text.strip()
        region = athlete_details[4].find_all("td")[1].text.strip()
        nation = athlete_details[5].find_all("td")[1].text.strip()

        athlete = Athlete(
            name=athlete_name,
            club=club,
            gender=gender,
            age_group=age_group,
            county=county,
            region=region,
            nation=nation,
        )
        return athlete
