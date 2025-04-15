from bs4 import BeautifulSoup

from power_of_10.models.athlete import Athlete

from .po10_exceptions import (
    AthleteDetailsNotFoundException,
    AthleteNameNotFoundException,
)


def get_athlete_details(soup: BeautifulSoup) -> Athlete:
    try:
        athlete_name = (
            soup.find("tr", {"class": "athleteprofilesubheader"})
            .find("td")
            .find("h2")
            .text.strip()
        )
    except AttributeError as err:
        raise AthleteNameNotFoundException("Athlete name not found.") from err

    try:
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
        
        return Athlete(
            name=athlete_name,
            club=club,
            gender=gender,
            age_group=age_group,
            county=county,
            region=region,
            nation=nation,
            events={},
        )
    except AttributeError as err:
        raise AthleteDetailsNotFoundException("Athlete details not found.") from err
    except IndexError as err:
        raise AthleteDetailsNotFoundException("Athlete details not found.") from err
