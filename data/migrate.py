import os
import sys
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from data.database import DataBase


def get_migrations_dir():
    """Get migrations directory for both dev and packaged app"""
    if getattr(sys, 'frozen', False):
        # Running as packaged app - look in assets
        base_path = Path(sys.executable).parent / "data" / "flutter_assets" / "assets" / "migrations"
    else:
        # Running in development - look in data/migrations folder
        base_path = Path(__file__).parent / "migrations"
    
    return base_path


def run_migrations():
    db = DataBase()
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL
        )
    """)

    applied = {
        row["version"]
        for row in cursor.execute("SELECT version FROM schema_migrations")
    }

    migrations_dir = get_migrations_dir()
    
    # Check if migrations directory exists
    if not migrations_dir.exists():
        print(f"⚠️ Migrations directory not found: {migrations_dir}")
        conn.close()
        return

    files = sorted(f for f in os.listdir(migrations_dir) if f.endswith(".sql"))

    if not files:
        print("ℹ️ No migration files found")
        conn.close()
        return

    for file in files:
        version = file.split("_")[0]
        if version in applied:
            continue

        path = migrations_dir / file
        with open(path, "r", encoding="utf-8") as f:
            sql = f.read()

        print(f"Applying migration {file}")
        cursor.executescript(sql)

        cursor.execute(
            "INSERT INTO schema_migrations (version, applied_at) VALUES (?, ?)",
            (version, datetime.now(timezone.utc).isoformat())
        )

        conn.commit()

    conn.close()