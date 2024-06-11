import time

import flet as ft

from dtypes.movie import Movie
from utils.utils import load_history, dump_history
from parser import Parser

from app.page import Page


class MoviePage(Page, ft.Container):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        ft.Container.__init__(self)

        self.current_movie: Movie = None

        self.expand = True
        self.margin = ft.Margin(top=0, bottom=10, left=0, right=0)
        self.content = None
        self.video = ft.Video(
            expand=True,
            playlist=ft.VideoMedia(
                resource=None,
                http_headers={
                    "Accept": "*/*",
                    "Accept-Encoding": "identity;q=1, *;q=0",
                    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                    "Connection": "keep-alive",
                    "Referer": None,
                    "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": "\"macOS\"",
                    "Sec-Fetch-Dest": "video",
                    "Sec-Fetch-Mode": "no-cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
                }
            ),
            playlist_mode=ft.PlaylistMode.SINGLE,
            fill_color=ft.colors.BLACK,
            fit=ft.ImageFit.FIT_WIDTH,
            opacity=1,
            volume=100,
            autoplay=True,
            muted=False,
            on_loaded=lambda x: x,
            filter_quality=ft.FilterQuality.HIGH,
            wakelock=True
        )

    def load(self):
        if not self.content:
            self.content = self.get_content()

    def load_movie(self, movie):
        history = load_history()

        for i, temp_movie in enumerate(history):
            if temp_movie.id == movie.id:
                movie.source = temp_movie.source if temp_movie.source else movie.source
                movie.watched = temp_movie.watched if temp_movie.watched else movie.watched
                del history[i]
                break

        parser = Parser()
        parser.get_movie_stream(movie)

        movie.watched = round(time.time())

        movies = [movie, *history]
        dump_history(movies)

        self.current_movie = movie
        self.video.playlist.resource = self.current_movie.source
        self.video.playlist.http_headers["reffer"] = self.current_movie.source

    def get_content(self):
        if self.current_movie:
            return

        self.load_movie(load_history()[0])

        if not self.current_movie.source:
            self.controller.page.snack_bar = ft.SnackBar(
                content=ft.Text("This film is not avaible in your country :(")
            )
            self.controller.page.snack_bar.open = True

        return ft.Stack(
            controls=[
                ft.Container(
                    content=self.video,
                    border_radius=10,
                    margin=10
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            value=self.current_movie.title,
                                            size=25,
                                            selectable=True
                                        ),
                                        ft.Text(
                                            value=self.current_movie.subtitle,
                                            size=15,
                                            selectable=True
                                        )
                                    ]
                                ),
                                padding=10,
                                border_radius=10,
                                expand=True
                            ),
                        ]
                    ),
                    height=250,
                )
            ]
        )
