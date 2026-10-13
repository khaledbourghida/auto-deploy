CREATE TABLE IF NOT EXISTS platforms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL,
    subtitle TEXT NOT NULL,
    bgcolor TEXT NOT NULL,
    icon TEXT NOT NULL,
    desc TEXT NOT NULL,
    base_url TEXT,
    is_connected INTEGER,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS schema_migrations (
    version TEXT PRIMARY KEY,
    applied_at TEXT NOT NULL
);
