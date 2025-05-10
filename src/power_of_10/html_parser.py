from datetime import datetime

from bs4 import BeautifulSoup

from power_of_10 import (
    AthleteDetailsNotFoundException,
    AthleteNameNotFoundException,
    string_utils,
)
from power_of_10.models import (
    Athlete,
    BestPerformance,
    EventName,
    Performance,
)


def _get_athlete_details(soup: BeautifulSoup) -> Athlete:
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
            best_performances={},
            all_performances=[],
        )
    except AttributeError as err:
        raise AthleteDetailsNotFoundException("Athlete details not found.") from err
    except IndexError as err:
        raise AthleteDetailsNotFoundException("Athlete details not found.") from err


def _get_best_performances(soup: BeautifulSoup) -> dict[EventName, BestPerformance]:
    best_performance_rows = (
        soup.find("div", {"id": "cphBody_divBestPerformances"})
        .find("table")
        .find_all("tr")
    )

    th, best_performances = [], {}
    for tr in best_performance_rows:
        if not th and tr.find("td").text.strip() == "Event":
            th = [th.text for th in tr.find_all("td")]
        elif th and tr.find("td").text.strip() != "Event":
            td = [td.text for td in tr.find_all("td")]

            event = string_utils.parse_event_code(td[0])

            year_bests = [
                {"year": year_best[0], "result": year_best[1]}
                for year_best in zip(th[2:], td[2:], strict=True)
                if year_best[0].strip()
                != "Event"  # Lose the repeated Event Name column
            ]
            best_performances[event.event_name] = BestPerformance(
                event_name=event.event_name,
                personal_best=td[1],
                year_bests={result["year"]: result["result"] for result in year_bests},
            )
    return best_performances


def _get_all_performances(soup) -> list[Performance]:
    all_performance_rows = (
        soup.find("div", {"id": "cphBody_pnlPerformances"})
        .find_all("table")[1]
        .find_all("tr")
    )

    rows = []
    for row in all_performance_rows:
        if row.find("td").text.strip() == "Event":
            continue
        elif row.find("td", {"colspan": "12"}):
            continue
        rows.append(row)

    all_performances: list[Performance] = []
    for tr in rows:
        tds = tr.find_all("td")
        all_performances.append(
            Performance(
                **{
                    "event_name": tds[0].text,
                    "performance": tds[1].text,
                    "indoor": "Y" if tds[2].text == "i" else "",
                    "position": tds[5].text,
                    "meeting": tds[10].text,
                    "date": datetime.strptime(tds[11].text, "%d %b %y"),
                }
            )
        )

    return all_performances
