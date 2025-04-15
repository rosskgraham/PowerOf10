import httpx
from bs4 import BeautifulSoup

from power_of_10 import (
    Athlete,
    AthleteNotFoundException,
    BestKnownPerformances,
    EventPerfomance,
    html_parser,
    string_utils,
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

        athlete = html_parser.get_athlete_details(soup)

        best_performance_rows = (
            soup.find("div", {"id": "cphBody_divBestPerformances"})
            .find("table")
            .find_all("tr")
        )

        th, events = [], {}
        for tr in best_performance_rows:
            if not th and tr.find("td").text == "Event":
                th = [th.text for th in tr.find_all("td")]
            elif tr.find("td").text != "Event" and th:
                td = [td.text for td in tr.find_all("td")]

                event = td[0]
                year_bests = [
                    {"year": th_td[0], "result": th_td[1]}
                    for th_td in list(zip(th[2:], td[2:], strict=True))
                    if th_td[0] != "Event"  # Lose the repeated Event Name column
                ]
                personal_best = td[1]
                event_name = string_utils.parse_event_code(event).event_name
                events[event_name] = EventPerfomance(
                    event_name=event_name,
                    best_known_performances=BestKnownPerformances(
                        personal_best=personal_best,
                        year_best={
                            result["year"]: result["result"] for result in year_bests
                        },
                    ),
                )
        athlete.events = events
        
        return athlete
