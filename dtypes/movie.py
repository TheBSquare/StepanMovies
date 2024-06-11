
from utils.jsonify import Jsonified


class Movie(Jsonified):
    id: str
    link: str
    title: str
    subtitle: str
    is_series: bool
    poster: str
    watched: int | None

    def __init__(
        self,
        id: str,
        link: str,
        title: str,
        subtitle: str,
        poster: str,
        watched: int = None,
        source: str = None
    ):
        self.id = id
        self.link = link
        self.title = title
        self.subtitle = subtitle
        self.poster = poster
        self.watched = watched
        self.source = source

        self.fields = [
            "id", "link", "title",
            "subtitle", "poster",
            "watched", "source"
        ]
