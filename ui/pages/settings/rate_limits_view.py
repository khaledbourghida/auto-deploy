import flet as ft
from core.general_service import GeneralService
from core.http.errors import AuthenticationError , RateLimitError , AuthorizationError
from core.platforms.github.github_service import GitHubService
from ui.components.dialogs import Dialog
from datetime import datetime
import os

class RateLimitsView(ft.Column):
    def __init__(self, navigator , service : GeneralService):
        super().__init__(expand=True, spacing=20)
        self.navigator = navigator
        self.service = service
        self.platforms = self.service.platforms
        
        # State containers
        self.github_content = ft.Column(spacing=15 , scroll=ft.ScrollMode.AUTO)
        
        # Initialization
        self.controls = [
            self._build_header(),
            self._build_tabs()
        ]

    def did_mount(self):
        self.load_github_data()

    def _build_header(self):
        return ft.Column([
            ft.Text("API Rate Limits", size=24, weight=ft.FontWeight.BOLD, color="white"),
            ft.Text("Monitor your API usage quota to avoid service interruptions.", color="#8b949e", size=14),
        ], spacing=5)

    def _build_tabs(self):
        return ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text=platform.display_name,
                    icon=ft.Image(src=f"{platform.icon}.png" , height=45 , width=45),
                    content=self._build_placeholder(f"{platform.display_name} support coming soon") if platform.name != "github" else ft.Container(content=self.github_content,padding=ft.padding.only(top=20))
                ) for platform in self.platforms
            ],
            expand=True,
        )

    def load_github_data(self):
        """
        Orchestrates the loading of GitHub data. 
        It clears previous content, shows a loader, then fetches data.
        """
        # 1. Show Loading State
        self.github_content.controls = [
            ft.Row([ft.ProgressRing(height=30, width=30, stroke_width=2), ft.Text("Fetching data from GitHub...")], 
                   alignment=ft.MainAxisAlignment.CENTER)
        ]
        self.update()

        # 2. Fetch Accounts
        try:
            # Safely get the ID, fallback to 1 if lookup fails
            try:
                gh_id = self.service.platform_repo.get_id_by_name("github") or 1
            except:
                gh_id = 1
                
            accounts = self.service.account_repo.get_by_platform(gh_id)
        except Exception as e:
            self._show_global_error(f"Database Error: {e}")
            return

        # 3. Handle Empty State
        if not accounts:
            self.github_content.controls = [
                ft.Container(
                    alignment=ft.alignment.center,
                    padding=40,
                    content=ft.Column([
                        ft.Icon(ft.Icons.LINK_OFF, size=50, color="#8b949e"),
                        ft.Text("No GitHub accounts connected", color="#8b949e")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            ]
            self.update()
            return

        # 4. Process Each Account safely
        cards = []
        for account in accounts:
            cards.append(self._build_loader_card())
            self.github_content.controls = cards
            self.update()
            try:
                gh_service = GitHubService(account, self.navigator, self.page)
                
                data = gh_service.get_rate_limit()
                
                cards.pop()
                cards.append(self._build_rate_card(account, data))
                
            except AuthenticationError as e:
                print("auth")
                cards.pop()
                cards.append(self._build_error_card(account, str(e)))
            except AuthorizationError as e :
                print("authz")
                cards.pop()
                cards.append(self._build_error_card(account , str(e)))
            except RateLimitError as e :
                print("ratelimit")
                cards.pop()
                cards.append(self._build_error_card(account , str(e)))
            except Exception as e:
                print("exc")
                cards.pop()
                cards.append(self._build_error_card(account, f"Unexpected error: {str(e).split(':')[0]}"))
            
            self.github_content.controls = cards
            self.update()

    def _show_global_error(self, message):
        self.github_content.controls = [
            ft.Container(
                bgcolor="#450a0a", padding=15, border_radius=8,
                content=ft.Row([ft.Icon(ft.Icons.ERROR, color="white"), ft.Text(message, color="white")])
            )
        ]
        self.update()

    def _build_rate_card(self, account, data):
        limit = data.get("limit", 0)
        remaining = data.get("remaining", 0)
        reset_ts = data.get("reset", 0)
        
        # Calculate usage
        used = limit - remaining
        percent = used / limit if limit > 0 else 0
        
        # Humanize time
        reset_dt = datetime.fromtimestamp(reset_ts)
        time_str = reset_dt.strftime("%H:%M")
        
        # Dynamic Colors
        bar_color = "#3fb950" # Green
        if percent > 0.5: bar_color = "#d29922" # Orange
        if percent > 0.75: bar_color = "#f85149"

        return ft.Container(
            bgcolor="#0d1117",
            border=ft.border.all(1, "#30363d"),
            border_radius=8,
            padding=20,
            content=ft.Column([
                # Header
                ft.Row([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.Icons.PERSON, color="white"),
                        ),
                        ft.Column([
                            ft.Text(f"@{account.username}", weight="bold", color="white"),
                            ft.Text("Core API", size=12, color="#8b949e")
                        ], spacing=2),
                    ]),
                    ft.Text(f"{remaining} / {limit}", color="white", weight="bold")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.ProgressBar(value=percent, color=bar_color, bgcolor="#21262d", height=8, border_radius=4),
                
                # Footer Stats
                ft.Row([
                    self._stat_pill(ft.Icons.REFRESH, f"Resets at {time_str}"),
                    self._stat_pill(ft.Icons.SPEED, f"{int(percent * 100)}% Used"),
                ], spacing=10)
            ], spacing=15)
        )
        
    def _build_loader_card(self) :
        return  ft.Container(
            bgcolor="#0d1117",
            border=ft.border.all(1, "#30363d"),
            border_radius=8,
            padding=20,
            content=ft.ProgressRing(color="#58a6ff" , height=25 , width=25),
            alignment=ft.alignment.center,
        )

    def _build_error_card(self, account, message):
        action_button = ft.OutlinedButton(
            "Reconnect", 
            icon=ft.Icons.LOGIN, 
            style=ft.ButtonStyle(color="#f85149", side={"": ft.BorderSide(1, "#f85149")}),
            height=30,
            on_click=lambda e,token=self.service.get_token(account.id) : self.page.open(Dialog(self.page).create_token(account.id , self.load_github_data) if not token else Dialog(self.page).edit_token(token , self.load_github_data)) 
        )

        return ft.Container(
            bgcolor="#0d1117",
            border=ft.border.all(1, "#f85149"), # Red border
            border_radius=8,
            padding=15,
            content=ft.Row([
                ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color="#f85149", size=30),
                ft.Column([
                    ft.Text(f"@{account.username}", weight="bold", color="white"),
                    ft.Text(message, color="#f85149", size=12, width=350, no_wrap=False),
                ], expand=True),
                action_button
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

    def _stat_pill(self, icon, text):
        return ft.Container(
            bgcolor="#161b22",
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            border_radius=4,
            content=ft.Row([
                ft.Icon(icon, size=12, color="#8b949e"),
                ft.Text(text, size=11, color="#8b949e")
            ], spacing=5)
        )

    def _build_placeholder(self, text):
        return ft.Container(
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=50),
            content=ft.Column([
                ft.Icon(ft.Icons.CONSTRUCTION, size=40, color="#8b949e"),
                ft.Text(text, color="#8b949e", size=16),
                ft.Text("We are working on adding this platform.", color="#484f58", size=12)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
        )



