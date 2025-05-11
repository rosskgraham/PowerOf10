from datetime import datetime

from bs4 import BeautifulSoup
from bs4.element import Tag

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


def _get_table_cell_text(table: Tag, row_ix: int, td_ix: int) -> str:
    """Get cell text from HTML table object by row and column index."""
    rows = table.find_all("tr")
    try:
        return rows[row_ix].find_all("td")[td_ix].text.strip()
    except KeyError:
        return "Cell text not found."


def _get_athlete(soup: BeautifulSoup) -> Athlete:
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
        athlete_details_table = (
            soup.find("div", {"id": "cphBody_pnlAthleteDetails"})
            .find_all("table")[1]
            .find("table")
        )

        club = _get_table_cell_text(athlete_details_table, 0, 1)
        gender = _get_table_cell_text(athlete_details_table, 1, 1)
        age_group = _get_table_cell_text(athlete_details_table, 2, 1)
        county = _get_table_cell_text(athlete_details_table, 3, 1)
        region = _get_table_cell_text(athlete_details_table, 4, 1)
        nation = _get_table_cell_text(athlete_details_table, 5, 1)

        return Athlete(
            name=athlete_name,
            club=club,
            gender=gender,
            age_group=age_group,
            county=county,
            region=region,
            nation=nation,
            best_performances=_get_best_performances(soup),
            all_performances=_get_all_performances(soup),
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

            event_name = string_utils.parse_event_code(td[0]).event_name

            year_bests = {
                int(year.strip()): best_performance.strip()
                for year, best_performance in zip(th[2:], td[2:], strict=True)
                if year.strip() != "Event"  # Lose the repeated Event Name column
            }
            best_performances[event_name] = BestPerformance(
                event_name=event_name,
                personal_best=td[1],
                year_bests=year_bests,
            )
    return best_performances


def _get_all_performances(soup: BeautifulSoup) -> list[Performance]:
    all_performance_table_rows = (
        soup.find("div", {"id": "cphBody_pnlPerformances"})
        .find_all("table")[1]
        .find_all("tr")
    )

    filtered_rows = [
        row.find_all("td")
        for row in all_performance_table_rows
        if not row.find("td").text.strip() == "Event"
        and not row.find("td", {"colspan": "12"})
    ]

    return [
        Performance(
            **{
                "event_name": tds[0].text.strip(),
                "performance": tds[1].text.strip(),
                "indoor": "Y" if tds[2].text.strip() == "i" else "",
                "position": tds[5].text.strip(),
                "meeting": tds[10].text.strip(),
                "date": datetime.strptime(tds[11].text.strip(), "%d %b %y"),
            }
        )
        for tds in filtered_rows
    ]
