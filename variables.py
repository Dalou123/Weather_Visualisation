allowed_weather_values = [
    "time",
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


wind_direction_guide = dict(
    {
        range(0, 45): "N",
        range(45, 90): "NE",
        range(90, 135): "E",
        range(135, 180): "SE",
        range(180, 225): "S",
        range(225, 270): "SW",
        range(270, 315): "W",
        range(315, 360): "NW",
    }
)

# set the [color, label, linestyle] settings for each key
customizations = {
    "time": ["k", "Date", "solid"],
    "temperature_2m_max": ["#cc0000", "Temp max", "-"],
    "temperature_2m_min": ["#0052cc", "Temp min", "-"],
    "temperature_2m_mean": ["#e65c00", "Temp mean", "-"],
    "apparent_temperature_max": ["#ff9999", "Apparent Temp Max", ":"],
    "apparent_temperature_min": ["#66a3ff", "Apparent Temp Min", ":"],
    "apparent_temperature_mean": ["#ff944d", "Apparent Temp Mean", ":"],
    "rain_sum": ["#8585ad", "Rainfall", "solid"],
    "snowfall_sum": ["#99ffff", "Snowfall", "solid"],
    "windspeed_10m_max": ["g", "Wind Speed", "-."],
    "winddirection_10m_dominant": ["red", "Wind Direction", (0, (5, 10))],
}
