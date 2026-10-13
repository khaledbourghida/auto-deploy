import flet as ft
import threading
import time

class GlobalToast(ft.Container):
    def __init__(self):
        super().__init__(
            visible=False,
            bottom=20,
            right=20,
            padding=15,
            border_radius=10,
            bgcolor="#1f6feb",
            content=ft.Text("", color="white"),
        )

    def _show(self, page: ft.Page, message: str, color: str, duration=2):
        self.content.value = message
        self.bgcolor = color
        self.visible = True
        page.update()

        def auto_hide():
            time.sleep(duration)
            self.visible = False
            page.update()

        threading.Thread(target=auto_hide, daemon=True).start()

    def success(self, page: ft.Page, message: str):
        self._show(page, message, "#238636")

    def error(self, page: ft.Page, message: str):
        self._show(page, message, "#da3633")

    def info(self, page: ft.Page, message: str):
        self._show(page, message, "#1f6feb")
