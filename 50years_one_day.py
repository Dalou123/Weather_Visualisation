"""
This code creates a plot that showcases the max temperature on the 1st day of
 each month in beirut over the past 53 years.
"""

import json
from datetime import datetime

import matplotlib.pyplot as plt

from variables import allowed_weather_values


def get_value_per_month(weather_dict: dict, weather_string: str):
    """
    Starting from a dictionary that contains the historical weather data for
    the past x years, choose only the values recorded on the first day of each
    month. Save the weather data specified in the value argument along with
    the corresponding month and year.

    :param dict weather: weather data as returned from the funtion
                         get_historical_weather() in main.py
    :param str  value: the name of the weather data to be extracted (specified
                       in variables.py)

    :return 3 separate lists: years, months, value

    """

    if weather_string not in allowed_weather_values:
        print("Invalid weather string!")
        return

    years = []
    months = []
    data = []

    for i, v in enumerate(weather_dict["time"]):
        if v.endswith("01"):
            my_date = datetime.strptime(v, "%Y-%m-%d")

            years.append(my_date.year)
            months.append(my_date.month)
            data.append(weather_dict[weather_string][i])

    return years, months, data


# get the weather data from the saved file (file was generated using the
# function get_historical_weather() in main.py)
with open("json_files/beirut_50years.json", "r") as file:
    weather = json.load(file)


year, month, max_temp = get_value_per_month(weather, "temperature_2m_max")
# _, _, rain = get_temps(weather, 'rain_sum')

# create a figure with 1 ax and a scatter plot
fig, ax = plt.subplots(figsize=(8, 8))
pc = ax.scatter(
    x=month,
    y=year,
    c=max_temp,
    cmap="rainbow",
    # s=rain,        # big circle if rain, none if no rain
)

# Customize plot
fig.colorbar(pc, ax=ax, extend="both")

ax.set_xlabel("months", fontsize=12, weight="bold")
ax.set_ylabel("years", fontsize=12, weight="bold")
ax.set_title(
    "Temperature on the 1st of each month from 1970 to 2023",
    fontsize=15,
    weight="bold"
)

# save plot then display it
plt.savefig("saved_plots\\50years_one_day.png")
plt.show()
