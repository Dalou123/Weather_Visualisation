"""
Plotting the weather data in dubai for a duration of 15 days.
Here I am trying out a few functionalities of the matplotlib library by
implementing a figure that contains 4 axes where each ax is of a different
type. I'm also adding multiple values to a single plot, customizing
colors, labels and line styles.
"""
import json
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from variables import customizations as info
from variables import wind_direction_guide


def helper(ax, title, x_label, y_label):
    """ set labels for an ax """
    ax.set_title(title, fontsize=20)
    ax.set_xlabel(x_label, size=12, labelpad=10)
    ax.set_ylabel(y_label)


def translate_wind_dir(directions):
    """ translate wind directions from degrees to 8 possible directions """
    ranges = wind_direction_guide.keys()

    for i, v in enumerate(directions):
        for r in ranges:
            if v in r:
                directions[i] = wind_direction_guide[r]

    return directions


# get the weather data from file
with open("json_files/dubai.json", "r") as file:
    weather = json.load(file)

# create figure with 4 axes
fig, axes = plt.subplots(2, 2,
                         figsize=(16, 9),
                         layout="constrained")

(ax1, ax2), (ax3, ax4) = axes

# set labels for the axes and the figure
fig.suptitle("Dubai Weather Data", fontsize=25, color='black',
             bbox=dict(boxstyle='square'))

helper(ax1, "Temperatures", "Date", "Temperature")
helper(ax2, "Wind Speeds", "Date", "Wind Speed")
helper(ax3, "Wind Directions", "", "")
helper(ax4, "Wind Directions", "Direction", "Nb of Days")


# create the x value (used in ax1 and ax2)
date = list(map(lambda x: datetime.strptime(x, "%Y-%m-%d"), weather["time"]))

# Define the date format from string
date_form = DateFormatter("%d-%m")
ax1.xaxis.set_major_formatter(date_form)

# define the date format using autodatelocator
cdf = mdates.ConciseDateFormatter(mdates.AutoDateLocator())
ax2.xaxis.set_major_formatter(cdf)

# translate the values in winddirection from degrees to NESW
wind_dir = "winddirection_10m_dominant"
weather[wind_dir] = translate_wind_dir(weather[wind_dir])

# customize markers and make it reusable
markers = dict(marker='.', markersize=10)

# loop through the weather key anv value pairs, and add the relevan values to
# their corresponding plots
for k, v in weather.items():
    kwargs = dict(color=info[k][0],
                  label=info[k][1],
                  linestyle=info[k][2],
                  **markers)
    args = [date, v]

    if k == "time":
        continue

    elif 'temperature' in k:
        ax1.plot(*args, **kwargs)

        if 'apparent' not in k:
            for i, v in zip(*args):
                ax1.annotate(str(v),
                             xy=(mdates.date2num(i), v),
                             xytext=(0, 5),
                             textcoords='offset points',)

    elif k == 'windspeed_10m_max':
        l2 = ax2.plot(*args, **kwargs)

    elif k == wind_dir:
        # generate lables and directions count for ax3
        labels = set(v)
        directions_count = [v.count(direction) if direction
                            else 0 for direction in labels]

        # draw ax3: pie chart representing wind directions
        ax3.pie(directions_count, labels=labels, autopct="%1.1f%%")

        # generate lables and directions count for ax4
        labels2 = list(wind_direction_guide.values())
        directions_count2 = [v.count(direction) if direction
                             else 0 for direction in labels2]

        # draw ax4: contains a histogram with a plot on top
        ax4.plot(labels2, directions_count2, c='b',
                 alpha=0.5, marker='o', markersize=11)
        ax4.bar(labels2, directions_count2, color='g')


# add another y axis to ax2 and plot it
ax5 = ax2.twinx()
ax5.set_ylabel("Apparent Temperature")
app = "apparent_temperature_mean"
l5 = ax5.plot(date,
              weather[app],
              label=info[app][1],
              linewidth=1.5,
              color=info[app][0],
              linestyle=info[app][2],
              **markers,)
app = 'temperature_2m_mean'
l5 += ax5.plot(date,
               weather[app],
               label=info[app][1],
               linewidth=1.5,
               color=info[app][0],
               linestyle=info[app][2],
               **markers,)


# Add legends
ax1.legend()
ax2.legend(handles=l2 + l5, )

# find the day with the highest wind speed and add it as a note to the chart
wind = max(weather["windspeed_10m_max"])
date_wind = date[weather["windspeed_10m_max"].index(wind)]

ax2.annotate(
    f"Top Speed\n({wind}km/h)\non {date_wind.strftime('%b %d')}",
    xy=(mdates.date2num(date_wind), wind),
    xytext=(-100, -60),
    textcoords='offset points',
    arrowprops=dict(facecolor="black", shrink=0.1,),
    multialignment="center",
    bbox=dict(boxstyle="square", fc="w"),
)

fig.savefig("saved_plots\\plotting_dubai.png")
plt.show()
