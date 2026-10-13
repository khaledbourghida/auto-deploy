import flet as ft
from core.general_service import GeneralService
from ui.components.dialogs import Dialog
from core.platforms.github.github_service import GitHubService

class GithubPage(ft.Column):
    def __init__(self, navigator , platform):
        super().__init__(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
        self.navigator = navigator
        self.platform = platform
        self.service = GeneralService()
        self.accounts = self.service.get_accounts(self.platform.id)
        self.active_account = self.service.get_active_account(self.platform.id)
        
        self.controls = self.build_ui(self.platform)
    
    def load(self):
        shell = self.navigator.shell
        shell.loader.show(self.page)

        try:
            self.platform = self.service.get_platform(self.platform.id)
            self.accounts = self.service.get_accounts(self.platform.id)
            self.active_account = self.service.get_active_account(self.platform.id)
        
            self.controls = self.build_ui(self.platform)
        finally:
            shell.loader.hide(self.page)
            self.update()

    def build_ui(self, platform) :
        return [
            ft.Container(
                expand=2,
                bgcolor="#161b22",
                padding=ft.Padding(40, 15, 40, 15),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        # LEFT — Platform identity
                        ft.Row(
                            spacing=15,
                            controls=[
                                ft.Container(
                                    alignment=ft.alignment.center,
                                    bgcolor=platform.bgcolor,
                                    border_radius=8,
                                    height=42,
                                    width=42,
                                    content=ft.Icon(
                                        ft.Icons.CODE,
                                        color=ft.Colors.WHITE,
                                        size=18,
                                    ),
                                ),
                                ft.Column(
                                    spacing=2,
                                    controls=[
                                        ft.Text(
                                            "GitHub",
                                            size=18,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.WHITE,
                                        ),
                                        ft.Text(
                                            "Manage repositories & workflows",
                                            size=12,
                                            color=ft.Colors.GREY,
                                        ),
                                    ],
                                ),
                            ],
                        ),

                        # RIGHT — Account / Actions
                        ft.Row(
                            spacing=20,
                            controls=[
                                # Account pill
                                ft.Container(
                                    padding=ft.Padding(10, 6, 10, 6),
                                    border_radius=20,
                                    bgcolor="#0d1117",
                                    border=ft.Border(
                                        ft.BorderSide(1 , "#30363d"),
                                        ft.BorderSide(1 , "#30363d"),
                                        ft.BorderSide(1 , "#30363d"),
                                        ft.BorderSide(1 , "#30363d"),
                                    ),
                                    on_click=lambda e: self.page.open(self.account_dialog()),
                                    content=(
                                        ft.Row(
                                            spacing=8,
                                            controls=[
                                                ft.CircleAvatar(
                                                    radius=10,
                                                    bgcolor="#2f82f7",
                                                    content=ft.Text(
                                                        self.active_account.username[0].upper(),
                                                        size=12,
                                                        color=ft.Colors.WHITE,
                                                    ),
                                                ),
                                                ft.Text(
                                                    self.active_account.username,
                                                    size=13,
                                                    color=ft.Colors.WHITE,
                                                ),
                                                ft.Icon(
                                                    ft.Icons.KEYBOARD_ARROW_DOWN,
                                                    size=16,
                                                    color=ft.Colors.GREY,
                                                ),
                                            ],
                                        )
                                        if platform.is_connected
                                        else ft.Row(
                                            spacing=6,
                                            controls=[
                                                ft.Icon(
                                                    ft.Icons.LINK,
                                                    size=16,
                                                    color="#2f82f7",
                                                ),
                                                ft.Text(
                                                    "Connect account",
                                                    size=13,
                                                    color="#2f82f7",
                                                ),
                                            ],
                                        )
                                    ),
                                ),

                                # Back button
                                ft.TextButton(
                                    "Back",
                                    on_click=lambda e: self.navigator.push_home(),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
            ),

            ft.Container(height=20),
            ft.Container(
                expand=10,
                alignment=ft.alignment.center,
                content=ft.Column([
                    ft.Text(spans=[
                        ft.TextSpan("Availibale " , style=ft.TextStyle(color="#ffffff")),
                        ft.TextSpan("Services" , style=ft.TextStyle(color="#2f82f7"))
                    ], size=35 ,),
                    ft.Text("Select a service to start with your GitHub operation" , size=15 , color=ft.Colors.GREY),
                    ft.Container(height=30),
                    ft.Row(
                        wrap=True,
                        spacing=10,
                        run_spacing=20,
                        controls=[
                            ft.Container(
                                width=320,
                                height=200,
                                alignment=ft.alignment.center,
                                border_radius=15,
                                padding=20,
                                bgcolor="#161b22",
                                content=ft.Column([
                                    ft.Row([
                                        ft.Container(
                                            bgcolor="#dbebff",
                                            height=42,
                                            width=32,
                                            alignment=ft.alignment.center,
                                            content=ft.Icon(ft.Icons.ADD , color="#2664eb" , size=20, weight=ft.FontWeight.BOLD),
                                            border_radius=10,
                                        ),
                                        ft.Container(
                                            alignment=ft.alignment.center,
                                            content=ft.Icon(ft.Icons.ARROW_FORWARD , color="#ffffff" , size=20,),
                                            on_click=lambda e : self.handle_services(GitHubService(self.active_account , self.navigator , self.page).create_repo)
                                        )
                                    ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ft.Text(
                                        value="Create Repository",
                                        color="#ffffff",
                                        size=20,
                                    ),
                                    ft.Text(
                                        "Create a new GitHub repository with custom settings",
                                        no_wrap=False,
                                        color=ft.Colors.GREY,
                                        size=15
                                    )
                                ], spacing=20)
                            ),
                            ft.Container(
                                width=320,
                                height=200,
                                alignment=ft.alignment.center,
                                border_radius=15,
                                padding=20,
                                bgcolor="#161b22",
                                content=ft.Column([
                                    ft.Row([
                                        ft.Container(
                                            bgcolor="#dcfce7",
                                            height=42,
                                            width=32,
                                            alignment=ft.alignment.center,
                                            content=ft.Icon(ft.Icons.SEARCH , color="#15a349" , size=20, weight=ft.FontWeight.BOLD),
                                            border_radius=10,
                                        ),
                                        ft.Container(
                                            alignment=ft.alignment.center,
                                            content=ft.Icon(ft.Icons.ARROW_FORWARD , color="#ffffff" , size=20,),
                                            on_click=lambda e : print("get repo")
                                        )
                                    ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ft.Text(
                                        value="Get Repository",
                                        color="#ffffff",
                                        size=20,
                                    ),
                                    ft.Text(
                                        "Retrieve repository information and details",
                                        no_wrap=False,
                                        color=ft.Colors.GREY,
                                        size=15
                                    )
                                ], spacing=20)
                            ),
                            ft.Container(
                                width=320,
                                height=200,
                                alignment=ft.alignment.center,
                                border_radius=15,
                                padding=20,
                                bgcolor="#161b22",
                                content=ft.Column([
                                    ft.Row([
                                        ft.Container(
                                            bgcolor="#f3e8ff",
                                            height=42,
                                            width=32,
                                            alignment=ft.alignment.center,
                                            content=ft.Icon(ft.Icons.LIST , color="#9234eb" , size=20, weight=ft.FontWeight.BOLD),
                                            border_radius=10,
                                        ),
                                        ft.Container(
                                            alignment=ft.alignment.center,
                                            content=ft.Icon(ft.Icons.ARROW_FORWARD , color="#ffffff" , size=20,),
                                            on_click=lambda e : print("list repos")
                                        )
                                    ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ft.Text(
                                        value="List Repositories",
                                        color="#ffffff",
                                        size=20,
                                    ),
                                    ft.Text(
                                        "View all repositories for a user or organization",
                                        no_wrap=False,
                                        color=ft.Colors.GREY,
                                        size=15
                                    )
                                ], spacing=20)
                            ),
                            ft.Container(
                                width=320,
                                height=200,
                                alignment=ft.alignment.center,
                                border_radius=15,
                                padding=20,
                                bgcolor="#161b22",
                                content=ft.Column([
                                    ft.Row([
                                        ft.Container(
                                            bgcolor="#ffe3e3",
                                            height=42,
                                            width=32,
                                            alignment=ft.alignment.center,
                                            content=ft.Icon(ft.Icons.DELETE , color="#db2525" , size=20, weight=ft.FontWeight.BOLD),
                                            border_radius=10,
                                        ),
                                        ft.Container(
                                            alignment=ft.alignment.center,
                                            content=ft.Icon(ft.Icons.ARROW_FORWARD , color="#ffffff" , size=20,),
                                            on_click=lambda e : print("delete repo")
                                        )
                                    ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ft.Text(
                                        value="Delete Repository",
                                        color="#ffffff",
                                        size=20,
                                    ),
                                    ft.Text(
                                        "Permanetly delete a repository",
                                        no_wrap=False,
                                        color=ft.Colors.GREY,
                                        size=15
                                    )
                                ], spacing=20)
                            ),
                        ]
                        
                    )
                ]),
                padding=ft.Padding(80,0,80,0),
            ),
        ]
    
    def account_dialog(self) :
        def close_dialog() :
            dialog.open = False
            self.page.update()
            
        no_account = ft.Container(
            alignment=ft.alignment.center,
            padding=20,
            expand=True,
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.LINK_OFF, size=30, color=ft.Colors.GREY),
                    ft.Text("No accounts connected yet", size=13, color=ft.Colors.GREY),
                    ft.ElevatedButton(
                        "Create Account",
                        bgcolor="#2f82f7",
                        color="#ffffff",
                        on_click=lambda e: self.create_account(),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        with_account = [
            ft.Container(
                bgcolor="#3a4048",
                border_radius=15,
                expand=True,
                padding=10,
                content=ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.PERSON, color="#ffffff"),
                                ft.Text(
                                    spans=[
                                        ft.TextSpan(
                                            f"{account.username}\n",
                                            style=ft.TextStyle(
                                                color="#ffffff",
                                                weight=ft.FontWeight.BOLD,
                                                size=15,
                                            ),
                                        ),
                                        ft.TextSpan(
                                            account.email,
                                            style=ft.TextStyle(
                                                color=ft.Colors.GREY, size=13
                                            ),
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                on_click=lambda e, a=account : self.activate_account(a.id , close_dialog)
            )
            for account in self.accounts
        ]

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#22272e",
            title=ft.Text(
                f"Create New Account",
                color="#ffffff",
                size=20,
            ),
            content=ft.Column(
                controls=[
                    ft.Column(
                        controls=with_account,
                        scroll=ft.ScrollMode.AUTO,
                        expand=6,
                    ),
                    ft.Divider(height=1, color=ft.Colors.GREY),
                    ft.Container(
                        alignment=ft.alignment.center_left,
                        content=ft.Text(
                            "+ Add Github Account",
                            color="#2f82f7",
                            size=15,
                        ),
                        on_click=lambda e: self.create_account(),
                    ),
                ]
                if len(self.accounts) > 0
                else [no_account]
            ),

            actions=[
                ft.TextButton("Cancel", on_click=lambda e:close_dialog()),
            ],
        )
        
        return dialog
        
    def create_account(self) :
        print(self.platform)
        dialog = Dialog(self.page).create_account({ "platform" : self.platform.display_name, "platform_id" : self.platform.id,} , self.load)
        self.page.open(dialog)
        
    def activate_account(self , account_id , func) :
        if not self.platform.is_connected :
            self.service.connect_platform(self.platform.id)
        self.service.activate_account(account_id , self.platform.id)
        func()
        self.load()
        
    def handle_services(self , service_func) :
        if not self.platform.is_connected :
            self.page.open(self.account_dialog())
            return
        else:
            token = self.service.get_token(self.active_account.id)
            if token:
                print(token.expires_at)
                dialog = Dialog(self.page).create_repo_dialog(service_func)
                self.page.open(dialog)
                
            else:
                dialog = Dialog(self.page).create_token(self.active_account.id , self.load)
                self.page.open(dialog)
        