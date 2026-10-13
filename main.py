import logging
import traceback
import sys
import os

# 1. SETUP LOGGING IMMEDIATELEY
# This file 'startup_log.txt' will appear next to your exe
logging.basicConfig(
    filename='startup_log.txt', 
    level=logging.DEBUG, 
    filemode='w', 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("--- REAL APP LAUNCHING ---")

try:
    logging.info("1. Attempting to import flet...")
    import flet as ft
    logging.info("   Flet imported successfully!")
    
    logging.info("2. Attempting to import local modules (core, ui, data)...")
    # We import these here to catch if PyInstaller missed the folders
    from core.navigator import Navigator
    from ui.shell.app_shell import AppShell
    from ui.pages.home_page import HomePage
    from data.migrate import run_migrations
    from data.platforms_seed import seed_platforms
    logging.info("   Local modules imported successfully!")

except Exception as e:
    logging.error("CRITICAL IMPORT ERROR: The build is missing files.")
    logging.error(traceback.format_exc())
    # If imports fail, we must exit because main() cannot run
    sys.exit(1)

def main(page: ft.Page):
    try:
        logging.info("3. Main function started")
        
        logging.info("   Running migrations...")
        run_migrations()
        
        logging.info("   Seeding platforms...")
        seed_platforms()
        
        logging.info("   Setting up page window...")
        page.title = "Automation App"
        page.padding = 0
        page.bgcolor = "#0d1117"

        logging.info("   Initializing UI structure...")
        navigator = Navigator(page)
        shell = AppShell(navigator)

        logging.info("   Setting root and pushing home...")
        navigator.set_root(shell)
        navigator.push(HomePage(navigator))

        page.update()
        logging.info("   App rendered successfully!")
        
    except Exception as e:
        error_msg = traceback.format_exc()
        logging.error(f"CRASH INSIDE APP: {error_msg}")
        try:
            # Try to show error on screen if possible
            page.add(ft.Text(f"CRITICAL ERROR:\n{e}", color="red", size=20))
            page.update()
        except:
            pass

if __name__ == "__main__":
    try:
        logging.info("0. Starting Flet Engine...")
        ft.app(target=main)
    except Exception:
        logging.error("CRASH AT STARTUP")
        logging.error(traceback.format_exc())