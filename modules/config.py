# ========== IMPORT ==========
import argparse
import os
from typing import Optional
from parser import configure_parser

# ========== CONFIG ==========
showCityName: bool = True
showTime: bool = True
separator: str = ": "
api: Optional[str] = os.getenv("API_WEATHER") # Change it to your api but it doesn't important if you don't use APIOpenWeather or you can add enviroment variable
list_names_weather: list[str] = [ # Here you can change names of data, but you mustn't change meaning, only when you change `fetch_weather.py`
    "Region",
    "Description",
    "temperature",
    "Wind speed",
    "Sunrise",
    "Sunset",
    "Timestamp",
]

args: argparse.Namespace = configure_parser()
groups = {
    "location": [args.City, args.AutoCity],
    "output": [args.Ascii, args.Format, args.JsonFormat]
}
