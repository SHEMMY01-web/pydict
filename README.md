# 🐍 PyKtionary — The Python Lexicon

**PyKtionary** is an encyclopedic dictionary and linguistic reference for Python, modeled directly on the **Wiktionary** interface. It provides structured definitions, phonetic pronunciations, syntactic breakdowns, parameter specifications, version lineages, common pitfalls, cross-language analogies, and in-browser code execution.

The project consists of:
1. **Web Application:** Built with React & Vite using the authentic Wikimedia Vector styling.
2. **Mobile Application:** Built with React Native & Expo for iOS and Android, following the official mobile Wiktionary layout with 100% offline support.
3. **Backend API:** Built with FastAPI & SQLite FTS5 for full-text indexing, linguistic polysemy, and version history.

---

## 📖 Wiktionary Anatomy

Every Python symbol in PyKtionary follows the traditional Wiktionary article structure:

* **Headword (`H1`):** Formatted in serif type (`Linux Libertine` / `Georgia`).
* **Pronunciation & Audio:** International Phonetic Alphabet (IPA) transcription (e.g. `[ˈzaɪp]`, `[taɪp]`) with audio playback.
* **Table of Contents:** Numbered navigation box to jump between sections.
* **Etymology & Origin:** Python version introduced, deprecation notices, and official PEP links.
* **Part of Speech:** Heading (`Built-in function`, `Keyword`, `Metaclass`, `Protocol`, `Module`).
* **Numbered Definitions (`1.`, `2.`, `3.`):** Each sense includes parenthetical linguistic context (e.g. `(programming, iterators)`) and a direct definition.
* **Parameters & Return Value:** Structured table of argument names, types, defaults, and return specifications.
* **Code Examples:** Minimalist, readable code snippets with `Copy` and `Run` execution.
* **Usage Notes:** Bulleted lists of edge cases, common bugs, and performance characteristics.
* **Evolutionary Version History:** Chronological change logs tracking how terms developed across major Python releases.
* **Translations:** Cross-language analogies mapping Python concepts to JavaScript, Rust, Go, C++, and Java.
* **Zero Marketing Fluff:** Authoritative and scholarly without promotional banners, buzzwords, or unnecessary subtext.

---

## 📱 Mobile App (React Native & Expo)

The mobile app in [`mobile/`](file:///home/olaewevictor01/PY%20DICT/mobile) delivers a faithful mobile Wiktionary experience:

* **100% Offline-Capable:** Pre-bundles all 221 Python definitions in [`offlineData.json`](file:///home/olaewevictor01/PY%20DICT/mobile/src/services/offlineData.json).
* **Wiktionary Mobile Header:** Py logo monogram, "The free dictionary" tagline, random entry button, search trigger, and dark/light theme switcher.
* **Read Tab:** Features the daily Python Word of the Day and categorized index.
* **Search Tab:** Live filtering by term, keyword, or category with instant preview.
* **Article Screen:** Complete Wiktionary layout with serif headword, IPA audio button, numbered senses, code snippets with copy action, parameter tables, gotchas, version timeline, and translations.
* **Saved Tab:** Personal bookmarks list for rapid offline study and revision.
* **Quiz Tab:** Scholarly multiple-choice vocabulary test with direct links back to dictionary entries.

### Running the Mobile App

```bash
cd mobile

# Install dependencies
npm install

# Start the Expo development server
npx expo start

# Open on specific platform:
npx expo start --android   # Android Emulator / Device
npx expo start --ios       # iOS Simulator / Device
npx expo start --web       # Web browser preview
```

---

## 🌐 Web App (React + Vite)

The web frontend in [`frontend/`](file:///home/olaewevictor01/PY%20DICT/frontend) features the authentic Wikimedia Vector layout:

* **Typography:** `Linux Libertine`, `Georgia`, and serif headwords with classic Wikimedia blue links (`#3366cc`).
* **Interactive WASM Execution:** Code examples can be executed in-browser via Pyodide without server-side overhead.
* **Keyboard Shortcuts:** `⌘K` or `/` opens instant FTS5 search dialog.
* **Dual Theme:** Native dark and light modes matching Wikimedia Vector styles.

### Running the Web App

```bash
cd frontend
npm install
npm run dev
```

Visit [http://127.0.0.1:5173](http://127.0.0.1:5173).

---

## ⚙️ Backend API (FastAPI + SQLite FTS5)

The backend in [`backend/`](file:///home/olaewevictor01/PY%20DICT/backend) stores 221 comprehensive entries covering:
* All 71 built-in functions
* All 35 language keywords
* 40+ special / dunder methods
* 10 core standard library modules (`math`, `re`, `json`, `pathlib`, `datetime`, `random`, `sys`, `subprocess`, `typing`, `hashlib`)
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

Run the root startup script to start both Backend and Frontend concurrently:
```bash
./start.sh
```
