# 🐍 PyDict — The Definitive Python Dictionary

**PyDict** is an encyclopedic dictionary and interactive linguistic reference for Python. It provides structured definitions, phonetic pronunciations, plain-English conceptual breakdowns, syntactic signatures, parameter specifications, version lineages, common pitfalls, cross-language analogies, and live in-browser Python execution.

The project is architected as a high-performance web platform:
1. **Web Application:** Built with React & Vite using a clean, distraction-free classical lexicographical reference interface.
2. **Backend API:** Built with FastAPI & SQLite FTS5 for full-text search indexing, linguistic polysemy, and evolutionary version history.
3. **Interactive Playground:** Powered by client-side WebAssembly (Pyodide) for real-time Python execution directly in the browser.

---

## 📖 Dictionary Anatomy & Entry Structure

Every Python symbol in PyDict follows a comprehensive, classical lexicographical article structure:

* **Headword (`H1`):** Formatted in crisp scholarly serif typography (`Linux Libertine` / `Georgia`).
* **Pronunciation & Audio:** International Phonetic Alphabet (IPA) transcription (e.g. `[ˈzaɪp]`, `[taɪp]`) with audio playback.
* **Table of Contents:** Numbered navigation panel to seamlessly jump between sections.
* **Etymology & Origin:** Python version introduced, deprecation notices, and official PEP links.
* **Part of Speech:** Heading tags (`Built-in Function`, `Language Keyword`, `Metaclass`, `Protocol`, `Standard Library Class`).
* **Numbered Definitions (`1.`, `2.`, `3.`):** Each sense includes parenthetical domain context (e.g. `(programming, iterators)`) and a direct definition.
* **In Plain English:** A dedicated, beginner-friendly conceptual breakdown that demystifies complex terms with clear analogies.
* **Parameters & Return Value:** Structured table of argument names, types, defaults, and return specifications.
* **Ample & Real-World Code Examples:** Practical, production-grade code snippets illustrating real-life use cases with one-click `Copy` and in-browser `Run` execution.
* **Usage Notes & Gotchas:** Bulleted lists of edge cases, common bugs, and performance characteristics.
* **Evolutionary Version History:** Chronological change logs tracking how terms developed across major Python releases.
* **Cross-Language Equivalents:** Analogies mapping Python concepts to JavaScript, Rust, Go, and other languages.
* **Zero Marketing Fluff:** Authoritative and scholarly without promotional banners, buzzwords, or distractions.

---

## 🌐 Web App (React + Vite)

The web frontend in [`frontend/`](frontend) provides a fast, responsive reference experience:

* **Scholarly Typography:** Clean hierarchy with serif headwords, monospace code pills, and accessible contrast.
* **Interactive WASM Execution:** Code examples execute entirely in-browser via Pyodide without server-side overhead or security hazards.
* **Instant Search:** `⌘K` or `/` opens a fast FTS5 search dialog with instant auto-complete.
* **Dual Theme:** Native dark and light modes with seamless contrast.
* **Offline PWA Support:** Built-in caching for fast offline reference.

### Running the Web App

```bash
cd frontend
npm install
npm run dev
```

Visit [http://127.0.0.1:5173](http://127.0.0.1:5173).

---

## ⚙️ Backend API (FastAPI + SQLite FTS5)

The backend in [`backend/`](backend) stores 245+ comprehensive entries covering:
* All 71 built-in functions
* All 35 language keywords
* 40+ special and dunder methods
* Core standard library modules (`math`, `re`, `json`, `pathlib`, `datetime`, `random`, `sys`, `subprocess`, `typing`, `hashlib`)
* Linguistic Polysemy (multiple numbered senses for `type`, `* / **`, `[]`, etc.)
* Version Evolution Timelines (`zip`, `type`, `dict`, `gil`, `enumerate`)

### Running the Backend

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Interactive documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## 🚀 One-Click Launch

Run the startup script to launch both the backend and frontend concurrently:
```bash
./start.sh
```
