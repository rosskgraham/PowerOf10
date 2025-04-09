from bs4 import BeautifulSoup
import httpx
from power_of_10.models.athlete import Athlete


class PowerOf10:
    def __init__(self):
        self._page_html = None
        pass

    def _get_page_html(self, url: str) -> str:
        self._page_html = httpx.get(url).text
        return self._page_html
    
    def get_athlete_by_id(self, athlete_id: int):
        """Get an athlete's details by their athleteid."""
        url = f"https://www.thepowerof10.info/athletes/profile.aspx?athleteid={athlete_id}"
        html = self._get_page_html(url)

        soup = BeautifulSoup(html, "html.parser")

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

        best_performances_table = (
            soup.find("div", {"id": "cphBody_divBestPerformances"})
            .find("table")
        )
        best_performance_rows = best_performances_table.find_all("tr")

        headers, data_rows = [],  []
        for tr in best_performance_rows:
            if tr.find("td").text == "Event":
                headers = tr.find_all("td")
            elif tr.find("td").text != "Event" and headers:
                data_rows.append(tr.find_all("td"))
            
        print([[td.text for td in tr] for tr in data_rows])
        return athlete
