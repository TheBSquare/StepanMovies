
from screeninfo import get_monitors
from uuid import uuid3, NAMESPACE_URL
import json


from dtypes import Movie
from config import HISTORY_PATH


def string_to_uuid(string: str) -> str:
    return uuid3(NAMESPACE_URL, string).hex


def get_max_quality(qualities):
    if len(qualities) == 0:
        return None

    max_quality = -1

    for quality in qualities:
        try:
            quality = quality.replace("p Ultra", "")
            quality = quality.replace("p", "")
            quality = int(quality)

        except Exception as err:
            continue

        if quality > max_quality:
            max_quality = quality

    return qualities["1080p Ultra"] if "1080p Ultra" in qualities else qualities[str(max_quality)+"p"]


def get_primary_monitor_size():
    for monitor in get_monitors():
        if monitor.is_primary:
            return monitor.width, monitor.height

    exit()


def load_history(path=HISTORY_PATH) -> list[Movie]:
    return sorted(list(map(lambda x: Movie(**x), json.load(open(path)))), key=lambda x: x.watched, reverse=True)


def dump_history(movies: list[Movie], path=HISTORY_PATH):
    return json.dump(list(map(lambda x: x.to_dict(), movies)), open(path, "w"))
