import flet as ft
from core.general_service import GeneralService
from core.http.errors import AuthenticationError , RateLimitError , AuthorizationError
from core.platforms.github.github_service import GitHubService
from ui.components.dialogs import Dialog
from datetime import datetime
import os

class AccountsView(ft.Column):
    def __init__(self, service: GeneralService):
        super().__init__(expand=True)
        self.service = service
        
        self.spacing = 20
        self.scroll = ft.ScrollMode.AUTO 
        
        self.controls = [
            ft.Container(
                content=ft.ProgressRing(color="#58a6ff"),
                alignment=ft.alignment.center,
                padding=20
            )
        ]
        self.load_data()

    def load_data(self):
        data = self.service.get_all_active_accounts()
        
        stats = {
            "total": len(data),
            "active": sum(1 for d in data if self.check_activity(d)[0]),
            "last_connected": "None" if not data else "Recently"
        }
        
        self.controls = self.build_ui(data, stats)

    def build_ui(self, data, stats):
        # 1. Decide what to show in the "Content" area (List vs Empty State)
        if not data:
            content_area = self._build_empty_state()
        else:
            content_area = ft.Container(
                height=280, 
                content=ft.Column(
                    controls=self.build_account_cards(data),
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10
                ),
            )

        # 2. Return the full layout
        return [
            # Header
            ft.Column([
                ft.Text("Connected Accounts", size=24, weight=ft.FontWeight.BOLD, color="white"),
                ft.Text("Manage your connected platform accounts and authentication", size=14, color="#8b949e"),
            ], spacing=5),

            # The Dynamic Content Area (List OR Empty Message)
            content_area,

            # "Add New Account" Section (Always visible so user can fix empty state)
            ft.Container(
                bgcolor="#0d1117",
                border=ft.border.all(1, "#30363d"),
                border_radius=8,
                padding=30,
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(ft.Icons.ADD, color="#8b949e"),
                        bgcolor="#21262d",
                        padding=10,
                        border_radius=30
                    ),
                    ft.Text("Add New Account", weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text("Connect another platform account to expand your workflow", color="#8b949e", size=12),
                    ft.ElevatedButton(
                        "Connect Platform",
                        icon=ft.Icons.LINK,
                        color="white",
                        bgcolor="#1f6feb",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        height=35,
                        on_click=lambda e : self.page.open(self.handle_create_account())
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                alignment=ft.alignment.center
            ),

            # Account Statistics Section
            ft.Container(
                margin=ft.margin.only(top=10),
                content=ft.Column([
                    ft.Text("Account Statistics", weight=ft.FontWeight.BOLD, color="white", size=16),
                    ft.Row(
                        controls=[
                            self._build_stat_card("Total Connections", str(stats['total']), "active connections", ft.Icons.LINK),
                            self._build_stat_card("Active Platforms", str(stats['active']), "running services", ft.Icons.CHECK_CIRCLE),
                            self._build_stat_card("Last Connected", stats['last_connected'], "latest activity", ft.Icons.ACCESS_TIME_FILLED),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ], spacing=15)
            )
        ]

    def _build_empty_state(self):
        # Displays the broken link icon and text from your screenshot
        return ft.Container(
            height=280, # Match the height of the list view for consistency
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.LINK_OFF, size=60, color="#8b949e"), # The broken link icon
                    ft.Text("No accounts connected yet", size=18, color="#8b949e"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        )

    def build_account_cards(self, data):
        cards = []
        for d in data:
            is_active, status_msg = self.check_activity(d)
            status_color = "#3fb950" if is_active else "#d29922"
            status_text = "Active" if is_active else "Inactive"
            status_bg_opacity = 0.15

            card = ft.Container(
                bgcolor="#0d1117", 
                border=ft.border.all(1, "#30363d"),
                border_radius=8,
                padding=15,
                content=ft.Row([
                    ft.Row([
                        ft.Container(
                            bgcolor="#21262d", 
                            padding=8,
                            border_radius=6,
                            content=ft.Icon(ft.Icons.CODE, color="white", size=24)
                        ),
                        ft.Column([
                            ft.Row([
                                ft.Text(d[0].display_name, weight=ft.FontWeight.BOLD, color="white"),
                                ft.Container(
                                    content=ft.Text(status_text, size=10, color=status_color, weight=ft.FontWeight.BOLD),
                                    bgcolor=ft.Colors.with_opacity(status_bg_opacity, status_color),
                                    border=ft.border.all(1, status_color),
                                    border_radius=12,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=2)
                                )
                            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                            ft.Text(f"@{d[1].username}", color="#8b949e", size=12),
                            ft.Text(f"Connected {self.time_ago(d[1].created_at)} • {status_msg or 'Full Access'}", color="#8b949e", size=11),
                        ], spacing=2)
                    ]),
                    ft.Row([
                        ft.TextButton("Switch" if is_active else "Activate", style=ft.ButtonStyle(color="white" if is_active else "#58a6ff") , on_click= lambda e,ia=is_active,da=d :self.handle_activate_click(ia , da[0] , da[1])),
                        ft.TextButton("Remove", style=ft.ButtonStyle(color="#f85149") , on_click=lambda e : self.handle_remove_click(d[1])),
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )
            cards.append(card)
        return cards

    def _build_stat_card(self, title, value, subtext, icon):
        return ft.Container(
            expand=True,
            bgcolor="#0d1117",
            border=ft.border.all(1, "#30363d"),
            border_radius=8,
            padding=15,
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        bgcolor="#21262d", 
                        padding=5, 
                        border_radius=5, 
                        content=ft.Icon(icon, size=16, color="#58a6ff")
                    ),
                    ft.Text(title, color="#8b949e", size=12)
                ], spacing=10),
                ft.Text(str(value), size=24, weight=ft.FontWeight.BOLD, color="white"),
                ft.Text(subtext, size=11, color="#8b949e")
            ], spacing=5)
        )

    def check_activity(self, data):
        if not data[2]:
            return (False, "Token missing")
        try:
            expires = datetime.fromisoformat(data[2].expires_at)
            if expires < datetime.now():
                return (False, "Token expired")
        except:
            pass 
        return (True, None)

    def time_ago(self, date_str):
        try:
            dt = datetime.fromisoformat(date_str)
            delta = datetime.now() - dt
            if delta.days > 0: return f"{delta.days} days ago"
            hours = delta.seconds // 3600
            if hours > 0: return f"{hours} hours ago"
            return "Just now"
        except:
            return "Unknown"
        
    def handle_remove_click(self , account) :
        loader = ft.ProgressRing(visible=False)
        
        def close_dialog() :
            dialog.open = False
            self.page.update()
        
        def submit(e) :
            loader.visible = True
            self.page.update()
        
            self.service.delete_account(account)
            dialog.open = False
            
            loader.visible = False
            self.load_data()
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#22272e",
            title=ft.Text("Do you want remove this account ?" , color="#ffffff" , size=20),
            content=ft.Column(
                [
                    ft.Text("by deleting this account , all related data like token and events are also deleted"),
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
        
    def handle_create_account(self) :
        def close() :
            dialog.open = False
            self.page.update()
        
        widget = []
        platforms = self.service.get_all_data()[0]
        for platform in platforms :
            widget.append(
                ft.Container(
                    content=ft.Text(platform["platform"].display_name , size=15 , color="#ffffff"),
                    alignment=ft.alignment.center,
                    border_radius=15,
                    border=ft.Border(
                        ft.BorderSide(1 , ft.Colors.GREY),
                        ft.BorderSide(1 , ft.Colors.GREY),
                        ft.BorderSide(1 , ft.Colors.GREY),
                        ft.BorderSide(1 , ft.Colors.GREY),
                    ),
                    width=200,
                    padding=10,
                    on_click=lambda e,p=platform : click(p)
                )
            )
        
        dialog = ft.AlertDialog(
            title=ft.Text("Choose platform" , color="#ffffff" , size=20),
            modal=True,
            content=ft.Column(
                controls=widget,
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            actions=[
                ft.TextButton("cancel" , on_click=lambda e : close())
            ]
        )
        
        def click(platform) :
            new_dialog = Dialog(self.page).create_account(platform , self.load_data)
            self.page.open(new_dialog)
            dialog.open = False
            self.page.update()
            
        return dialog
    
    def handle_activate_click(self , is_active , platform , account) :
        if is_active :
            accounts = self.service.get_accounts(platform.id)
            accounts.remove(account)
            if not accounts :
                self.page.open(Dialog(self.page).create_account_v2(platform , self.load_data))
                self.page.update()
            else :
                def click(acc) :
                    self.service.activate_account(acc.id , platform.id)
                    dialog.open = False
                    self.load_data()
                    self.page.update()
                    
                def close():
                    dialog.open = False
                    self.page.update()
                
                widget = []
                for acc in accounts :
                    widget.append(
                        ft.Container(
                            content=ft.Text(acc.username , size=15 , color="#ffffff"),
                            alignment=ft.alignment.center,
                            border_radius=15,
                            border=ft.Border(
                                ft.BorderSide(1 , ft.Colors.GREY),
                                ft.BorderSide(1 , ft.Colors.GREY),
                                ft.BorderSide(1 , ft.Colors.GREY),
                                ft.BorderSide(1 , ft.Colors.GREY),
                            ),
                            width=200,
                            padding=10,
                            on_click=lambda e,a=acc: click(a)
                        )
                    )
                dialog = ft.AlertDialog(
                    title=ft.Text("Choose account" , color="#ffffff" , size=18 , weight=ft.FontWeight.BOLD),
                    modal=True,
                    bgcolor="#22272e",
                    content=ft.Container(
                        width=300,
                        content=ft.Column(
                            controls=widget,
                            tight=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10
                        ),
                    ),
                    actions=[
                        ft.TextButton("Cancel" , style=ft.ButtonStyle(color=ft.Colors.RED) , on_click=lambda e : close())
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                self.page.open(dialog)
            
        else :
            self.page.open(Dialog(self.page).create_token(account.id , self.load_data))
            

