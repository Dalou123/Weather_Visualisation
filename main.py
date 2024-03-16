""" generate a json file that contains all the weather data """
import json

import requests

# sample url: this url get the weather for the past 50 years
# "https://archive-api.open-meteo.com/v1/archive?latitude=33.89&longitude=35.50&start_date=1970-01-01&end_date=2023-01-01&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,rain_sum,snowfall_sum,windspeed_10m_max,winddirection_10m_dominant&timezone=Africa%2FCairo&min=1990-01-01&max=2023-01-01"


def get_historical_weather(start_date: str, end_date: str, city: tuple,
                           timezone: str = "auto") -> dict:
    """ this function retrieves the temperature for a specified date, city,
    timezone.
    start_date: string in the format yyyy-mm-dd
    end_date: string in the format yyyy-mm-dd
    city: coordinates of the city as a tuple of (latitude, longitude)
    timezone: the timezone requested, defaults to
    """

    # step 1: create the url
    url_start = "https://archive-api.open-meteo.com/v1/archive?" \
                f"latitude={city[0]}&longitude={city[1]}&" \
                f"start_date={start_date}&end_date={end_date}&daily="

    url_end = f"&timezone={timezone}&min={start_date}&max={end_date}"

    # this list represents the values that will be requested in the api call
    variables = [
        "temperature_2m_max",
        "temperature_2m_min",
        "temperature_2m_mean",
        "apparent_temperature_max",
        "apparent_temperature_min",
        "apparent_temperature_mean",
        "rain_sum",
        "snowfall_sum",
        "windspeed_10m_max",
        "winddirection_10m_dominant",
    ]

    the_data = ",".join(variables)

    url = f"{url_start}{the_data}{url_end}"
    print(url)

    # step 2: make api call
    r = requests.get(url)
    if r.status_code == 200:
        response_dict = r.json()
    else:
        response_dict = None

    # raw data format:
    # {"latitude":33.800003,
    # "longitude":35.5,
    # "generationtime_ms":6.30497932434082,
    # "utc_offset_seconds":10800,
    # "timezone":"Africa/Cairo",
    # "timezone_abbreviation":"EEST",
    # "elevation":60.0,
    # "daily_units":{
    #                "time":"iso8601",
    #                "temperature_2m_max":"°C"
    #                 ... amount of info depends on the requested url
    #               },
    # "daily":{
    #          "time":["1970-01-01","1970-01-02","1970-01-03", ...],
    #          "temperature_2m_max":[15.3,18.4,20.4, ...]
    #           ... amount of info depends on the requested url
    #         }
    # }

    if not response_dict:
        print(f"No results returned from API, error: {r.json()['reason']}")
        return

    # format is now:
    # "time":["1970-01-01","1970-01-02","1970-01-03", ...],
    # "temperature_2m_max":[15.3,18.4,20.4, ...]
    # "temperature_2m_min":[...],
    # "temperature_2m_mean":[...],
    # "apparent_temperature_max":[...],
    # "apparent_temperature_min":[...],
    # "apparent_temperature_mean":[...]},
    return response_dict["daily"]


def get_one_month_weather(start: str, end: str, month_nb: str, city: tuple,
                          timezone: str):
    raw_data = get_historical_weather(start, end, city, timezone)

    if not raw_data:
        print("None object returned!")
        return

    counter = 0
    start_year = int(start[:4])
    month = dict()
    for i, v in enumerate(raw_data["time"]):
        year = f"{start_year + counter}"
        if v == f"{year}-{month_nb.rjust(2, '0')}-01":
            month[year] = [raw_data["temperature_2m_max"][i],
                           raw_data["temperature_2m_min"][i],
                           raw_data["temperature_2m_mean"][i],
                           raw_data["apparent_temperature_max"][i],
                           raw_data["apparent_temperature_min"][i],
                           raw_data["apparent_temperature_mean"][i],
                           raw_data['rain_sum'][i],
                           raw_data['snowfall_sum'][i],
                           raw_data['windspeed_10m_max'][i],
                           raw_data['winddirection_10m_dominant'][i],
                           ]
            counter += 1

    print("final temps are\n", month)
    return month


def get_snow_data(start, end, city):
    raw_data = get_historical_weather(start, end, city)
    snow = dict()

    for i, v in enumerate(raw_data["time"]):
        snowfall = raw_data["snowfall_sum"][i]
        if snowfall > 0:
            snow[v] = snowfall

    return snow


# Latitude and Longitudes of selected cities
beirut = (33.89, 35.50)
dubai = (25.08, 55.31)

timezone = "Africa%2FCairo"

# Start and end dates
start = "1970-01-01"
end = "2022-12-31"
filename = "json_files/beirut_50years_2024_test.json"

# data = get_snow_data(start, end, beirut)
# data = get_one_month_weather(start, end, "4", beirut, timezone)
data = get_historical_weather(start, end, beirut, timezone=timezone)

with open(filename, "w") as file:
    json.dump(data, file)
