import flet as ft
from datetime import datetime
from core.general_service import GeneralService
from data.models import Account, Token
import threading
import webbrowser
from core.http.errors import AuthenticationError , ValidationError

class Dialog:
    def __init__(self, page: ft.Page):
        self.page = page
        
    def failed_operation(self , text : str) -> ft.AlertDialog:
        def close_dailog() :
            dialog.open = False
            self.page.update()
        dialog = ft.AlertDialog(
            title=ft.Icon(ft.Icons.ERROR , color=ft.Colors.RED),
            content=ft.Text(text),
            actions=[
                ft.TextButton("Try again" , on_click= lambda e:close_dailog()),
            ]
        )
        return dialog

    def success_operation(self, text : str) -> ft.AlertDialog :
        def close_dialog() :
            dialog.open = False
            self.page.update()
        dialog = ft.AlertDialog(
            title=ft.Icon(ft.Icons.DONE , color=ft.Colors.GREEN),
            content=ft.Text(text),
            actions=[
                ft.TextButton("done" , on_click= lambda e:close_dialog()),
            ]
        )
        return dialog
    
    def open_link_dialog(self, url : str , title : str) :
        def close_dialog() :
            dialog.open = False
            self.page.update()
        def open_link() :
            webbrowser.open(url)
            dialog.open = False
            self.page.update()
            
        dialog = ft.AlertDialog(
            title=ft.Text(title , color=ft.Colors.WHITE),
            content=ft.Column([
                ft.Text("Click here to open it :" , color=ft.Colors.WHITE),
                ft.Container(
                    content=ft.Text(url , color="#2f82f7"),
                    on_click=lambda e : open_link()
                ),
            ]),
            actions=[
                ft.TextButton("done" , on_click= lambda e:close_dialog()),
            ]
        )
        return dialog

    def create_account(self, platform , func):
        username_tf = ft.TextField(
            label="Username",
            autofocus=True,
        )

        email_tf = ft.TextField(
            label="Email (optional)"
        )

        active_cb = ft.Checkbox(
            label="Set as active account",
            value=True
        )

        loader = ft.ProgressRing(visible=False)

        def submit(e):
            if not username_tf.value:
                username_tf.error_text = "Username is required"
                self.page.update()
                return
            if not email_tf.value :
                email_tf.error_text = "Email is required"
                self.page.update()
                return

            loader.visible = True
            self.page.update()

            account = Account(
                id=None,
                platform_id=platform["platform_id"],
                username=username_tf.value,
                email=email_tf.value,
                avatar_url=None,
                is_active=1 if active_cb.value else 0,
                created_at=datetime.utcnow().isoformat()
            )

            try:
                GeneralService().create_account(account, platform["platform_id"] , account.is_active)
                dialog.open = False
            finally:
                loader.visible = False
                func()
                self.page.update()
            
        def close_dialog() :
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#22272e",
            title=ft.Text(
                f'Create New Account ({platform["platform"]})',
                color="#ffffff",
                size=20,
            ),
            content=ft.Column(
                [
                    username_tf,
                    email_tf,
                    active_cb,
                    ft.Row([loader], alignment=ft.MainAxisAlignment.CENTER),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e:close_dialog()),
                ft.ElevatedButton(
                    "Create",
                    bgcolor="#2f82f7",
                    color="#ffffff",
                    on_click=submit,
                ),
            ],
        )

        return dialog
    
    def create_account_v2(self, platform , func):
        username_tf = ft.TextField(
            label="Username",
            autofocus=True,
        )

        email_tf = ft.TextField(
            label="Email (optional)"
        )

        active_cb = ft.Checkbox(
            label="Set as active account",
            value=True
        )

        loader = ft.ProgressRing(visible=False)

        def submit(e):
            if not username_tf.value:
                username_tf.error_text = "Username is required"
                self.page.update()
                return
            if not email_tf.value :
                email_tf.error_text = "Email is required"
                self.page.update()
                return

            loader.visible = True
            self.page.update()

            account = Account(
                id=None,
                platform_id=platform.id,
                username=username_tf.value,
                email=email_tf.value,
                avatar_url=None,
                is_active=1 if active_cb.value else 0,
                created_at=datetime.utcnow().isoformat()
            )

            try:
                GeneralService().create_account(account, platform.id , account.is_active)
                dialog.open = False
            finally:
                loader.visible = False
                func()
                self.page.update()
            
        def close_dialog() :
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#22272e",
            title=ft.Text(
                f"Create New Account ({platform.display_name})",
                color="#ffffff",
                size=20,
            ),
            content=ft.Column(
                [
                    username_tf,
                    email_tf,
                    active_cb,
                    ft.Row([loader], alignment=ft.MainAxisAlignment.CENTER),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e:close_dialog()),
                ft.ElevatedButton(
                    "Create",
                    bgcolor="#2f82f7",
                    color="#ffffff",
                    on_click=submit,
                ),
            ],
        )

        return dialog
    
    def create_repo_dialog(self, func) -> ft.AlertDialog:
        """
        UI Component for creating a repository.
        'func' is the bound method: service.create_repo
        """
        # --- UI ELEMENTS ---
        name_tf = ft.TextField(
            label="Repository Name", 
            hint_text="e.g., my-project",
            autofocus=True, 
            text_size=14,
            border_color="#30363d"
        )
        desc_tf = ft.TextField(
            label="Description (optional)", 
            multiline=True, 
            max_lines=3, 
            text_size=14,
            border_color="#30363d"
        )
        visibility_dd = ft.Dropdown(
            label="Visibility",
            options=[
                ft.dropdown.Option("Public"),
                ft.dropdown.Option("Private"),
            ],
            value="Public",
            text_size=14,
            border_color="#30363d"
        )
        
        loader = ft.ProgressRing(visible=False, width=20, height=20, color="#2f82f7")
        error_text = ft.Text(color=ft.Colors.RED, size=12, visible=False)

        def close_dialog():
            dialog.open = False
            self.page.update()

        # --- BACKGROUND WORKER (Async/Thread) ---
        def run_service_call():
            try:
                # 1. Prepare Data
                is_private = (visibility_dd.value == "Private")
                
                # 2. Call Service (Service owns validation & logic)
                result = func(
                    name=name_tf.value,
                    description=desc_tf.value,
                    private=is_private
                )
                
                # 3. Handle SUCCESS
                dialog.open = False
                self.page.update()
                
                # Show success feedback (Toast/SnackBar)
                snack_bar = ft.SnackBar(
                    content=ft.Text(f"Repository '{result.get('name')}' created successfully!" , color=ft.Colors.BLACK , size=15),
                    bgcolor="#238636" # GitHub Green
                )
                self.page.open(snack_bar)
                self.page.update()

            # 4. Handle ERRORS (Mapped Cleanly)
            except ValidationError as e:
                # Specific UI field error
                name_tf.error_text = str(e)
                name_tf.update()
                loader.visible = False
                loader.update()
                
            except AuthenticationError as e:
                # Critical Auth Fail -> Close Dialog -> Maybe Redirect
                error_text.value = str(e)
                error_text.visible = True
                loader.visible = False
                self.page.update()

            except Exception as e:
                # Generic fallback for Network/API/System errors
                error_text.value = "Network or System errors , try again later"
                error_text.visible = True
                loader.visible = False
                self.page.update()

        # --- SUBMIT ACTION ---
        def submit(e):
            # 0. Basic UI Guard (Empty Check)
            if not name_tf.value:
                name_tf.error_text = "Repository name is required"
                name_tf.update()
                return
            
            # 1. Update State -> Loading
            name_tf.error_text = None
            error_text.visible = False
            loader.visible = True
            self.page.update()

            # 2. Trigger Worker
            threading.Thread(target=run_service_call, daemon=True).start()

        # --- DIALOG STRUCTURE ---
        dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#22272e",
            title=ft.Text("Create Repository", color="#ffffff", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                width=400,
                content=ft.Column(
                    [
                        name_tf,
                        desc_tf,
                        visibility_dd,
                        ft.Container(height=10),
                        # Error area
                        ft.Row([error_text], alignment=ft.MainAxisAlignment.CENTER),
                        # Loader area
                        ft.Row([loader], alignment=ft.MainAxisAlignment.CENTER),
                    ],
                    tight=True,
                )
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dialog(), style=ft.ButtonStyle(color=ft.Colors.GREY)),
                ft.ElevatedButton(
                    "Create Repository", 
                    bgcolor="#238636", 
                    color="#ffffff", 
                    on_click=submit
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return dialog
        
    def create_token(self, account_id, func):
        github_token = ft.TextField(
            label="GitHub Token",
            autofocus=True,
        )

        selected_datetime = {"value": None}
        
        error_text = ft.Text("please add the expired date" , color=ft.Colors.RED , visible=False)

        expire_text = ft.Text("Expire At: Not set", color=ft.Colors.GREY)

        loader = ft.ProgressRing(visible=False)

        # --- Date & Time Pickers ---
        def on_date_picked(e):
            if e.control.value:
                selected_datetime["date"] = e.control.value
                open_time_picker()

        def on_time_picked(e):
            if e.control.value:
                date = selected_datetime["date"]
                time = e.control.value
                dt = datetime(
                    date.year, date.month, date.day,
                    time.hour, time.minute
                )
                selected_datetime["value"] = dt
                expire_text.value = f"Expire At: {dt.strftime('%Y-%m-%d %H:%M')}"
                expire_text.color = ft.Colors.WHITE
                self.page.update()

        date_picker = ft.DatePicker(on_change=on_date_picked)
        time_picker = ft.TimePicker(on_change=on_time_picked)

        self.page.overlay.extend([date_picker, time_picker])

        def open_date_picker(e):
            date_picker.open = True
            self.page.update()

        def open_time_picker():
            time_picker.open = True
            self.page.update()

        def close_dialog():
            dialog.open = False
            self.page.update()

        def submit(e):
            if not github_token.value:
                github_token.error_text = "Token is required"
                self.page.update()
                return

            if not selected_datetime["value"] :
                error_text.visible = True
                self.page.update()
                return

            loader.visible = True
            self.page.update()

            token = Token(
                id=None,
                account_id=account_id,
                token_encrypted=github_token.value,
                token_type="GitHub Access Token",
                expires_at=(
                    selected_datetime["value"].isoformat()
                    if selected_datetime["value"]
                    else None
                ),
                scopes=None,
                created_at=datetime.utcnow().isoformat(),
            )

            try:
                GeneralService().create_token(token)
                dialog.open = False
            finally:
                loader.visible = False
                func()
                self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#22272e",
            title=ft.Text("Create Token", color="#ffffff", size=20),
            content=ft.Column(
                [
                    github_token,
                    ft.Row(
                        [
                            expire_text,
                            ft.IconButton(
                                icon=ft.Icons.TIMER,
                                icon_color=ft.Colors.WHITE,
                                on_click=open_date_picker,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    error_text,
                    ft.Row([loader], alignment=ft.MainAxisAlignment.CENTER),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dialog()),
                ft.ElevatedButton(
                    "Create",
                    bgcolor="#2f82f7",
                    color="#ffffff",
                    on_click=submit,
                ),
            ],
        )

        return dialog

    # [In dialogs.py] inside Dialog class

    def edit_token(self, token: Token, func):
        # Pre-fill with existing token data
        token_tf = ft.TextField(
            label="Access Token",
            value=token.token_encrypted, # Assumes token is decrypted when passed here
            autofocus=True,
            password=True,
            can_reveal_password=True
        )

        # Parse existing expiry date
        initial_date = None
        if token.expires_at:
            try:
                initial_date = datetime.fromisoformat(token.expires_at)
            except:
                pass

        selected_datetime = {"value": initial_date}
        
        expire_text = ft.Text(
            f"Expire At: {initial_date.strftime('%Y-%m-%d %H:%M')}" if initial_date else "Expire At: Never", 
            color=ft.Colors.WHITE if initial_date else ft.Colors.GREY
        )

        loader = ft.ProgressRing(visible=False)

        # --- Date & Time Pickers (Same logic as create) ---
        def on_date_picked(e):
            if e.control.value:
                selected_datetime["date"] = e.control.value
                open_time_picker()

        def on_time_picked(e):
            if e.control.value:
                date = selected_datetime["date"]
                time = e.control.value
                dt = datetime(date.year, date.month, date.day, time.hour, time.minute)
                selected_datetime["value"] = dt
                expire_text.value = f"Expire At: {dt.strftime('%Y-%m-%d %H:%M')}"
                expire_text.color = ft.Colors.WHITE
                self.page.update()

        date_picker = ft.DatePicker(on_change=on_date_picked)
        time_picker = ft.TimePicker(on_change=on_time_picked)
        self.page.overlay.extend([date_picker, time_picker])

        def open_date_picker(e):
            date_picker.open = True
            self.page.update()

        def open_time_picker():
            time_picker.open = True
            self.page.update()

        def close_dialog():
            dialog.open = False
            self.page.update()

        def submit(e):
            if not token_tf.value:
                token_tf.error_text = "Token cannot be empty"
                self.page.update()
                return

            loader.visible = True
            self.page.update()

            # Update the token object
            token.token_encrypted = token_tf.value
            token.expires_at = selected_datetime["value"].isoformat() if selected_datetime["value"] else None
            
            try:
                GeneralService().update_token(token)
                dialog.open = False
            finally:
                loader.visible = False
                func()
                self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#22272e",
            title=ft.Text("Edit Token", color="#ffffff", size=20),
            content=ft.Column(
                [
                    token_tf,
                    ft.Row(
                        [
                            expire_text,
                            ft.IconButton(icon=ft.Icons.TIMER, icon_color=ft.Colors.WHITE, on_click=open_date_picker),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row([loader], alignment=ft.MainAxisAlignment.CENTER),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dialog()),
                ft.ElevatedButton("Save Changes", bgcolor="#2f82f7", color="#ffffff", on_click=submit),
            ],
        )
        return dialog
        
        
