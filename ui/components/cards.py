import flet as ft
from ui.theme import AppTheme

class SurfaceCard(ft.Container):
    def __init__(self, content, padding=20, on_click=None, **kwargs):
        super().__init__(
            content=content,
            padding=padding,
            bgcolor=AppTheme.BG_SURFACE,
            border_radius=8,
            border=ft.border.all(1, AppTheme.BORDER_COLOR),
            on_click=on_click,
            **kwargs
        )
