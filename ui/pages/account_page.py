import flet as ft
from core.general_service import GeneralService
from ui.components.dialogs import Dialog
from typing import List

class AccountPage(ft.Column):
    def __init__(self, navigator):
        super().__init__(expand=True, scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.navigator = navigator
        self.service = GeneralService()
        self.content = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.controls = [self.content]

    def did_mount(self):
        self.load()

    def load(self):
        shell = self.navigator.shell
        shell.loader.show(self.page)

        try:
            all_data = self.service.get_all_data()
            data = all_data[0]
            num_accounts = all_data[1]
            self.content.controls = self.build_ui(data, num_accounts)
        finally:
            shell.loader.hide(self.page)
            self.update()

    def build_ui(self, data: List, num_accounts):
        return [
            # --- Header Section ---
            ft.Container(
                alignment=ft.alignment.center_left,
                content=ft.Column([
                    ft.Text("Connected Accounts", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text("Manage all your platforms accounts in one place. Connect new accounts or manage existing ones.", 
                           color=ft.Colors.WHITE54, size=15),
                ], spacing=5),
                padding=ft.padding.symmetric(horizontal=80, vertical=0),
            ),
            
            ft.Container(height=20),

            # --- Statistics Section ---
            ft.Container(
                content=ft.Row([
                    self._build_stat_card("Total Platforms", len(data), ft.Icons.LAYERS, ["#2f82f7", "#0d47a1"]),
                    self._build_stat_card("Connected Accounts", num_accounts, ft.Icons.LINK, ["#a855f7", "#6b21a8"]),
                ], expand=True, spacing=20),
                padding=ft.padding.symmetric(horizontal=80),
                expand=True
            ),

            ft.Container(height=30),

            # --- All Accounts Title ---
            ft.Container(
                alignment=ft.alignment.center_left,
                content=ft.Row([
                     ft.Text("All Accounts", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                     ft.Container(
                         content=ft.Text(f"{len(data)}", size=12, color=ft.Colors.WHITE),
                         padding=ft.padding.all(6),
                         bgcolor=ft.Colors.WHITE10,
                         border_radius=20
                     )
                ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.symmetric(horizontal=80),
            ),
            
            ft.Container(height=10),

            # --- Platform Cards Grid ---
            ft.Container(
                alignment=ft.alignment.center_left,
                padding=ft.padding.symmetric(horizontal=80),
                content=ft.Row(
                    wrap=True,
                    spacing=20,
                    run_spacing=20,
                    controls=[
                        self._build_platform_card(platform) for platform in data
                    ]
                ),
            ),
            ft.Container(height=50)
        ]

    def _build_stat_card(self, title, count, icon, gradient_colors):
        return ft.Container(
            padding=25,
            expand=1,
            border_radius=16,
            bgcolor="#22272e",
            border=ft.border.all(1, "#30363d"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            ),
            content=ft.Column([
                ft.Row([
                    ft.Text(title, color=ft.Colors.WHITE70, size=16, weight=ft.FontWeight.W_500),
                    ft.Container(
                        content=ft.Icon(icon, color=ft.Colors.WHITE, size=18),
                        padding=8,
                        border_radius=10,
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=gradient_colors
                        )
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=10),
                ft.Text(
                    f"{count}",
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                    size=32
                ),
            ])
        )

    def _build_platform_card(self, platform):
        active_accounts = len(platform["accounts"])
        platform_data = platform["platform"]
        is_active = active_accounts > 0
        
        return ft.Container(
            padding=0, # Padding handled inside
            alignment=ft.alignment.center,
            width=345,
            height=420,
            bgcolor="#22272e",
            border_radius=16,
            border=ft.border.all(1, "#30363d"),
            shadow=ft.BoxShadow(
                blur_radius=15,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 5)
            ),
            content=ft.Column(
                spacing=0,
                controls=[
                    # Card Header
                    ft.Container(
                        padding=20,
                        content=ft.Row(
                            controls=[
                                ft.Row([
                                    ft.Container(
                                        alignment=ft.alignment.center,
                                        border_radius=12,
                                        content=ft.Image(src=f"{platform_data.icon}.png" , height=45 , width=45),
                                        gradient=ft.LinearGradient(
                                            begin=ft.alignment.top_left,
                                            end=ft.alignment.bottom_right,
                                            colors=["#2f82f7", "#0d47a1"]
                                        ),
                                        width=45,
                                        height=45,
                                        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.4, "#2f82f7"))
                                    ),
                                    ft.Column([
                                        ft.Text(f"{platform_data.display_name}", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.WHITE),
                                        ft.Text(f"{active_accounts} accounts connected", size=12, color=ft.Colors.WHITE54)
                                    ], spacing=2)
                                ]),
                                ft.Container(
                                    border_radius=30,
                                    bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.GREEN) if is_active else ft.Colors.with_opacity(0.1, ft.Colors.GREY),
                                    border=ft.border.all(1, ft.Colors.GREEN if is_active else ft.Colors.GREY_700),
                                    content=ft.Text(
                                        "Active" if is_active else "Inactive", 
                                        color=ft.Colors.GREEN_400 if is_active else ft.Colors.GREY_400, 
                                        size=11, 
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    alignment=ft.alignment.center,
                                    padding=ft.padding.symmetric(horizontal=10, vertical=4)
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True
                        )
                    ),
                    ft.Divider(height=1, color="#30363d"),
                    
                    # Card Body (List)
                    ft.Container(
                        expand=True,
                        padding=10,
                        content=ft.Column(
                            scroll=ft.ScrollMode.AUTO,
                            controls=self.account_state(platform),
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                    ),

                    # Card Footer (Add Button)
                    ft.Container(visible=is_active), # Spacer if active
                    ft.Column([
                        ft.Divider(height=1, color="#30363d"),
                        ft.Container(
                            alignment=ft.alignment.center,
                            padding=15,
                            content=ft.Row([
                                ft.Icon(ft.Icons.ADD_ROUNDED, color="#2f82f7", size=18),
                                ft.Text(f"Add {platform_data.display_name} Account", color="#2f82f7", weight=ft.FontWeight.W_600, size=14),
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            on_click=lambda e, p=platform: self.create_account(p),
                            ink=True,
                            border_radius=ft.border_radius.only(bottom_left=16, bottom_right=16)
                        )
                    ]) if is_active else ft.Container()
                ],
            )
        )

    def account_state(self, platform):
        controls = []

        if len(platform["accounts"]) > 0:
            for account in platform["accounts"]:
                controls.append(
                    ft.Container(
                        bgcolor="#2d333b", # Slightly lighter than card bg
                        border_radius=12,
                        border=ft.border.all(1, ft.Colors.with_opacity(0.05, ft.Colors.WHITE)),
                        padding=12,
                        on_click=lambda e: self.page.open(self.handle_account_options(account)),
                        content=ft.Row([
                            ft.Row([
                                ft.Container(
                                    content=ft.Icon(ft.Icons.PERSON, color="#ffffff", size=18),
                                    bgcolor=ft.Colors.WHITE10,
                                    width=36, height=36,
                                    border_radius=18,
                                    alignment=ft.alignment.center
                                ),
                                ft.Column([
                                    ft.Text(account.username, weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.WHITE),
                                    ft.Text(account.email, color=ft.Colors.WHITE54, size=11, overflow=ft.TextOverflow.ELLIPSIS)
                                ], spacing=2, width=180) # Constrain width
                            ]),
                            ft.Icon(ft.Icons.MORE_VERT_ROUNDED, color=ft.Colors.WHITE54, size=20)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    )
                )
        else:
            controls.append(
                ft.Container(
                    alignment=ft.alignment.center,
                    expand=True,
                    content=ft.Column([
                        ft.Container(
                            content=ft.Icon(ft.Icons.LINK_OFF_ROUNDED, size=40, color=ft.Colors.WHITE24),
                            padding=20,
                            border_radius=50,
                            bgcolor=ft.Colors.WHITE10
                        ),
                        ft.Text("No accounts connected", size=14, color=ft.Colors.WHITE54),
                        ft.Container(height=5),
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.ADD, size=16),
                                ft.Text(f"Connect {platform['platform'].display_name}")
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            style=ft.ButtonStyle(
                                bgcolor="#2f82f7",
                                color="#ffffff",
                                shape=ft.RoundedRectangleBorder(radius=10),
                                elevation=0
                            ),
                            on_click=lambda e: self.create_account(platform),
                            height=40,
                            width=200
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15)
                )
            )

        return controls

    def handle_account_options(self, account):
        self.action_sheet = ft.CupertinoActionSheet(
            title=ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column([
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=40, color=ft.Colors.WHITE),
                    ft.Text(f"{account.username}", size=18, weight=ft.FontWeight.BOLD, color="#ffffff")
                ])
            ),
            message=ft.Container(
                alignment=ft.alignment.center,
                content=ft.Text("Manage this account settings", size=14, color=ft.Colors.GREY),
            ),
            cancel=ft.CupertinoActionSheetAction(
                content=ft.Text("Cancel", color=ft.Colors.BLUE),
                on_click=lambda e: self.page.close(self.bottom_sheet),
            ),
            actions=[
                ft.CupertinoActionSheetAction(
                    content=ft.Text("Activate Account"),
                    on_click=lambda e: self.handle_click(self.service.activate_account(account.id, account.platform_id), False),
                ),
                ft.CupertinoActionSheetAction(
                    content=ft.Text("Deactivate Account"),
                    on_click=lambda e: self.handle_click(self.service.deactivate_account(account.platform_id), False),
                ),
                ft.CupertinoActionSheetAction(
                    content=ft.Text("Delete Account", color=ft.Colors.RED),
                    is_destructive_action=True,
                    on_click=lambda e: self.handle_click(self.service.delete_account(account), True),
                ),
            ],
        )
        self.bottom_sheet = ft.CupertinoBottomSheet(self.action_sheet)
        return self.bottom_sheet

    def handle_click(self, func, is_delete):
        self.navigator.shell.loader.show(self.page)
        func
        self.navigator.shell.loader.hide(self.page)
        if is_delete:
            self.load()
        self.page.close(self.bottom_sheet)
    
    def create_account(self, platform):
        print(platform)
        dialog = Dialog(self.page).create_account_v2(platform["platform"], self.load)
        self.page.open(dialog)