# %%
from datetime import timedelta

import polars as pl

from power_of_10 import PowerOf10

murray = PowerOf10().get_athlete_by_id(1114055)

parkrun_results = sorted(
    [
        {
            "date": p.date.strftime("%Y-%m-%d"),
            "event_no": p.meeting.split(" ")[-1],
            "time": timedelta(
                minutes=int(p.performance.split(":")[0]),
                seconds=int(p.performance.split(":")[1]),
            ).seconds,
        }
        for p in murray.all_performances
        if p.event_name == "parkrun" and "Eglinton" in p.meeting
    ],
    key=lambda x: x["event_no"],
)

for r in parkrun_results:
    print(r["date"], r["event_no"], r["time"])

df = pl.DataFrame(parkrun_results)
print(df)

df.plot.line(x="date", y="time").properties(width=1200, height=500, title="Eglinton Parkrun").configure_scale(zero=False)
# %%
