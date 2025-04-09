from power_of_10 import PowerOf10
import yaml
from alive_progress import alive_it
from power_of_10.models.athlete import Athlete


def main():
    po10 = PowerOf10()
    athletes: list[Athlete] = []
    with open("config.yml", "r") as f:
        config: dict[dict[int, str]] = yaml.safe_load(f.read())

    for athlete_id, athlete_name in (bar:=alive_it(config.get("athletes").items())):
        bar.text=athlete_name
        athletes.append(po10.get_athlete_by_id(athlete_id))

    for athlete in athletes:
        print(athlete.model_dump_json(indent=4))


if __name__ == "__main__":
    main()
