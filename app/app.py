
import flet as ft

from .search_page import SearchMoviePage
from .movie_page import MoviePage
from .history_page import HistoryPage
from .page import Page

from utils.utils import get_primary_monitor_size, load_history


class App(ft.Container):
    def __init__(self, *args, **kwargs):
        ft.Container.__init__(self, *args, **kwargs)

        self.expand = True
        self.rail = None

        self.movie_page = MoviePage(controller=self)
        self.search_movie_page = SearchMoviePage(controller=self)
        self.history_page = HistoryPage(controller=self)

        self.page_selected = ft.Container(
            expand=True,
            content=self.search_movie_page,
            padding=ft.Padding(left=0, top=10, right=10, bottom=0)
        )

        self.content = self.get_controls()

    def get_selected_index(self, page) -> int:
        return {
            self.search_movie_page: 0,
            self.movie_page: 1,
            self.history_page: 2
        }.get(page)

    def change_page(self, i):
        selected_page: Page = {
            "0": self.search_movie_page,
            "search": self.search_movie_page,
            "1": self.movie_page,
            "movie": self.movie_page,
            "2": self.history_page,
            "history": self.history_page
        }.get(str(i))

        if not selected_page:
            return

        if selected_page == self.movie_page and not len(load_history()):
            self.rail.selected_index = self.get_selected_index(self.page_selected.content)
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Please search some movie before opening this tab :)")
            )
            self.page.snack_bar.open = True

        else:
            self.rail.selected_index = self.get_selected_index(selected_page)
            self.page_selected.content = selected_page
            selected_page.load()

        self.page.update()

    def get_controls(self):
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            bgcolor=ft.colors.TRANSPARENT,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.SEARCH, selected_icon=ft.icons.SAVED_SEARCH
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PERSONAL_VIDEO_ROUNDED, selected_icon=ft.icons.ONDEMAND_VIDEO_ROUNDED
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.STORAGE, selected_icon=ft.icons.STORAGE
                )
            ],
            on_change=lambda x: self.change_page(x.data)
        )

        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=self.rail,
                                bgcolor="#121212",
                                border_radius=10,
                                expand=True
                            )
                        ]
                    ),
                    margin=ft.Margin(
                        left=10,
                        top=10,
                        right=0,
                        bottom=10
                    ),
                    width=50
                ),
                self.page_selected
            ],
            spacing=10
        )

    def run(self, page: ft.Page):
        width, height = get_primary_monitor_size()

        page.padding = 0
        page.bgcolor = "#000000"
        page.window_width = width // 1.3
        page.window_height = height // 1.3
        page.window_left = (width - page.window_width) // 2
        page.window_top = (height - page.window_height) // 2
        page.snack_bar = ft.SnackBar(content=ft.Text("Nothing"))

        page.overlay.append(self.history_page.export_file_picker)
        page.overlay.append(self.history_page.import_file_picker)

        page.add(self)
