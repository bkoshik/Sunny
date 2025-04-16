# ========== IMPORT ==========
import argparse
import re
from typing import NamedTuple
from parser import configure_parser
from fetch_weather import fetch_weather_wttr, fetch_weather_owm

# ========== FORMAT ==========
def print_format(type: str) -> str:
    args: argparse.Namespace = configure_parser()
    weather: NamedTuple = fetch_weather_owm(args.City, args.Units)

    format: dict[str, str] = {
        "reg": weather.region,
        "desc": weather.description,
        "temp": weather.temperature,
        "wind": weather.wind,
        "srise": weather.sunrise,
        "sset": weather.sunset,
        "date": weather.timestamp,
        "\\n": "\n",
        "\\t": "\t",
    }

    return type.format(**format)

def json_template_render(template: str, data: dict) -> str:
    def extractor(match):
        path = match.group(1)
        try:
            keys = path.split(".")
            value = data
            for key in keys:
                if key.isdigit():
                    value = value[int(key)]
                else:
                    value = value[key]
            return str(value)
        except (KeyError, IndexError, TypeError):
            return f"{{{path}}}"  # оставить как есть, если ошибка

    return re.sub(r"{([^}]+)}", extractor, template)
