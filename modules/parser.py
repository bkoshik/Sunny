# ========== IMPORT ==========
import argparse

# ========== PARSER ==========
def configure_parser() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Fetch weather data for a city")
    cityGroup: argparse._MutuallyExclusiveGroup = parser.add_mutually_exclusive_group(required=True)
    formatGroup: argparse._MutuallyExclusiveGroup = parser.add_mutually_exclusive_group(required=False)

    cityGroup.add_argument("-c", "--city", dest="City", type=str,
                        help="City for fetch weather")
    cityGroup.add_argument("-A", "--auto-city", dest="AutoCity",
                        action="store_true", help="Autodetect your city")
    parser.add_argument("-u", "--units", dest="Units",
                        choices=["metric", "imperial"], default="metric")
    formatGroup.add_argument("-a", "--ascii", dest="Ascii",
                        required=False, action="store_true", help="Only Ascii art")
    formatGroup.add_argument("-f", "--format", dest="Format", 
                        required=False, action="store", help="Use your own format")
    formatGroup.add_argument("-jf", "--json-format", dest="JsonFormat",
                        required=False, action="store", help="Use your own format with json parsing")
    parser.add_argument("-s", "--source", dest="Source",
                        choices=["wttr.in", "openweathermap"], default="wttr.in")

    return parser.parse_args()
