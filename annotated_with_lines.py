""" messing around with annotations """
import json
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# get weather data
with open("json_files/dubai.json", "r") as file:
    weather = json.load(file)


# prepare the figure
fig, ax = plt.subplots(layout="constrained")

# x represents the dates
x = list(map(lambda x: datetime.strptime(x, "%Y-%m-%d"), weather["time"]))
cdf = mdates.ConciseDateFormatter(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(cdf)

y = weather["temperature_2m_max"]

ax.plot_date(x, y, label="Temperature", linestyle="-")

ax.set_xlabel("Date", size=12, labelpad=5)
ax.set_ylabel("Temperature")
plt.title("Temps and dates")

lowest = min(y)
lowest_date = weather["time"][y.index(lowest)]
lowest_date = datetime.strptime(lowest_date, "%Y-%m-%d")

for i, v in zip(x, y):
    ax.annotate(
        str(v),
        xy=(mdates.date2num(i), v),
        xytext=(-2, 3),
        textcoords="offset points",
    )

# here we add the vertical line
plt.axvline(lowest_date, color='red', linestyle='--', linewidth=1)

# here we add the horizontal line
plt.axhline(lowest, color='orange', linestyle='--', linewidth=1)

fig.savefig("saved_plots\\annotated_with_lines.png")
plt.show()
