from pathlib import Path

import polars as pl
import xlsxwriter
from alive_progress import alive_it

from power_of_10 import Athlete, PowerOf10, get_config

temp_path = Path().home() / "OneDrive" / "Documents" / "Temp"
config = get_config("config_naac.yml")


def main():
    po10 = PowerOf10()
    athletes: list[Athlete] = []
    for athlete_id, athlete_name in (bar := alive_it(config.get("athletes").items())):
        bar.text = athlete_name
        athletes.append(po10.get_athlete_by_id(athlete_id))

    # Event PBs
    personal_bests = []
    for athlete in athletes:
        personal_bests.append(
            {
                "Name": athlete.name,
                **{
                    e: athlete.best_performances[e].personal_best
                    for e in athlete.best_performances
                },
            }
        )
    personal_bests_df = pl.DataFrame(personal_bests).fill_null("")
    cols = sorted([c for c in personal_bests_df.columns if c != "Name"])
    personal_bests_df = personal_bests_df.select("Name", *cols).sort("Name")

    # Event Year Bests
    year_bests = []
    for athlete in athletes:
        year_bests.extend(
            [
                {
                    "Name": athlete.name,
                    "Event": event,
                    "Year": year,
                    "Result": year_best if year_best[-1] != "i" else year_best[:-1],
                    "Indoor": "Y" if year_best[-1] == "i" else "",
                }
                for event, best_performances in athlete.best_performances.items()
                for year, year_best in best_performances.year_bests.items()
                if year_best != ""
            ]
        )
    year_bests_df = pl.DataFrame(year_bests).fill_null("").sort("Name", "Event", "Year")

    # All Performances
    all_performances = []
    for athlete in athletes:
        all_performances.extend(
            [
                {
                    "Name": athlete.name,
                    "Event": performance.event_name,
                    "Date": performance.date,
                    "Year": performance.date.year,
                    "Performance": performance.performance,
                    "Indoor": performance.indoor,
                    "Position": performance.position,
                    "Meeting": performance.meeting,
                }
                for performance in athlete.all_performances
            ]
        )
    all_performances_df = (
        pl.DataFrame(all_performances).fill_null("").sort("Name", "Event", "Date")
    )

    (temp_path / "PowerOf10.xlsx").unlink(missing_ok=True)

    # Write data to Excel Workbook with a Worksheet per dataframe
    with xlsxwriter.Workbook(temp_path / "PowerOf10.xlsx") as workbook:
        personal_bests_df.write_excel(
            workbook=workbook,
            worksheet="PBs",
            autofit=True,
            table_style="Table Style Medium 5",
            table_name="PBs",
            freeze_panes="B2",
        )
        year_bests_df.write_excel(
            workbook=workbook,
            worksheet="Year Bests",
            autofit=True,
            table_style="Table Style Medium 5",
            table_name="YearBests",
            column_formats={"Year": "0"},
            freeze_panes="B2",
        )
        all_performances_df.write_excel(
            workbook=workbook,
            worksheet="All Performances",
            autofit=True,
            table_style="Table Style Medium 5",
            table_name="AllPerformances",
            freeze_panes="B2",
        )


if __name__ == "__main__":
    main()
