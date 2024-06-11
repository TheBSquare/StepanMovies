
from dtypes.movie import Movie


class SearchResult:
    query: str
    movies: list[Movie]

    def __init__(
        self,
        query: str,
        movies: list[Movie]
    ):
        self.query = query
        self.movies = movies
