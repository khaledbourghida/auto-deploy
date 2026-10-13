import flet as ft
from core.general_service import GeneralService
from ui.pages.github_page import GithubPage
from ui.theme import AppTheme

class HomePage(ft.Column):
    def __init__(self, navigator):
        super().__init__(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.navigator = navigator
        self.general_service = GeneralService()
        self.platforms = self.general_service.platforms
        
        self.controls = [
            ft.Container(height=30),
            ft.Text(
                spans=[
                    ft.TextSpan("Automate Your " , style=ft.TextStyle(color=ft.Colors.WHITE)),
                    ft.TextSpan(
                        "Development", 
                        style=ft.TextStyle(color="#2f82f7")
                    ),
                    ft.TextSpan(" Workflow" , style=ft.TextStyle(color=ft.Colors.WHITE)),
                ],
                size=40,
                weight=ft.FontWeight.BOLD
            ),
            ft.Text(
                "Connect and automate popular development platforms through powerful APIs.",
                color=ft.Colors.GREY,
                size=15
            ),
            ft.Text(
                "Streamline your workflow with GitHub, Netlify, Render, and more.",
                color=ft.Colors.GREY,
                size=15
            ),
            ft.Container(height=20),
            ft.Row([
                ft.Button(
                    icon=ft.Icons.LINK,
                    text="Connect a Platform",
                    color=ft.Colors.WHITE,
                    bgcolor="#2f82f7",
                    width=200,
                    height=40,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                ),
                ft.Button(
                    text="View Documentation",
                    color=ft.Colors.WHITE,
                    bgcolor="#0d1117",
                    width=200,
                    height=40,
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(1, ft.Colors.GREY),
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                )
            ],alignment=ft.MainAxisAlignment.SPACE_EVENLY , width=430),
            ft.Container(height=50),
            ft.Text(
                "Supported Platforms",
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD,
                size=25
            ),
            ft.Text(
                "Connect with your favorite development tools and services",
                color=ft.Colors.GREY,
                size=15
            ),
            ft.Row(
                wrap=True,
                spacing=10,
                run_spacing=20,
                controls=[
                    ft.Container(
                        width=320,
                        height=200,
                        bgcolor="#22272e",
                        padding=20,
                        border_radius=10,
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    width=40,
                                    height=40,
                                    content=ft.Image(src=f"{platform.icon}.png" , height=30 , width=30),
                                    bgcolor= platform.bgcolor,
                                    alignment=ft.alignment.center,
                                    border_radius=10
                                ),
                                ft.Container(width=5),
                                ft.Text(
                                    spans=[
                                        ft.TextSpan(f"{platform.display_name}\n" , style=ft.TextStyle(color=ft.Colors.WHITE , weight=ft.FontWeight.W_700 , size=15)),
                                        ft.TextSpan(f"{platform.subtitle}" , style=ft.TextStyle(color=ft.Colors.GREY , size=13))
                                    ]
                                )
                            ]),
                            ft.Text(
                                f"{platform.desc}",
                                color=ft.Colors.GREY,
                                size=13,
                                no_wrap=False
                            ),
                            ft.Row([
                                ft.Button(
                                    text="Connected" if platform.is_connected else "Available",
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREEN if platform.is_connected else "#4c5663",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=5),
                                        padding=5
                                    ),
                                    
                                ),
                                ft.Container(
                                    alignment=ft.alignment.center,
                                    # padding=5,
                                    content=ft.Icon(
                                        ft.Icons.ARROW_FORWARD,
                                        color="#2f82f7",
                                        size=20,
                                    ),
                                    on_click=lambda e, p=platform: self.platform_navigator(p)
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ] , spacing=20)
                    ) for platform in self.platforms
                ]
            ),
            ft.Container(height=50),
            ft.Row(
                spacing=25,
                controls=[
                    ft.Container(
                        width=350,
                        border_radius=15,
                        height=200,
                        padding=20,
                        bgcolor="#22272e",
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    bgcolor="#2f82f7",
                                    content=ft.Icon(ft.Icons.SETTINGS , color=ft.Colors.WHITE),
                                    height=35,
                                    width=35,
                                    alignment=ft.alignment.center,
                                    border_radius=5
                                ),
                                ft.Text("Settings" , color=ft.Colors.WHITE , weight=ft.FontWeight.BOLD , size=18)
                            ], spacing=20),
                            ft.Text(
                                "Configure API parameters, set up authentication, and customize you automation workflow",
                                color=ft.Colors.GREY,
                                size=15
                            ),
                            ft.Container(
                                content=ft.Row([
                                    ft.Text("Manage Settings" , color="#2f82f7" , size=17),
                                    ft.Icon(ft.Icons.ARROW_FORWARD , color="#2f82f7" , size=17),
                                    
                                ] , spacing=15),
                                on_click=lambda e : self.navigator.shell.move("settings")
                            )
                        ] , spacing=20)
                    ),
                    ft.Container(
                        width=350,
                        border_radius=15,
                        height=200,
                        padding=20,
                        bgcolor="#22272e",
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    bgcolor="#2f82f7",
                                    content=ft.Icon(ft.Icons.PERSON_3 , color=ft.Colors.WHITE),
                                    height=35,
                                    width=35,
                                    alignment=ft.alignment.center,
                                    border_radius=5
                                ),
                                ft.Text("Accounts" , color=ft.Colors.WHITE , weight=ft.FontWeight.BOLD , size=18)
                            ], spacing=20 ),
                            ft.Text(
                                "Explore all your integrated accounts, view account status, and check your account credentail.",
                                color=ft.Colors.GREY,
                                size=15
                            ),
                            ft.Container(
                                content=ft.Row([
                                    ft.Text("Browse Accounts" , color="#2f82f7" , size=17),
                                    ft.Icon(ft.Icons.ARROW_FORWARD , color="#2f82f7" , size=17),
                                    
                                ] , spacing=15),
                                
                            )
                        ] , spacing=20),
                        on_click=lambda e : self.navigator.shell.move("accounts")
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Container(height=50),
            ft.Text(
                "Ready to Automate Your Workflow?",
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD,
                size=35,
            ),
            ft.Text(
                "Join thousands of developers who are already automating their development processes with",
                color=ft.Colors.GREY,
                size=15,
            ),
            ft.Text(
                "AutoDeploy",
                color=ft.Colors.GREY,
                size=15
            ),
            ft.Container(height=30),
            ft.Button(
                icon=ft.Icons.ROCKET,
                text="Start Automating Now",
                color=ft.Colors.WHITE,
                width=250,
                height=50,
                style=ft.ButtonStyle(
                    alignment=ft.alignment.center,
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
                bgcolor="#2f82f7"
            ),
            ft.Container(height=30),
            ft.Container(
                padding = 20,
                bgcolor="#22272e",
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            bgcolor="#2f82f7",
                            width=30,
                            height=30,
                            border_radius=5,
                            alignment=ft.alignment.center,
                            content=ft.Icon(ft.Icons.CODE , color=ft.Colors.WHITE , size=15)
                        ),
                        ft.Text(
                            "AutoDeploy",
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.BOLD,
                            size=20
                        )
                    ] , spacing=10 , alignment=ft.MainAxisAlignment.CENTER),
                    ft.Column([
                        ft.Text(
                            "We believe developer automation should be simple, powerful, and accessible to",
                            color="#878e91",
                            size=13,
                        ),
                        ft.Text(
                            "everyone.Our mission is to eliminate repetitive tasks so you can focus on what matters",
                            color="#878e91",
                            size=13,
                        ),
                        ft.Text(
                            "most - building amazing software.",
                            color="#878e91",
                            size=13,
                        ),
                        ft.Container(height=20),
                        ft.Divider(
                            height=1,
                            color=ft.Colors.GREY,
                        ),
                        ft.Container(height=10),
                        ft.Text(
                            "© 2024 AutoDeploy. Making development workflow effortless.",
                            color="#343d48",
                            size=10,
                        ),
                        ft.Container(height=10)
                    ] , spacing=10 , alignment=ft.MainAxisAlignment.CENTER)
                ] , spacing=15 , alignment=ft.MainAxisAlignment.CENTER),
                alignment=ft.alignment.center
            )
        ]
        
    def platform_navigator(self , platform) :
        if platform.name == "github" :
            self.navigator.push_fullscreen(GithubPage(self.navigator , platform))
        else :
            print(platform.name)
