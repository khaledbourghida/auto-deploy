import flet as ft
from ui.components.loaders import GlobalLoader
from ui.components.toasts import GlobalToast
from ui.pages.home_page import HomePage
from ui.pages.account_page import AccountPage
from ui.pages.settings_page import SettingPage

class AppShell(ft.Stack):
    def __init__(self, navigator):
        super().__init__(expand=True)
        self.navigator = navigator
        
        self.location = "home"
        
        self.sidebar = self._build_sidebar()
        
        self.loader = GlobalLoader()
        self.toast = GlobalToast()

        self.content_container = ft.Container(
            expand=10,
        )
        
        self.main_row = ft.Column(
            expand=True,
            controls=[self.sidebar, self.content_container],
        )

        self.controls = [
            self.main_row,
            self.loader,
            self.toast,
        ]
        
    def _update_sidebar_colors(self):
        self.home_text.color = ft.Colors.WHITE if self.location == "home" else ft.Colors.GREY
        self.accounts_text.color = ft.Colors.WHITE if self.location == "accounts" else ft.Colors.GREY
        self.settings_text.color = ft.Colors.WHITE if self.location == "settings" else ft.Colors.GREY
        self.about_text.color = ft.Colors.WHITE if self.location == "about" else ft.Colors.GREY


    def _build_sidebar(self):
        self.home_text = ft.Text("Home", size=15)
        self.accounts_text = ft.Text("accounts", size=15)
        self.settings_text = ft.Text("Settings", size=15)
        self.about_text = ft.Text("About", size=15)

        self._update_sidebar_colors()

        return ft.Container(
            expand=1,
            bgcolor="#161b22",
            padding=ft.Padding(20, 5, 20, 5),
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        alignment=ft.Alignment(0.0, 0.0),
                        bgcolor="#2f82f7",
                        border_radius=5,
                        height=25,
                        width=25,
                        content=ft.Icon(ft.Icons.CODE, color=ft.Colors.WHITE, size=15)
                    ),
                    ft.Text("AutoDeploy", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=15),
                ]),
                ft.Row([
                    ft.Container(on_click=lambda e: self.move("home"), content=self.home_text),
                    ft.Container(on_click=lambda e: self.move("accounts"), content=self.accounts_text),
                    ft.Container(on_click=lambda e: self.move("settings"), content=self.settings_text),
                    ft.Container(on_click=lambda e: self.move("about"), content=self.about_text),
                ], width=400, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(
                    width=100
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        )


    def set_content(self, content):
        self.content_container.content = content
        
    def show_sidebar(self):
        self.sidebar.visible = True
        self.sidebar.height = 100

    def hide_sidebar(self):
        self.sidebar.visible = False
        self.sidebar.height = 0
        
    def move(self, location: str):
        self.location = location
        self._update_sidebar_colors()

        if location == "home":
            self.navigator.push(HomePage(self.navigator))
        elif location == "accounts":
            self.navigator.push(AccountPage(self.navigator))
        elif location == "settings" :
            self.navigator.push(SettingPage(self.navigator))
        elif location == "about" :
            print("about")

        self.update()
