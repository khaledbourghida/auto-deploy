import flet as ft

class AppTheme:
    # Color Palette
    BG_DARK = "#0d1117"
    BG_SURFACE = "#161b22"
    BG_SURFACE_HOVER = "#21262d"
    
    PRIMARY = "#2f82f7"
    PRIMARY_HOVER = "#316dca"
    
    TEXT_PRIMARY = "#c9d1d9"
    TEXT_SECONDARY = "#8b949e"
    
    BORDER_COLOR = "#30363d"
    
    SUCCESS = "#2ea043"
    ERROR = "#f85149"
    WARNING = "#d29922"
    
    # Fonts
    FONT_FAMILY = "Inter, Roboto, sans-serif"
    
    @classmethod
    def get_theme(cls) -> ft.Theme:
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                background=cls.BG_DARK,
                surface=cls.BG_SURFACE,
                primary=cls.PRIMARY,
                on_primary=ft.colors.WHITE,
                error=cls.ERROR,
                outline=cls.BORDER_COLOR,
            ),
            font_family=cls.FONT_FAMILY,
            visual_density=ft.ThemeVisualDensity.COMFORTABLE,
        )
