
from dtypes.movie import Movie
from parser import Parser
import flet as ft

from app.page import Page
from app.movie_card import MovieCard


class SearchMoviePage(Page, ft.Column):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        ft.Column.__init__(self)

        self.spacing = 10

        self.search_results_container = ft.Column(
            controls=[],
            expand=True,
            scroll=True
        )
        self.controls = self.get_controls()

    def open_movie_page(self, movie: Movie):
        self.controller.movie_page.load_movie(movie)
        self.controller.change_page("movie")

    def search_movies(self, e: ft.ControlEvent):
        movies = []

        if e.control.value not in ["", " "]:
            parser = Parser()
            search_results = parser.search(e.control.value)

            movies = [
                MovieCard(movie=movie, callback=self.open_movie_page)
                for movie in search_results.movies
            ]

        self.search_results_container.controls = movies
        self.page.update()

    def get_controls(self):
        return [
            ft.Container(
                ft.TextField(
                    label="Enter movie name",
                    on_change=self.search_movies,
                    adaptive=True,
                    border=ft.border.Border(),
                    border_color=ft.colors.TRANSPARENT,
                    bgcolor=ft.colors.TRANSPARENT,
                    text_align=ft.TextAlign.CENTER
                ),
                alignment=ft.alignment.center_left,
                bgcolor="#121212",
                border_radius=10,
                padding=ft.Padding(left=5, top=0, right=5, bottom=0),
                height=50
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[self.search_results_container],
                        ),
                        expand=True,
                        bgcolor="#121212",
                        border_radius=10,
                        margin=ft.Margin(top=0, left=0, right=0, bottom=10),
                        padding=ft.Padding(top=10, left=10, right=10, bottom=0),
                        alignment=ft.alignment.top_center
                    )
                ],
                expand=True
            )
        ]
