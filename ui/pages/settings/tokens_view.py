import flet as ft
from core.general_service import GeneralService
from core.http.errors import AuthenticationError , RateLimitError , AuthorizationError
from core.platforms.github.github_service import GitHubService
from ui.components.dialogs import Dialog
from datetime import datetime
import os

class TokensView(ft.Column):
    def __init__(self, service: GeneralService):
        super().__init__(expand=True, spacing=20, scroll=ft.ScrollMode.AUTO ,)
        self.service = service
        self.dialogs = None # Will initialize with page later

        self.controls = [
            ft.Container(
                content=ft.ProgressRing(color="#58a6ff", height=35, width=35),
                alignment=ft.alignment.center
            )
        ]

    def did_mount(self):
        self.dialogs = Dialog(self.page)
        self.load_data()

    def load_data(self):
        # Fetch (Platform, Account, Token) tuples
        data = self.service.get_all_tokens_info()
        self.controls = self.build_ui(data)
        self.update()

    def build_ui(self, data):
        if not data:
            return [
                self._header(),
                ft.Container(
                    height=200,
                    alignment=ft.alignment.center,
                    content=ft.Column([
                        ft.Icon(ft.Icons.KEY_OFF, size=50, color="#8b949e"),
                        ft.Text("No access tokens found", color="#8b949e")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            ]

        return [
            self._header(),
            ft.Column(
                controls=self.build_token_cards(data),
                spacing=10
            )
        ]

    def _header(self):
        return ft.Column([
            ft.Text("Access Tokens", size=35, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            ft.Text("Manage authentication tokens for your connected accounts", size=16, color=ft.Colors.GREY),
            ft.Divider(height=1, color=ft.Colors.GREY),
            ft.Container(height=10)
        ])

    def build_token_cards(self, data):
        cards = []
        for item in data:
            platform, account, token = item
            is_valid, status_msg = self.check_token_status(token)
            
            # Status Badge Styles
            status_color = "#3fb950" if is_valid else "#f85149"
            status_bg = "#172b28" if is_valid else "#450a0a" 
            status_text = "Valid" if is_valid else "Expired"

            card = ft.Container(
                bgcolor="#0d1117",
                border=ft.border.all(1, "#30363d"),
                border_radius=8,
                padding=20,
                content=ft.Row([
                    # Left: Icon & Info
                    ft.Row([
                        ft.Container(
                            bgcolor=platform.bgcolor or "#21262d",
                            padding=10,
                            border_radius=8,
                            content=ft.Icon(ft.Icons.KEY, color="white", size=24) 
                        ),
                        ft.Column([
                            ft.Row([
                                ft.Text(f"{platform.display_name} • {account.username}", weight=ft.FontWeight.BOLD, color="white", size=16),
                                ft.Container(
                                    content=ft.Text(status_text, size=12, color=status_color, weight=ft.FontWeight.BOLD),
                                    bgcolor=status_bg,
                                    border=ft.border.all(1, status_color),
                                    border_radius=50,
                                    padding=ft.padding.symmetric(horizontal=10, vertical=2)
                                )
                            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                            ft.Text(f"Expires: {self.format_expiry(token.expires_at)}", color="#8b949e", size=13),
                            ft.Text(status_msg, color="#8b949e", size=12, italic=True)
                        ], spacing=4)
                    ]),

                    # Right: Actions
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT, 
                            icon_color="#58a6ff",
                            tooltip="Change Token",
                            on_click=lambda e, t=token: self.open_edit_dialog(t)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE, 
                            icon_color="#f85149",
                            tooltip="Delete Token",
                            on_click=lambda e, tid=account.id: self.handle_remove_click(tid)
                        )
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )
            cards.append(card)
        return cards

    def open_edit_dialog(self, token):
        # Open the dialog created in dialogs.py
        if self.dialogs:
            self.page.open(self.dialogs.edit_token(token, self.load_data))
            
    def handle_remove_click(self , token_id) :
        loader = ft.ProgressRing(visible=False)
        
        def close_dialog() :
            dialog.open = False
            self.page.update()
        
        def submit(e) :
            loader.visible = True
            self.page.update()
        
            self.delete_token(token_id)
            dialog.open = False
            
            loader.visible = False
            self.load_data()
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#22272e",
            title=ft.Text("Do you want remove this Token ?" , color="#ffffff" , size=20),
            content=ft.Column(
                [
                    ft.Text("by deleting this token , there no data will be deleting with it"),
                    ft.Row([loader], alignment=ft.MainAxisAlignment.CENTER),
                ],
                tight=True
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e:close_dialog()),
                ft.TextButton(
                    "Delete",
                    style=ft.ButtonStyle(color=ft.Colors.RED),
                    on_click=submit,
                ),
            ],
        )
        self.page.open(dialog)

    def delete_token(self, token_id):
        try:
            self.service.delete_token(token_id)
            self.load_data()
            self.page.open(ft.SnackBar(ft.Text("Token deleted successfully"), bgcolor="green"))
        except Exception as e:
            self.page.open(ft.SnackBar(ft.Text(f"Error: {e}"), bgcolor="red"))

    def check_token_status(self, token):
        if not token.expires_at:
            return True, "No expiration date set"
        try:
            expires = datetime.fromisoformat(token.expires_at)
            if expires < datetime.now():
                return False, f"Expired on {expires.strftime('%Y-%m-%d')}"
            return True, f"Valid until {expires.strftime('%Y-%m-%d')}"
        except:
            return False, "Invalid Date"

    def format_expiry(self, date_str):
        if not date_str: return "Never"
        try:
            dt = datetime.fromisoformat(date_str)
            return dt.strftime('%b %d, %Y')
        except:
            return "Unknown"
 
