import flet as ft
from core.general_service import GeneralService
from core.http.errors import AuthenticationError , RateLimitError , AuthorizationError
from core.platforms.github.github_service import GitHubService
from ui.components.dialogs import Dialog
from datetime import datetime
import os
from ui.pages.settings.settings_sidebar import SettingsSidebar
from ui.pages.settings.accounts_view import AccountsView
from ui.pages.settings.tokens_view import TokensView
from ui.pages.settings.rate_limits_view import RateLimitsView
from ui.pages.settings.preferences_view import PreferencesView

class SettingPage(ft.Row) :
    def __init__(self, navigator):
        super().__init__(expand=True)
        
        self.active_section = "accounts"
        
        self.service = GeneralService()
        
        self.content_area = ft.Container(expand=True , padding=20)
        
        self.navigator = navigator
        
        self.sidebar = SettingsSidebar(self.on_sidebar_select)
        
        self.controls = [
            self.sidebar,
            self.content_area,
        ]
        
    def did_mount(self):
        self._render_content()
    
    def on_sidebar_select(self, key: str):
        self.active_section = key

        self._render_content()
    
    def _render_content(self):
        if self.active_section == "accounts":
            self.content_area.content = AccountsView(self.service)
        elif self.active_section == "tokens":
            self.content_area.content = TokensView(self.service)
        elif self.active_section == "ratelimits":
            self.content_area.content = RateLimitsView(self.navigator , self.service)
        elif self.active_section == "preferences":
            self.content_area.content = PreferencesView()

        if self.page:
            self.update()
    
