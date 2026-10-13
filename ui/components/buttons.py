import flet as ft
from ui.theme import AppTheme

class PrimaryButton(ft.ElevatedButton):
    def __init__(self, text, icon=None, on_click=None, **kwargs):
        super().__init__(
            text=text,
            icon=icon,
            on_click=on_click,
            color=ft.colors.WHITE,
            bgcolor=AppTheme.PRIMARY,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=6),
                padding=ft.padding.all(16),
            ),
            **kwargs
        )

class SecondaryButton(ft.OutlinedButton):
    def __init__(self, text, icon=None, on_click=None, **kwargs):
        super().__init__(
            text=text,
            icon=icon,
            on_click=on_click,
            style=ft.ButtonStyle(
                color=AppTheme.TEXT_PRIMARY,
                shape=ft.RoundedRectangleBorder(radius=6),
                padding=ft.padding.all(16),
                side=ft.BorderSide(1, AppTheme.BORDER_COLOR),
            ),
            **kwargs
        )
