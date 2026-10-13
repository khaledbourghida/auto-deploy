import flet as ft
from core.general_service import GeneralService
from core.http.errors import AuthenticationError , RateLimitError , AuthorizationError
from core.platforms.github.github_service import GitHubService
from ui.components.dialogs import Dialog
from datetime import datetime
import os

class PreferencesView(ft.Column):
    def __init__(self):
        super().__init__(expand=True, scroll=ft.ScrollMode.AUTO, spacing=20)
        
        self.controls = [
            self._build_header(),
            ft.Divider(height=20, color="transparent"),
            self._build_guides_list()
        ]

    def _build_header(self):
        return ft.Column([
            ft.Text("Help & Resources", size=30, weight=ft.FontWeight.BOLD, color="white"),
            ft.Text("Guides and tutorials to help you connect your accounts.", color="#8b949e"),
        ], spacing=5)

    def _build_guides_list(self):
        platforms = [
            {"id": "github", "name": "GitHub", "file": "githubtoken.mp4", "status": "active"},
            {"id": "docker", "name": "Docker Hub", "file": "dockertoken.mp4", "status": "later"},
            {"id": "netlify", "name": "Netlify", "file": "netlifytoken.mp4", "status": "later"},
            {"id": "render", "name" : "Render", "file": "rendertoken.mp4", "status": "later"}
        ]

        guides = []
        for p in platforms:
            if p["status"] == "active":
                guides.append(self._build_video_card(p))
            else:
                guides.append(self._build_placeholder_card(p))
        
        return ft.Column(guides, spacing=30)

    def _build_video_card(self, platform):
        video_path = f"assets/videos/{platform['file']}"
        
        file_exists = os.path.exists(video_path)

        # 1. Content Area (Video or Fallback Text)
        if file_exists:
            media_content = ft.Container(
                aspect_ratio=16/9,
                bgcolor="black",
                border_radius=8,
                content=ft.Video(
                    playlist=[ft.VideoMedia(video_path)],
                    playlist_mode=ft.PlaylistMode.LOOP,
                    fill_color=ft.Colors.BLACK,
                    aspect_ratio=16/9,
                    volume=100,
                    autoplay=False,
                    filter_quality=ft.FilterQuality.HIGH,
                    muted=False
                )
            )
            status_text = "Video Tutorial"
            icon = ft.Icons.PLAY_CIRCLE_FILLED
            icon_color = "#58a6ff"
        else:
            # Fallback if video is missing
            media_content = ft.Container(
                height=200,
                bgcolor="#161b22",
                border_radius=8,
                alignment=ft.alignment.center,
                content=ft.Column([
                    ft.Icon(ft.Icons.VIDEO_FILE, size=40, color="#8b949e"),
                    ft.Text("Video tutorial not found", color="white", weight="bold"),
                    ft.Text(f"Please place '{platform['file']}' in 'assets/videos/'", color="#8b949e", size=12),
                    ft.ElevatedButton("Read Text Guide", color="white", bgcolor="#21262d", height=30)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
            )
            status_text = "Guide Missing"
            icon = ft.Icons.WARNING_AMBER
            icon_color = "#d29922"

        # 2. The Card UI
        return ft.Container(
            bgcolor="#0d1117",
            border=ft.border.all(1, "#30363d"),
            border_radius=12,
            padding=20,
            content=ft.Column([
                # Title Row
                ft.Row([
                    ft.Row([
                        ft.Icon(ft.Icons.MOVIE, color="white"),
                        ft.Text(f"How to get {platform['name']} Token", size=20, weight="bold", color="white"),
                    ]),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(icon, size=14, color=icon_color),
                            ft.Text(status_text, size=12, color=icon_color)
                        ], spacing=5),
                        bgcolor=ft.Colors.with_opacity(0.1, icon_color),
                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                        border_radius=20
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Divider(color="#21262d"),
                
                # The Video or Placeholder
                media_content,
                
                # Footer / Description
                ft.Container(height=10),
                ft.Text(
                    f"Follow this step-by-step video to generate a Personal Access Token for {platform['name']}. "
                    "Ensure you select the correct scopes (repo, user, workflow) to allow the application to function correctly.",
                    color="#8b949e",
                    size=14
                )
            ])
        )

    def _build_placeholder_card(self, platform):
        return ft.Container(
            bgcolor="#0d1117",
            border=ft.border.all(1, "#30363d"),
            border_radius=12,
            padding=20,
            opacity=0.6, # Dimmed to look disabled/future
            content=ft.Row([
                ft.Column([
                    ft.Text(f"How to get {platform['name']} Token", size=18, weight="bold", color="white"),
                    ft.Text("Coming soon...", color="#8b949e", italic=True)
                ]),
                ft.Icon(ft.Icons.LOCK_CLOCK, color="#8b949e")
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )