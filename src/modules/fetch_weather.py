# ========== IMPORTS ==========
import requests
import tzlocal
from datetime import datetime
from typing import NamedTuple, Optional

# ========= NAMEDTUPLE ==========
class Weather(NamedTuple):
    region: str
    description: str
    temperature: str
    wind: str
    sunrise: str
    sunset: str
    timestamp: str

# ========== TEMP COLORS ==========
def get_temperature_color(temp: int, units: str) -> Optional[str]:
    if units == "metric":
        thresholds = [(-20, "35"), (-13, "38;5;201"), (3, "38;5;51"), (15, "38;5;28"), (25, "33"), (30, "38;5;208")]
    elif units == "imperial":
        thresholds = [(-5, "35"), (10, "38;5;201"), (35, "38;5;51"), (60, "38;5;28"), (75, "33"), (85, "38;5;208")]
    else:
        return None

    for threshold, color in thresholds:
        if temp <= threshold:
            return f"\033[{color}m"
    return "\033[31m"

# ========== WIND COLORS ==========
def get_wind_color(speed: int, units: str) -> Optional[str]:
    if units == "metric":
        thresholds = [(5, "36"), (15, "32"), (30, "38;5;226"), (50, "38;5;208")]
    elif units == "imperial":
        thresholds = [(3, "36"), (10, "32"), (20, "38;5;226"), (30, "38;5;208")]
    else:
        return None

    for threshold, color in thresholds:
        if speed <= threshold:
            return f"\033[{color}m"
    return "\033[31m"

# ========== FETCHING WEATHER ==========
def fetch_weather_wttr(city: str, units: str) -> Weather:
    # Getting weather in json format
    response: requests.Response = requests.get(f"https://wttr.in/{city}?format=j1")
    data = response.json()
    current = data["current_condition"][0]

    # Getting region name
    region = data["nearest_area"][0]["region"][0]["value"]

    # Getting weather description
    description = current["weatherDesc"][0]["value"].split(",")[0].strip()

    # Temperature
    temp_key = f"temp_{'C' if units == 'metric' else 'F'}"
    feels_key = f"FeelsLike{'C' if units == 'metric' else 'F'}"
    temp = get_temperature_color(int(current[temp_key]), units) + current[temp_key] + "\033[0m"
    feels = get_temperature_color(int(current[feels_key]), units) + current[feels_key] + "\033[0m"
    unit_temp = "°C" if units == "metric" else "°F"
    feels_part = "" if feels == temp else f"({feels})"

    # Wind
    wind_key = "Kmph" if units == "metric" else "Miles"
    wind = get_wind_color(int(current[f"windspeed{wind_key}"]), units) + current[f"windspeed{wind_key}"] + "\033[0m"
    unit_wind = "km/h" if units == "metric" else "miles"

    # Sunrise / Sunset
    sunrise = datetime.strptime(
        data["weather"][0]["astronomy"][0]["sunrise"], "%I:%M %p"
    ).strftime("%H:%M")
    sunset = datetime.strptime(
        data["weather"][0]["astronomy"][0]["sunset"], "%I:%M %p"
    ).strftime("%H:%M")

    # Timestamp
    timestamp = datetime.strptime(
        current["localObsDateTime"], "%Y-%m-%d %I:%M %p"
    ).strftime("%x %H:%M")

    return Weather(region, description, f"{temp}{feels_part} {unit_temp}",
                   f"{wind} {unit_wind}", sunrise, sunset, timestamp)

def fetch_weather_owm(city: str, units: str, api: str) -> Weather:
    # Getting weather in json format
    response: requests.Response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=en&units={units}&APPID={api}")
    data = response.json()

    # Getting region name
    region = data["name"]

    # Getting weather description
    description = data["weather"][0]["main"]

    # Temperature
    temp = f"{get_temperature_color(int(data["main"]["temp"]), units)}{data["main"]["temp"]}\033[0m"
    feels = f"{get_temperature_color(int(data["main"]["feels_like"]), units)}{data["main"]["feels_like"]}\033[0m"
    unit_temp = "°C" if units == "metric" else "°F"
    feels_part = "" if feels == temp else f"({feels})"

    # Wind
    wind = f"{get_wind_color(int(data["wind"]["speed"]), units)}{data["wind"]["speed"]}\033[0m"
    unit_wind = "km/h" if units == "metric" else "miles"

    # Sunrise / Sunset
    tz = tzlocal.get_localzone()
    sunrise = datetime.fromtimestamp(
        data["sys"]["sunrise"],
        tz
    ).strftime('%H:%M:%S')
    sunset = datetime.fromtimestamp(
        data["sys"]["sunset"],
        tz
    ).strftime('%H:%M:%S')

    # Timestamp
    timestamp = datetime.now().strftime("%x %H:%S")

    return Weather(region, description, f"{temp}{feels_part} {unit_temp}",
                   f"{wind} {unit_wind}", sunrise, sunset, timestamp)
