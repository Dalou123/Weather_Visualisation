""" create an animated plot of weather data for every month for the past
 50 years in beirut """

import json
import re
from datetime import datetime

import matplotlib.animation as animation
import matplotlib.pyplot as plt

from variables import allowed_weather_values


def get_this_month_weather(month_nb: int,
                           weather_string: str,
                           weather_dict: dict):
    """
    get the specified weather value for specified month

    :param int month_nb: the number of the month
    :param str  weather_string: the name of the weather data to be extracted
                               (specified in variables.py)
    :param dict weather_dict: weather data as returned from the funtion
                              get_historical_weather() in main.py

    :returns tuple of 4 lists: years, days, temperature, month name

    """

    if weather_string not in allowed_weather_values:
        print("Invalid weather string!")
        return

    years = []
    days = []
    data = []

    for i, v in enumerate(weather_dict['time']):
        # string is "1970-01-31"
        pattern = "\\d{4}-" + str(f"{month_nb:02}") + "-\\d{2}"
        if re.search(pattern, v):
            value = datetime.strptime(v, "%Y-%m-%d")
            days.append(value.day)
            years.append(value.year)
            data.append(weather_dict[weather_string][i])

    month_name = value.strftime("%B")
    return years, days, data, month_name


###############################################################################
# prepare the data
###############################################################################
weather_value = "temperature_2m_max"

# get the weather data from file
with open("json_files/beirut_50years.json", "r") as file:
    weather = json.load(file)

# get the min and max values for the whole dataset
highest = max(weather[weather_value])
lowest = min(weather[weather_value])

# generate the x and y values for the first month
years, days, max_temp, month_name = \
                get_this_month_weather(1, weather_value, weather_dict=weather)

###############################################################################
# create the plot
###############################################################################

# create a figure
fig, ax = plt.subplots(figsize=(8, 8))

# create a bubble chart for the first month
bc = ax.scatter(days, years,
                vmin=lowest, vmax=highest,
                c=max_temp, cmap='rainbow')

# customize plot
fig.colorbar(bc, ax=ax, extend='both')

ax.set_xlim(0, 32)
ax.set_xlabel("Days", fontsize=12, weight='bold')
ax.set_ylabel("Years", fontsize=12, weight='bold')
ax.set_title("Temperatures for January the past 53 years",
             fontsize=15, weight='bold')


###############################################################################
# create animation: METHOD 1 FuncAnimation
###############################################################################

def update(frame):
    """ update the data for each frame of the animation """
    ax.clear()

    # generate the x and y values for the first month
    years, days, max_temp, month_name = \
        get_this_month_weather(frame + 1, weather_value, weather_dict=weather)

    # create a bubble chart for the first month
    bc = ax.scatter(days, years,
                    vmin=lowest, vmax=highest,
                    c=max_temp, cmap='rainbow')

    ax.set_xlim(0, 32)
    ax.set_title(f"Temperatures for {month_name} the past 53 years",
                 fontsize=15, weight='bold')
    return bc


ani = animation.FuncAnimation(fig=fig, func=update, frames=12, interval=300,)

# save plot as gif and mp4 files
ani.save(filename="saved_plots\\temps.gif", writer="pillow")
ani.save(filename="saved_plots\\temps.mp4", writer="ffmpeg")


plt.show()
