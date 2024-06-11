
import flet as ft
from dtypes import Movie
import datetime


class MovieCard(ft.ElevatedButton):
    def __init__(self, movie: Movie, callback, callback_remove=None):
        ft.ElevatedButton.__init__(self, on_click=lambda x: callback(movie))
        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(
                radius=5
            ),
            padding=ft.Padding(
                left=10,
                right=10,
                top=15,
                bottom=15
            ),
            bgcolor="#181818",
            overlay_color="#242424"
        )
        self.movie = movie
        self.callback_remove = callback_remove

        self.content = self.get_content()

    def get_content(self):
        name_col = [
            ft.Text(self.movie.title, color=ft.colors.WHITE, size=20),
            ft.Text(self.movie.subtitle, color=ft.colors.WHITE, size=12, expand=True)
        ]

        if self.movie.watched:
            name_col += [
                ft.Text(datetime.datetime.fromtimestamp(self.movie.watched).strftime("%H:%M"), color=ft.colors.WHITE, size=12)
            ]

        controls = [
            ft.Image(
                src=self.movie.poster,
                fit=ft.ImageFit.COVER,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(5),
            ),
            ft.Container(
                content=ft.Column(
                    controls=name_col,
                ),
                expand=True
            )
        ]

        if self.callback_remove:
            controls += [
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color=ft.colors.RED_400,
                    on_click=lambda x: self.callback_remove(self.movie)
                ),
                ft.Container(
                    width=25
                )
            ]

        return ft.Row(
            controls=controls,
            height=150,
            alignment=ft.alignment.center_left
        )
