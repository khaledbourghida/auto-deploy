CREATE TABLE IF NOT EXISTS repositories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    repo_id TEXT NOT NULL,
    name TEXT NOT NULL,
    full_name TEXT NOT NULL,
    is_private INTEGER,
    main_language TEXT,
    updated_at TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);
