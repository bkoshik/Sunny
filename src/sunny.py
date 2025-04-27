#!/home/baktiar/develop/python/venv/bin/python3

# ========== IMPORTS ==========
from datetime import datetime
from typing import NamedTuple, Optional
import requests
import argparse
import re
from modules.ascii_art import find_ascii
from modules.fetch_weather import fetch_weather_wttr, fetch_weather_owm, fetch_weather_wapi
from modules.parser import configure_parser
from modules.format import print_format, json_template_render
from modules.config import *

# ========== DRAWING ==========
# Delete ANSI for draw_box find_ascii
def visible_length(s: str) -> int:
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return len(ansi_escape.sub('', s))

# Draw box with date
def draw_box(lines: list[str], width: int = 45) -> str:
    top = "┌" + "─" * width + "┐"
    day = "│" + " " * (width//2 - 5) + f"\033[1m{datetime.now().strftime("%a %d %b")}\033[0m" + " " * (width//2 - 4) + "│"
    mid = "├" + "─" * 13 + "┬" + "─" * (width - 14) + "┤"
    bot = "└" + "─" * 13 + "┴" + "─" * (width - 14) + "┘"
    body = ""
    # Drawing
    for line in lines:
        vis_len = visible_length(line)
        padding = width - vis_len
        body += f"│{line}{' ' * (padding)}│\n"
    return f"{top}\n{day}\n{mid}\n{body}{bot}"

def draw_box_ascii_only(lines: list[str], width: int = 14) -> str:
    top = "┌" + "─" * width + "┐"
    day = "│" + " " * (width//2 - 5) + f"\033[1m{datetime.now().strftime("%a %d %b")}\033[0m" + " " * (width//2 - 5) + "│"
    mid = "├" + "─" * width + "┤"
    bot = "└" + "─" * width + "┘"
    body = ""
    # Drawing
    for line in lines:
        vis_len = visible_length(line)
        padding = width - vis_len - 1
        body += f"│{line} {' ' * padding}│\n"
    return f"{top}\n{day}\n{mid}\n{body}{bot}"

# ========== RENDER ==========
def print_weather(weather_data: NamedTuple, args: argparse.Namespace) -> None:
    # Print weather with ASCII art
    if not any(groups["output"]):
        ascii_weather: list[str] = find_ascii(
            weather_data[1])

        print() # To do padding

        # Drawing
        text: list[str] = [f"{ascii_weather[i]}│ \033[1m{list_names_weather[i]}\033[0m{separator}{weather_data[i]}" for i in range((0 if showCityName else 1), (7 if showTime else 6))]
        print(draw_box(text))
    
    elif args.Format:
        print(print_format(args.Format)) # Print your own format
    
    elif args.JsonFormat:
        print(json_template_render(args.JsonFormat, requests.get(f"https://wttr.in/{args.City}?format=j1").json())) # Print your own format using json

    elif args.Ascii: # Print only ASCII art
        lines: list[str] = find_ascii(weather_data[1])[1:-2]
        print(draw_box_ascii_only(lines))

# ========== MAIN ==========
def main(args) -> None:
    def source(api_owm: str, api_wapi: str, args: argparse.Namespace):
        def weather_source(city: str, units: str, api_owm: str, api_wapi: str):
            if args.Source == "wttr.in":
                weather = fetch_weather_wttr(city, units)
            elif args.Source == "openweathermap":
                weather = fetch_weather_owm(city, units, api_owm)
            elif args.Source == "weatherapi":
                weather = fetch_weather_wapi(city, units, api_wapi)

            return weather

        if args.City:
            return weather_source(args.City, args.Units, api_owm, api_wapi)
        elif args.AutoCity:
            ipcity: str = requests.get("https://ipinfo.io").json()["city"]
            return weather_source(ipcity, args.Units, api_owm, api_wapi)

    # Calling print_weather function
    weather = source(api_owm, api_wapi, args)

    if weather:
        print_weather(weather, args)


if __name__ == "__main__":
    args: argparse.Namespace = configure_parser()
    main(args)
