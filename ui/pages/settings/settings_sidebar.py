import flet as ft
from core.general_service import GeneralService
from core.http.errors import AuthenticationError , RateLimitError , AuthorizationError
from core.platforms.github.github_service import GitHubService
from ui.components.dialogs import Dialog
from datetime import datetime
import os

class SettingsSidebar(ft.Container):
    def __init__(self, on_select):
        super().__init__(bgcolor="#2f82f7" , border=ft.Border(right=ft.BorderSide(1,ft.Colors.GREY)))

        self.on_select = on_select
        self.active_key = "accounts"

        self.width = 260
        self.bgcolor = "#0d1117"
        self.padding = ft.padding.all(12)

        self.content = ft.Column(
            spacing=6,
            controls=[
                self._section_title("GENERAL SETTINGS"),
                self._item("accounts", "Accounts", ft.Icons.PERSON),
                self._item("tokens", "Tokens", ft.Icons.KEY),
                self._item("ratelimits", "Rate Limits", ft.Icons.SPEED),
                self._item("preferences", "Preferences", ft.Icons.SETTINGS),
            ],
        )

    # ---------- UI BUILDERS ----------

    def _section_title(self, text: str):
        return ft.Container(
            padding=ft.padding.only(left=8, top=12, bottom=6),
            content=ft.Text(
                text,
                size=11,
                weight=ft.FontWeight.BOLD,
                color="#8b949e",
            ),
        )

    def _item(self, key, label, icon):
        return ft.Container(
            key=key,
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=10, vertical=8),
            on_click=lambda e: self._select(key),
            content=ft.Row(
                spacing=12,
                controls=[
                    ft.Icon(icon, size=18),
                    ft.Text(label, size=14),
                ],
            ),
        )

    # ---------- STATE ----------

    def _select(self, key):
        self.active_key = key
        self.on_select(key)

        for item in self.content.controls:
            if isinstance(item, ft.Container) and item.key:
                is_active = item.key == key
                item.bgcolor = "#161b22" if is_active else None
                item.content.controls[0].color = "#58a6ff" if is_active else "#8b949e"
                item.content.controls[1].color = "#ffffff" if is_active else "#c9d1d9"

        self.update()

