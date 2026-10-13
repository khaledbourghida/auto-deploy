import flet as ft


class GlobalLoader(ft.Container):
    def __init__(self):
        super().__init__(
            visible=False,
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.6, "#000000"),
            alignment=ft.alignment.center,
            content=ft.ProgressRing(),
        )

    def show(self, page: ft.Page):
        self.visible = True
        page.update()

    def hide(self, page: ft.Page):
        self.visible = False
        page.update()
