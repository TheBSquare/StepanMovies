
import flet as ft
from app import App


def main(page: ft.Page):
    app = App()
    app.run(page)


app = ft.app(main)
