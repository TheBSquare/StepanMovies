
import flet as ft
import datetime

from dtypes import Movie
from utils.utils import load_history, dump_history
from app.movie_card import MovieCard

from app.page import Page


class DateDivider(ft.Container):
    def __init__(self, date: int):
        ft.Container.__init__(self)
        self.date = datetime.datetime.fromtimestamp(date).strftime("%A %d of %B %Y")
        self.padding = 10

        self.content = self.get_content()

    def get_content(self):
        return ft.Row(
            controls=[
                ft.Text(
                    value=self.date,
                    size=15
                )
            ],
            height=20,
            alignment=ft.alignment.center_left
        )


class HistoryPage(Page, ft.Column):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        ft.Column.__init__(self)

        self.export_file_picker = ft.FilePicker(on_result=self.on_export_file_picked)
        self.import_file_picker = ft.FilePicker(on_result=self.on_import_file_picked)

        self.spacing = 10

        self.history_container = ft.Column(
            controls=[],
            expand=True,
            scroll=True
        )
        self.controls = self.get_controls()

    def load(self):
        movies = []
        last_date = None

        for movie in load_history():
            movie_date = datetime.datetime.fromtimestamp(movie.watched)

            if not last_date or (movie_date.month < last_date.month) or \
                    (movie_date.month == last_date.month and movie_date.day < last_date.day):
                last_date = movie_date
                movies.append(DateDivider(
                    last_date.timestamp()
                ))

            movies.append(
                MovieCard(movie=movie, callback=self.open_movie_page, callback_remove=self.remove_movie)
            )

        self.history_container.controls = movies

    def open_movie_page(self, movie: Movie):
        self.controller.movie_page.load_movie(movie)
        self.controller.change_page("movie")

    def remove_movie(self, movie: Movie):
        history = load_history()
        for i, temp_movie in enumerate(history):
            if temp_movie.id == movie.id:
                del history[i]
                break

        if self.controller.movie_page.current_movie and self.controller.movie_page.current_movie.id == movie.id:
            self.controller.movie_page.current_movie = None

        dump_history(history)

        self.load()
        self.controller.page.update()

    def on_export_file_picked(self, e: ft.FilePickerResultEvent):
        export_file = e.path

        if export_file:
            history = load_history()
            dump_history(history, export_file)

            self.controller.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Exported history to {export_file} with {len(history)} movies")
            )
            self.controller.page.snack_bar.open = True
            self.controller.page.update()

    def on_import_file_picked(self, e: ft.FilePickerResultEvent):
        import_files = e.files

        if len(import_files):
            import_file = import_files[0]

            try:
                history = load_history(path=import_file.path)
                ids = list(map(lambda x: x.id, history))

                for movie in load_history():
                    if movie.id not in ids:
                        history.append(movie)

                dump_history(history)

                self.controller.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Imported {import_file.path} with {len(history)} movies")
                )
                self.controller.page.snack_bar.open = True

                self.controller.movie_page.current_movie = None
                self.load()

            except Exception as err:
                self.controller.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Imported file {import_file.path} has some errors, so I can't import it")
                )
                self.controller.page.snack_bar.open = True

            self.controller.page.update()

    def get_controls(self):
        return [
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.TextButton(
                            text="import",
                            on_click=lambda _: self.import_file_picker.pick_files(allow_multiple=False, allowed_extensions=["json"]),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(
                                    radius=5
                                ),
                                color=ft.colors.WHITE
                            )
                        ),
                        ft.Text(
                            value="Watch history",
                            size=18,
                            text_align=ft.TextAlign.CENTER,
                            expand=True
                        ),
                        ft.TextButton(
                            text="export",
                            on_click=lambda _: self.export_file_picker.save_file(file_name=f"history-{datetime.datetime.now().strftime('%m.%d.%YT%H.%M.%S')}.json"),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(
                                    radius=5
                                ),
                                color=ft.colors.WHITE
                            )
                        )
                    ]
                ),
                alignment=ft.alignment.center,
                bgcolor="#121212",
                border_radius=10,
                padding=ft.Padding(left=15, top=0, right=15, bottom=0),
                height=50
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[self.history_container],
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
