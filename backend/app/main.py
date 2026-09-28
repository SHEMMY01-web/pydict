from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
import asyncio
import json
import sqlite3
import random
from datetime import date

from .database import get_db, init_db
from .schemas import (
    EntrySummary, EntryDetail, Parameter, ReturnInfo,
    CodeExample, CommunityNote, NoteCreate, CategoryStats,
    AppStats, QuizQuestion
)
from .seed_data import seed_database
from .extractor import extract_builtins

app = FastAPI(
    title="PyDict API",
    description="The encyclopedic dictionary and interactive reference engine for Python",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CATEGORY_LABELS = {
    "technique": "Programming Techniques & Idioms",
    "builtin": "Built-in Functions & Types",
    "keyword": "Language Keywords",
    "dunder": "Dunder / Special Methods",
    "std_lib": "Standard Library Modules",
    "concept": "Core Concepts & Architecture",
    "syntax": "Syntax & Operators"
}

@app.on_event("startup")
def startup_event():
    init_db()
    conn = get_db()
    cursor = conn.cursor()
    count = cursor.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
    conn.close()
    if count == 0:
        seed_database()
        extract_builtins()

def row_to_summary(row: sqlite3.Row) -> EntrySummary:
    tags = json.loads(row["tags"]) if row["tags"] else []
    senses_list = []
    try:
        if "senses" in row.keys() and row["senses"]:
            senses_list = json.loads(row["senses"])
    except Exception:
        senses_list = []

    return EntrySummary(
        id=row["id"],
        slug=row["slug"],
        term=row["term"],
        part_of_speech=row["part_of_speech"],
        pronunciation=row["pronunciation"],
        category=row["category"],
        signature=row["signature"],
        short_summary=row["short_summary"],
        added_in_version=row["added_in_version"],
        tags=tags,
        sense_count=max(1, len(senses_list))
    )

@app.get("/api/stats", response_model=AppStats)
def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    total = cursor.execute("SELECT COUNT(*) FROM entries").fetchone()[0]

    category_rows = cursor.execute(
        "SELECT category, COUNT(*) as c FROM entries GROUP BY category ORDER BY c DESC"
    ).fetchall()
    categories = [
        CategoryStats(
            category=r["category"],
            label=CATEGORY_LABELS.get(r["category"], r["category"].title()),
            count=r["c"]
        )
        for r in category_rows
    ]

    version_rows = cursor.execute(
        "SELECT DISTINCT added_in_version FROM entries WHERE added_in_version IS NOT NULL ORDER BY added_in_version DESC"
    ).fetchall()
    versions = [r["added_in_version"] for r in version_rows if r["added_in_version"]]

    # Word of the Day (deterministic based on today's ordinal)
    all_entries = cursor.execute("SELECT * FROM entries WHERE category IN ('builtin', 'dunder', 'concept', 'keyword')").fetchall()
    wotd = None
    if all_entries:
        day_index = date.today().toordinal() % len(all_entries)
        wotd = row_to_summary(all_entries[day_index])

    conn.close()
    return AppStats(
        total_entries=total,
        categories=categories,
        versions=versions,
        word_of_the_day=wotd
    )

@app.get("/api/categories")
def get_categories():
    conn = get_db()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT category, COUNT(*) as count FROM entries GROUP BY category"
    ).fetchall()
    conn.close()
    return [
        {
            "category": r["category"],
            "label": CATEGORY_LABELS.get(r["category"], r["category"].title()),
            "count": r["count"]
        }
        for r in rows
    ]

@app.get("/api/entries", response_model=dict)
def list_entries(
    category: Optional[str] = None,
    version: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    letter: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM entries WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if version:
        query += " AND added_in_version = ?"
        params.append(version)

    if tag:
        query += " AND tags LIKE ?"
        params.append(f"%{tag}%")

    if letter:
        clean_letter = letter.strip().lower()
        if clean_letter == "#":
            query += " AND term GLOB '[^a-zA-Z_]*'"
        elif len(clean_letter) == 1 and clean_letter.isalpha():
            query += " AND (term GLOB ? OR term GLOB ?)"
            params.extend([f"[{clean_letter.lower()}{clean_letter.upper()}]*", f"__[{clean_letter.lower()}{clean_letter.upper()}]*"])

    if search:
        query += " AND (term LIKE ? OR short_summary LIKE ? OR tags LIKE ?)"
        term_pattern = f"%{search}%"
        params.extend([term_pattern, term_pattern, term_pattern])

    # Count total
    count_query = query.replace("SELECT *", "SELECT COUNT(*)")
    total_count = cursor.execute(count_query, params).fetchone()[0]

    # Order & Pagination
    query += " ORDER BY term COLLATE NOCASE ASC LIMIT ? OFFSET ?"
    params.extend([page_size, (page - 1) * page_size])

    rows = cursor.execute(query, params).fetchall()
    conn.close()

    items = [row_to_summary(r) for r in rows]
    total_pages = (total_count + page_size - 1) // page_size if total_count > 0 else 1

    return {
        "items": items,
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

@app.get("/api/random")
def get_random_entry():
    """Returns a random entry slug for the 'Special:Random' feature."""
    conn = get_db()
    cursor = conn.cursor()
    row = cursor.execute("SELECT slug FROM entries ORDER BY RANDOM() LIMIT 1").fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="No entries available")
    return {"slug": row["slug"]}

@app.get("/api/search")
def search_entries(q: str = Query(..., min_length=1)):
    conn = get_db()
    cursor = conn.cursor()

    # Priority 1: Exact and prefix term match
    prefix = f"{q.strip()}%"
    contains = f"%{q.strip()}%"

    term_matches = cursor.execute("""
        SELECT * FROM entries 
        WHERE term LIKE ? OR slug LIKE ?
        ORDER BY CASE WHEN term = ? THEN 1 WHEN term LIKE ? THEN 2 ELSE 3 END, term
        LIMIT 10
    """, (contains, contains, q.strip(), prefix)).fetchall()

    # Priority 2: FTS5 matching for description/concept keywords
    fts_rows = []
    try:
        clean_q = "".join(c for c in q if c.isalnum() or c in (" ", "_", "-")).strip()
        if clean_q:
            fts_query = f"{clean_q}*"
            fts_rows = cursor.execute("""
                SELECT e.* FROM entries_fts f
                JOIN entries e ON e.slug = f.slug
                WHERE entries_fts MATCH ?
                LIMIT 10
            """, (fts_query,)).fetchall()
    except Exception:
        fts_rows = []

    conn.close()

    # Merge unique
    seen = set()
    results = []
    for r in list(term_matches) + list(fts_rows):
        if r["slug"] not in seen:
            seen.add(r["slug"])
            results.append(row_to_summary(r))
        if len(results) >= 15:
            break

    return {"query": q, "results": results}

@app.get("/api/entries/{slug}", response_model=EntryDetail)
def get_entry(slug: str):
    conn = get_db()
    cursor = conn.cursor()

    row = cursor.execute("SELECT * FROM entries WHERE slug = ?", (slug,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Entry not found")

    # Fetch examples
    example_rows = cursor.execute(
        "SELECT * FROM code_examples WHERE entry_slug = ? ORDER BY id ASC", (slug,)
    ).fetchall()
    examples = [
        CodeExample(
            id=ex["id"],
            title=ex["title"],
            code=ex["code"],
            expected_output=ex["expected_output"],
            is_interactive=bool(ex["is_interactive"])
        )
        for ex in example_rows
    ]

    # Fetch community notes
    note_rows = cursor.execute(
        "SELECT * FROM community_notes WHERE entry_slug = ? ORDER BY created_at DESC", (slug,)
    ).fetchall()
    notes = [
        CommunityNote(
            id=n["id"],
            entry_slug=n["entry_slug"],
            author=n["author"],
            content=n["content"],
            category=n["category"],
            created_at=str(n["created_at"])
        )
        for n in note_rows
    ]

    # Check bookmark
    is_bookmarked = cursor.execute(
        "SELECT 1 FROM bookmarks WHERE entry_slug = ?", (slug,)
    ).fetchone() is not None

    # Fetch related entries (by same category or overlapping tags)
    current_tags = json.loads(row["tags"]) if row["tags"] else []
    related_rows = cursor.execute("""
        SELECT * FROM entries 
        WHERE category = ? AND slug != ? 
        ORDER BY RANDOM() 
        LIMIT 4
    """, (row["category"], slug)).fetchall()
    related = [row_to_summary(r) for r in related_rows]

    conn.close()

    params_parsed = json.loads(row["parameters"]) if row["parameters"] else []
    params_data = [Parameter(**p) for p in params_parsed if isinstance(p, dict)]

    returns_parsed = json.loads(row["returns"]) if row["returns"] else None
    returns_data = ReturnInfo(**returns_parsed) if isinstance(returns_parsed, dict) else None

    senses_data = []
    if "senses" in row.keys() and row["senses"]:
        try:
            senses_data = [Sense(**s) for s in json.loads(row["senses"])]
        except Exception as e:
            senses_data = []

    timeline_data = []
    if "version_timeline" in row.keys() and row["version_timeline"]:
        try:
            timeline_data = [VersionEvent(**v) for v in json.loads(row["version_timeline"])]
        except Exception as e:
            timeline_data = []

    # Safely read simple_definition
    simple_def = None
    try:
        if "simple_definition" in row.keys():
            simple_def = row["simple_definition"]
    except Exception:
        pass

    return EntryDetail(
        id=row["id"],
        slug=row["slug"],
        term=row["term"],
        part_of_speech=row["part_of_speech"],
        pronunciation=row["pronunciation"],
        category=row["category"],
        signature=row["signature"],
        short_summary=row["short_summary"],
        simple_definition=simple_def,
        full_description=row["full_description"],
        parameters=params_data,
        returns=returns_data,
        added_in_version=row["added_in_version"],
        deprecated_in_version=row["deprecated_in_version"],
        pep_reference=row["pep_reference"],
        pep_url=row["pep_url"],
        gotchas=json.loads(row["gotchas"]) if row["gotchas"] else [],
        cross_language=json.loads(row["cross_language"]) if row["cross_language"] else {},
        tags=current_tags,
        senses=senses_data,
        version_timeline=timeline_data,
        examples=examples,
        notes=notes,
        is_bookmarked=is_bookmarked,
        related_entries=related
    )

@app.post("/api/entries/{slug}/notes", status_code=status.HTTP_201_CREATED)
def add_note(slug: str, note: NoteCreate):
    conn = get_db()
    cursor = conn.cursor()

    entry = cursor.execute("SELECT 1 FROM entries WHERE slug = ?", (slug,)).fetchone()
    if not entry:
        conn.close()
        raise HTTPException(status_code=404, detail="Entry not found")

    cursor.execute("""
    INSERT INTO community_notes (entry_slug, author, content, category)
    VALUES (?, ?, ?, ?)
    """, (slug, note.author or "Anonymous Pythonista", note.content, note.category))
    conn.commit()
    conn.close()

    return {"message": "Note added successfully"}

@app.post("/api/entries/{slug}/bookmark")
def toggle_bookmark(slug: str):
    conn = get_db()
    cursor = conn.cursor()

    existing = cursor.execute("SELECT 1 FROM bookmarks WHERE entry_slug = ?", (slug,)).fetchone()
    if existing:
        cursor.execute("DELETE FROM bookmarks WHERE entry_slug = ?", (slug,))
        is_bookmarked = False
    else:
        cursor.execute("INSERT INTO bookmarks (entry_slug) VALUES (?)", (slug,))
        is_bookmarked = True

    conn.commit()
    conn.close()
    return {"slug": slug, "is_bookmarked": is_bookmarked}

@app.get("/api/bookmarks")
def get_bookmarks():
    conn = get_db()
    cursor = conn.cursor()
    rows = cursor.execute("""
        SELECT e.* FROM bookmarks b
        JOIN entries e ON e.slug = b.entry_slug
        ORDER BY b.created_at DESC
    """).fetchall()
    conn.close()
    return [row_to_summary(r) for r in rows]

@app.get("/api/quiz", response_model=List[QuizQuestion])
def get_quiz():
    """Generates an engaging 5-question vocabulary quiz from entries."""
    conn = get_db()
    cursor = conn.cursor()
    
    rows = cursor.execute("""
        SELECT slug, term, short_summary, category FROM entries 
        WHERE LENGTH(short_summary) > 20
        ORDER BY RANDOM() LIMIT 15
    """).fetchall()
    conn.close()

    if len(rows) < 4:
        return []

    questions = []
    sample_pool = list(rows)
    random.shuffle(sample_pool)

    for i, target in enumerate(sample_pool[:5]):
        # Distractors
        distractors = [r["term"] for r in sample_pool if r["term"] != target["term"]]
        random.shuffle(distractors)
        options = distractors[:3] + [target["term"]]
        random.shuffle(options)

        questions.append(QuizQuestion(
            id=f"q_{i}_{target['slug']}",
            term=target["term"],
            question=f"Which Python term matches this definition?\n\"{target['short_summary']}\"",
            options=options,
            correct_answer=target["term"],
            explanation=f"`{target['term']}`: {target['short_summary']}",
            category=target["category"]
        ))

    return questions

BUILD_STATE_FILE = "/home/olaewevictor01/PY DICT/mobile/build_state.json"
APK_FILE = "/home/olaewevictor01/PY DICT/mobile/android/app/build/outputs/apk/debug/app-debug.apk"

@app.get("/api/build-status")
def get_build_status():
    if os.path.exists(BUILD_STATE_FILE):
        try:
            with open(BUILD_STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "phase": "idle",
        "step": 0,
        "total_steps": 3,
        "step_name": "Standby",
        "downloaded_bytes": 0,
        "total_bytes": 669320864,
        "percent": 0.0,
        "speed_mbps": 0.0,
        "eta_seconds": 0,
        "recent_logs": ["No active build."],
        "apk_path": APK_FILE if os.path.exists(APK_FILE) else None
    }

@app.get("/api/build-status/stream")
async def stream_build_status():
    from fastapi.responses import StreamingResponse
    import asyncio

    async def event_generator():
        while True:
            data = get_build_status()
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.post("/api/build/start")
def start_build():
    import subprocess
    # Check if already running
    check = subprocess.run(["pgrep", "-f", "download_and_build.py"], capture_output=True, text=True)
    if check.stdout.strip():
        return {"status": "already_running"}
    
    script_path = "/home/olaewevictor01/PY DICT/mobile/scripts/download_and_build.py"
    subprocess.Popen(["python3", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return {"status": "started"}

@app.post("/api/build/pause")
def pause_build():
    import subprocess
    subprocess.run(["pkill", "-f", "download_and_build.py"])
    subprocess.run(["pkill", "-f", "curl -4 --http1.1.*android-ndk"])
    if os.path.exists(BUILD_STATE_FILE):
        try:
            with open(BUILD_STATE_FILE, "r") as f:
                state = json.load(f)
            state["phase"] = "paused"
            state["step_name"] = "Paused by user (progress saved)"
            state["speed_mbps"] = 0.0
            state["recent_logs"].append("Download paused by user. Progress safely saved.")
            if len(state["recent_logs"]) > 50:
                state["recent_logs"] = state["recent_logs"][-50:]
            with open(BUILD_STATE_FILE, "w") as f:
                json.dump(state, f, indent=2)
        except Exception:
            pass
    return {"status": "paused"}

@app.post("/api/build/resume")
def resume_build():
    return start_build()

@app.get("/api/download-apk")
def download_apk():
    from fastapi.responses import FileResponse
    if os.path.exists(APK_FILE):
        return FileResponse(
            APK_FILE,
            media_type="application/vnd.android.package-archive",
            filename="PyKtionary-debug.apk"
        )
    raise HTTPException(status_code=404, detail="APK has not been built yet.")

from pathlib import Path
TTS_CACHE_DIR = Path(__file__).parent / "tts_cache"
TTS_CACHE_DIR.mkdir(exist_ok=True)

@app.get("/api/tts")
def get_pronunciation_audio(term: str = Query(..., min_length=1)):
    import urllib.request
    import urllib.parse
    import re
    from fastapi.responses import FileResponse
    
    clean = term.replace("__", " double underscore ").replace("()", "")
    clean = re.sub(r'[^a-zA-Z0-9_\s]', ' ', clean).strip()
    if not clean:
        clean = term.strip()
    
    safe_name = re.sub(r'\W+', '_', term.lower()) + ".mp3"
    cache_file = TTS_CACHE_DIR / safe_name
    
    if cache_file.exists() and cache_file.stat().st_size > 0:
        return FileResponse(cache_file, media_type="audio/mpeg")
    
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en&q={urllib.parse.quote(clean)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            audio_data = res.read()
            with open(cache_file, "wb") as f:
                f.write(audio_data)
            return FileResponse(cache_file, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"TTS synthesis unavailable: {e}")


