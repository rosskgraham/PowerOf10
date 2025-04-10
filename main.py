import polars as pl
import yaml
from alive_progress import alive_it

from power_of_10 import Athlete, PowerOf10


def main():
    with open("config.yml", "r") as config_file:
        config: dict[dict[int, str]] = yaml.safe_load(config_file.read())

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
                "name": athlete.name,
                **{
                    k: v.best_known_performances.personal_best
                    for k, v in athlete.events.items()
                },
            }
        )
    df = pl.DataFrame(personal_bests).fill_null("")
    df.columns = [config["events"].get(e,{"name":e})["name"] for e in df.columns]
    with pl.Config(tbl_cols=len(df.columns)):
        print(df.sort(by="name"))
    # df.write_csv("C:/Temp/po10.csv")


if __name__ == "__main__":
    main()
