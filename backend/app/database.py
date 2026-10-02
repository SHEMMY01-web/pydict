import sqlite3
import json
import os
from pathlib import Path

DB_PATH = os.environ.get("PYDICT_DB", os.environ.get("PYKTIONARY_DB", str(Path(__file__).parent / "pydict.db")))

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Main entries table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE NOT NULL,
        term TEXT NOT NULL,
        part_of_speech TEXT NOT NULL,
        pronunciation TEXT,
        category TEXT NOT NULL,
        signature TEXT,
        short_summary TEXT NOT NULL,
        full_description TEXT NOT NULL,
        parameters TEXT,        -- JSON array of {name, type, description, default}
        returns TEXT,           -- JSON object {type, description}
        added_in_version TEXT,
        deprecated_in_version TEXT,
        pep_reference TEXT,
        pep_url TEXT,
        gotchas TEXT,           -- JSON array of strings
        cross_language TEXT,    -- JSON object {lang: equivalent}
        tags TEXT,              -- JSON array of strings
        simple_definition TEXT, -- Plain-language breakdown shown after the official definition
        senses TEXT,            -- JSON array of Polysemy Senses {sense_number, part_of_speech, signature, summary, parameters, returns, example_code}
        version_timeline TEXT,  -- JSON array of Version Evolution Items {version, change_type, title, description, pep}
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Safe migration in case table was created prior
    for column, col_type in [("simple_definition", "TEXT"), ("senses", "TEXT"), ("version_timeline", "TEXT")]:
        try:
            cursor.execute(f"ALTER TABLE entries ADD COLUMN {column} {col_type};")
        except sqlite3.OperationalError:
            pass # column already exists

    # Code examples table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS code_examples (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_slug TEXT NOT NULL,
        title TEXT NOT NULL,
        code TEXT NOT NULL,
        expected_output TEXT,
        is_interactive BOOLEAN DEFAULT 1,
        FOREIGN KEY(entry_slug) REFERENCES entries(slug) ON DELETE CASCADE
    );
    """)

    # Community notes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS community_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_slug TEXT NOT NULL,
        author TEXT NOT NULL,
        content TEXT NOT NULL,
        category TEXT DEFAULT 'tip', -- 'tip', 'analogy', 'warning'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(entry_slug) REFERENCES entries(slug) ON DELETE CASCADE
    );
    """)

    # User bookmarks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_slug TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(entry_slug) REFERENCES entries(slug) ON DELETE CASCADE
    );
    """)

    # Full text search table (FTS5)
    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS entries_fts USING fts5(
        slug,
        term,
        short_summary,
        full_description,
        tags,
        category,
        tokenize = 'porter ascii'
    );
    """)

    conn.commit()
    conn.close()
