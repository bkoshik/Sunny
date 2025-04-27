# ========== IMPORT ==========
import argparse
import re
from parser import configure_parser
from fetch_weather import fetch_weather_wttr, fetch_weather_owm, fetch_weather_wapi
from config import api_owm, api_wapi

# ========== FORMAT ==========


def print_format(type: str) -> str:
    args: argparse.Namespace = configure_parser()
    if args.Source == "wttr.in":
        weather = fetch_weather_wttr(args.City, args.Units)
    elif args.Source == "openweathermap":
        weather = fetch_weather_owm(args.City, args.Units, api_owm)
    elif args.Source == "weatherapi":
        weather = fetch_weather_wapi(args.City, args.Units, api_wapi)

    format: dict[str, str] = {
        "region": weather.region,
        "description": weather.description,
        "temperature": weather.temperature,
        "wind": weather.wind,
        "sunrise": weather.sunrise,
        "sunset": weather.sunset,
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
