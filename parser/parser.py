
import base64
import re
import urllib.parse
import time

import requests
from bs4 import BeautifulSoup

from dtypes import SearchResult, Movie
from utils.utils import string_to_uuid, get_max_quality


class Parser:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    def search(self, query):
        search_link = f"https://hdrezka.ag/search/?do=search&subaction=search&q={query}"

        response = requests.get(search_link, headers=self.headers)
        if response.status_code != 200:
            return SearchResult(
                query=query,
                movies=[]
            )

        soup = BeautifulSoup(response.text, "html.parser")

        movies = []

        for movie_card in soup.select("div.b-content__inline_item"):
            movie_link = movie_card.get("data-url")
            poster = movie_card.select_one("img").get("src")

            title_block = movie_card.select_one("div.b-content__inline_item-link")
            title = title_block.select_one("a").get_text(strip=True)
            subtitle = title_block.select_one("div").get_text(strip=True)

            if "series" in movie_link:
                continue

            movies.append(
                Movie(
                    id=string_to_uuid(movie_link),
                    link=movie_link,
                    title=title,
                    subtitle=subtitle,
                    poster=poster,
                    is_series=False
                )
            )

        return SearchResult(
            query=query,
            movies=movies
        )

    def __decode_streams(self, string):
        def b1(s):
            encoded = urllib.parse.quote(s)
            encoded = encoded.replace('%', '')
            decoded_bytes = bytes.fromhex(encoded)
            return base64.b64encode(decoded_bytes).decode('utf-8')

        def b2(s):
            decoded_bytes = base64.b64decode(s)
            decoded_string = decoded_bytes.decode('utf-8')
            return urllib.parse.unquote(decoded_string)

        v = {
            "bk4": "$$!!@$$@^!@#$$@",
            "bk3": "@@@@@!##!^^^",
            "bk2": "####^!!##!@@",
            "bk1": "^^^!@##!!##",
            "bk0": "$$#!!@#!@##"
        }

        file3_separator = r'//_//'

        a = string[2:].replace(r'\/\/_\/\/', "//_//")

        for i in "43210":
            i = f"bk{i}"
            if i in v and v[i] != "":
                a = a.replace(file3_separator + b1(v[i]), "")

        return b2(a)

    def __find_streams(self, string, is_found=False):
        streams = {}

        if not is_found:
            pattern = r'"streams":\s*"(.*?)",'

            match = re.search(pattern, string, re.DOTALL)

            if not match:
                return streams

            streams_bytes = match.group(1)

        else:
            streams_bytes = string

        streams_raw = self.__decode_streams(streams_bytes)
        qualities = streams_raw.split(",")

        for quality_raw in qualities:
            parts = quality_raw.split("]")
            quality = parts[0][1:]

            #if quality == "1080p Ultra":
            #    continue

            streams.update({
                quality: parts[1].split(" or ")[1]
            })

        return streams

    def get_movie_stream(self, movie: Movie):
        if movie.source and time.time() - movie.watched <= 86400:
            return movie.source

        response = requests.get(movie.link, headers=self.headers)

        if response.status_code != 200:
            return None

        source = get_max_quality(self.__find_streams(response.text))
        movie.source = source
        return source
