import builtins
import inspect
import keyword
import json
import sqlite3
import sys
import importlib
from .database import get_db, init_db
from .catalog_data import BUILTIN_CATALOG, KEYWORD_CATALOG, EXCEPTION_CATALOG

BUILTIN_GOTCHAS = {
    "eval": ["Security hazard: never execute untrusted user input with eval()!", "Can be restricted with custom globals/locals, but AST parsing is much safer."],
    "exec": ["Executes arbitrary Python code dynamically; major security vulnerability if exposed to users.", "Does not return values, modifies local/global namespace."],
    "range": ["In Python 3, range returns a lazy sequence object, not a list.", "Supports O(1) membership testing (`x in range(...)`) and slicing!"],
    "open": ["Always use with a context manager (`with open(...) as f:`) to ensure immediate file descriptor closure.", "Default encoding varies by OS; specify `encoding='utf-8'` explicitly."],
    "sorted": ["Returns a new sorted list, unlike `list.sort()` which sorts in-place and returns None.", "Stable sort: items with identical keys maintain original order."],
    "map": ["Returns an iterator in Python 3. To see results in print, wrap in `list(map(...))`.", "Often less readable than list comprehensions."],
    "filter": ["Returns an iterator. `filter(None, seq)` removes all falsy values (0, '', None, False, [])."],
    "any": ["Short-circuits immediately upon encountering the first truthy value.", "Returns False for an empty iterable."],
    "all": ["Short-circuits immediately upon encountering the first falsy value.", "Vacuous truth: returns True for an empty iterable!"],
    "hash": ["Only hashable (immutable) objects can be hashed. Dicts and lists raise TypeError.", "Python randomizes hash seeds per process for security against collision attacks."],
    "isinstance": ["bool is a subclass of int in Python: isinstance(True, int) is True!", "Prefer isinstance(x, Class) over type(x) is Class for OOP polymorphism."],
    "dict": ["In Python 3.7+, dictionary key insertion order is guaranteed by the language specification.", "Use dict.get(key, default) instead of catching KeyError for optional keys."]
}

CROSS_LANG_BUILTINS = {
    "len": {"JavaScript": "array.length / string.length", "Rust": "slice.len()", "Go": "len(slice)"},
    "map": {"JavaScript": "array.map(fn)", "Rust": "iter.map(fn)", "Go": "No native map; use for loop"},
    "filter": {"JavaScript": "array.filter(fn)", "Rust": "iter.filter(fn)", "Go": "No native filter; use for loop"},
    "range": {"Rust": "start..end", "Go": "for i := 0; i < n; i++", "Ruby": "(start...end)"},
    "sorted": {"JavaScript": "array.slice().sort()", "Rust": "slice.sort()", "Go": "slices.Sort(s)"},
    "open": {"Node.js": "fs.readFileSync / fs.promises.open", "Rust": "std::fs::File::open", "Go": "os.Open"},
    "sum": {"JavaScript": "array.reduce((a, b) => a + b, 0)", "Rust": "iter.sum()", "Go": "manual loop"}
}

STDLIB_MODULES_TO_INGEST = [
    {
        "module": "math",
        "members": ["isclose", "comb", "perm", "gcd", "lcm", "sqrt", "factorial", "prod", "ceil", "floor"]
    },
    {
        "module": "re",
        "members": ["compile", "search", "match", "findall", "sub", "split", "escape"]
    },
    {
        "module": "json",
        "members": ["dumps", "loads", "dump", "load"]
    },
    {
        "module": "pathlib",
        "members": ["Path", "PurePath"]
    },
    {
        "module": "datetime",
        "members": ["datetime", "date", "time", "timedelta", "timezone"]
    },
    {
        "module": "random",
        "members": ["choice", "choices", "randint", "randrange", "sample", "shuffle", "uniform"]
    },
    {
        "module": "sys",
        "members": ["argv", "version", "path", "platform", "getsizeof", "getrefcount"]
    },
    {
        "module": "subprocess",
        "members": ["run", "Popen", "PIPE"]
    },
    {
        "module": "typing",
        "members": ["TypeVar", "Protocol", "Generic", "Annotated", "Self", "Literal", "Union", "Optional"]
    },
    {
        "module": "hashlib",
        "members": ["sha256", "md5", "sha1", "sha512"]
    }
]

def extract_builtins():
    conn = get_db()
    cursor = conn.cursor()

    existing_slugs = set(row[0] for row in cursor.execute("SELECT slug FROM entries").fetchall())

    # 1. Process Built-in Functions & Types
    for name in dir(builtins):
        if name.startswith("_"):
            continue
        obj = getattr(builtins, name)
        slug = name.lower()

        if slug in existing_slugs:
            continue

        is_fn = inspect.isbuiltin(obj) or inspect.isfunction(obj)
        is_cls = inspect.isclass(obj)
        if not (is_fn or is_cls):
            continue

        raw_doc = inspect.getdoc(obj) or ""
        lines = [line.strip() for line in raw_doc.split("\n") if line.strip()]
        short_summary = lines[0] if lines else f"Python built-in {name}."
        
        # Try signature
        sig_str = f"{name}(...)"
        try:
            sig = inspect.signature(obj)
            sig_str = f"{name}{sig}"
        except (ValueError, TypeError):
            if lines and lines[0].startswith(name + "("):
                sig_str = lines[0]
                short_summary = lines[1] if len(lines) > 1 else short_summary

        pos = "Built-in Type" if is_cls else "Built-in Function"
        full_desc = raw_doc if raw_doc else f"`{name}` is a standard Python built-in."
        
        # Check rich catalog first, else generate beginner-friendly definition
        if name in BUILTIN_CATALOG:
            simple_def = BUILTIN_CATALOG[name]["simple_definition"]
            example_title = BUILTIN_CATALOG[name]["title"]
            example_code = BUILTIN_CATALOG[name]["code"]
        elif name in EXCEPTION_CATALOG:
            simple_def = EXCEPTION_CATALOG[name]["simple_definition"]
            example_title = EXCEPTION_CATALOG[name]["title"]
            example_code = EXCEPTION_CATALOG[name]["code"]
        elif is_cls and ("Error" in name or "Exception" in name or "Warning" in name):
            simple_def = f"`{name}` is a standard Python built-in exception/warning class. It gets raised when this specific issue occurs, and can be caught and handled with `try / except {name}:`."
            example_title = f"Handling {name}"
            example_code = f"""# Real-world: Handling {name}
try:
    # Protected code block
    pass
except {name} as err:
    print(f'Caught {name}: {{err}}')"""
        elif is_cls:
            simple_def = f"`{name}` is a built-in Python type (like a blueprint) that you can use to create {name.lower()} objects. You don't need to import anything — it's always available."
            example_title = f"Using {name}"
            example_code = f"""# Creating and inspecting {name}
instance = {name}()
print('Created:', instance)
print('Type:', type(instance))"""
        else:
            simple_def = f"`{name}()` is a built-in function that comes with Python — no imports needed. {short_summary}"
            example_title = f"Using {name}()"
            example_code = f"""# Real-world usage of {name}
print('Callable built-in:', {name})"""

        gotchas = BUILTIN_GOTCHAS.get(name, [f"Standard {pos.lower()} available in all Python execution contexts without importing."])
        cross = CROSS_LANG_BUILTINS.get(name, {})

        # Version evolution timeline for notable built-ins
        timeline = []
        if name == "dict":
            timeline = [
                {"version": "1.0", "change_type": "feature", "title": "Built-in Hash Map", "description": "Standard dictionary type available since Python 1.0."},
                {"version": "3.6", "change_type": "optimization", "title": "Compact Hash Table", "description": "Raymond Hettinger compact dictionary implementation introduced in CPython, reducing memory by 20-25% and preserving insertion order as a side effect."},
                {"version": "3.7", "change_type": "feature", "title": "Insertion Order Guaranteed", "description": "Dictionary key insertion order became an official language specification guarantee for all Python implementations."},
                {"version": "3.9", "change_type": "pep", "title": "PEP 584 Dictionary Merge Operators", "description": "Added union operators | and |= to merge dictionaries.", "pep": "PEP 584"}
            ]

        cursor.execute("""
        INSERT INTO entries (
            slug, term, part_of_speech, pronunciation, category, signature,
            short_summary, simple_definition, full_description, parameters, returns, added_in_version,
            deprecated_in_version, pep_reference, pep_url, gotchas, cross_language, tags,
            senses, version_timeline
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            slug,
            name,
            pos,
            f"/{name}/",
            "builtin",
            sig_str,
            short_summary,
            simple_def,
            full_desc,
            json.dumps([]),
            json.dumps({"type": name if is_cls else "Any", "description": short_summary}),
            "2.0",
            None,
            "Python Built-in",
            f"https://docs.python.org/3/library/functions.html#{name}",
            json.dumps(gotchas),
            json.dumps(cross),
            json.dumps(["builtins", "core", "functions"]),
            json.dumps([]),
            json.dumps(timeline)
        ))

        cursor.execute("""
        INSERT INTO code_examples (entry_slug, title, code, expected_output, is_interactive)
        VALUES (?, ?, ?, ?, ?)
        """, (slug, example_title, example_code, None, 1))

        # FTS index
        cursor.execute("""
        INSERT INTO entries_fts (slug, term, short_summary, full_description, tags, category)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (slug, name, short_summary, full_desc, "builtins core functions", "builtin"))
        existing_slugs.add(slug)

    # 2. Process Core Keywords
    KEYWORDS = {
        "def": {"desc": "Defines a user-created function or method.", "sig": "def name(parameters): -> return_type"},
        "class": {"desc": "Defines a new class that acts as a blueprint for creating objects.", "sig": "class ClassName(BaseClass):"},
        "return": {"desc": "Exits a function and optionally passes a value back to the caller.", "sig": "return [expression]"},
        "if": {"desc": "Executes a block of code conditionally if its expression evaluates to truthy.", "sig": "if condition: ... elif: ... else:"},
        "for": {"desc": "Iterates over the items of any sequence or iterable in the order they appear.", "sig": "for target in iterable:"},
        "while": {"desc": "Repeats execution of a block of code as long as an expression remains true.", "sig": "while condition:"},
        "try": {"desc": "Wraps code blocks to catch and handle exceptions gracefully with except and finally.", "sig": "try: ... except Exception: ... finally:"},
        "with": {"desc": "Simplifies exception handling and resource cleanup by encapsulating common prep and clean-up tasks.", "sig": "with context_manager as target:"},
        "lambda": {"desc": "Creates small anonymous functions consisting of a single expression evaluated on call.", "sig": "lambda args: expression"},
        "pass": {"desc": "A null operation statement; nothing happens when it executes. Used as a syntactical placeholder.", "sig": "pass"},
        "raise": {"desc": "Explicitly raises an exception to interrupt normal control flow.", "sig": "raise ExceptionType('message')"},
        "assert": {"desc": "Debugging aid that tests an expression and raises AssertionError if it evaluates to False.", "sig": "assert condition, 'error message'"},
        "global": {"desc": "Declares that a variable name in the current block refers to a variable in the global module namespace.", "sig": "global var_name"},
        "nonlocal": {"desc": "Declares that a variable refers to a previously bound variable in the nearest enclosing non-global scope.", "sig": "nonlocal var_name"}
    }

    for kw, meta in KEYWORDS.items():
        if kw in existing_slugs:
            continue
        if kw in KEYWORD_CATALOG:
            kw_simple = KEYWORD_CATALOG[kw]["simple_definition"]
            kw_title = KEYWORD_CATALOG[kw]["title"]
            kw_code = KEYWORD_CATALOG[kw]["code"]
        else:
            kw_simple = f"`{kw}` is a reserved word in Python that you use for {meta['desc'].split('.')[0].lower()}. It's part of Python's grammar — you can't use it as a variable name."
            kw_title = f"Using {kw}"
            kw_code = f"# Keyword usage: {kw}\nprint('Python keyword:', '{kw}')"

        cursor.execute("""
        INSERT INTO entries (
            slug, term, part_of_speech, pronunciation, category, signature,
            short_summary, simple_definition, full_description, parameters, returns, added_in_version,
            deprecated_in_version, pep_reference, pep_url, gotchas, cross_language, tags,
            senses, version_timeline
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            kw,
            kw,
            "Language Keyword / Statement",
            f"/{kw}/",
            "keyword",
            meta["sig"],
            meta["desc"],
            kw_simple,
            f"The `{kw}` keyword is a core reserved syntax element in Python grammar.\n\n{meta['desc']}",
            json.dumps([]),
            json.dumps(None),
            "1.0",
            None,
            "Python Grammar",
            f"https://docs.python.org/3/reference/lexical_analysis.html#keywords",
            json.dumps([f"'{kw}' is a reserved keyword; you cannot use it as a variable, function, or class name."]),
            json.dumps({"JavaScript": kw, "Rust": kw, "Go": kw}),
            json.dumps(["keywords", "syntax", "grammar", "control-flow"]),
            json.dumps([]),
            json.dumps([])
        ))

        cursor.execute("""
        INSERT INTO code_examples (entry_slug, title, code, expected_output, is_interactive)
        VALUES (?, ?, ?, ?, ?)
        """, (kw, kw_title, kw_code, None, 1))

        cursor.execute("""
        INSERT INTO entries_fts (slug, term, short_summary, full_description, tags, category)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (kw, kw, meta["desc"], meta["desc"], "keywords syntax grammar control-flow", "keyword"))
        existing_slugs.add(kw)

    # 3. Process Standard Library Expansion
    for std in STDLIB_MODULES_TO_INGEST:
        mod_name = std["module"]
        try:
            mod = importlib.import_module(mod_name)
        except ImportError:
            continue

        for member_name in std["members"]:
            slug = f"{mod_name}-{member_name}".lower()
            if slug in existing_slugs or member_name in existing_slugs:
                continue

            if not hasattr(mod, member_name):
                continue

            obj = getattr(mod, member_name)
            is_fn = inspect.isbuiltin(obj) or inspect.isfunction(obj) or inspect.ismethod(obj)
            is_cls = inspect.isclass(obj)

            raw_doc = inspect.getdoc(obj) or ""
            lines = [l.strip() for l in raw_doc.split("\n") if l.strip()]
            summary = lines[0] if lines else f"{mod_name}.{member_name} standard library component."

            sig_str = f"{mod_name}.{member_name}(...)"
            try:
                sig = inspect.signature(obj)
                sig_str = f"{mod_name}.{member_name}{sig}"
            except Exception:
                pass

            pos = f"Standard Library {'Class' if is_cls else 'Function'}"
            full_desc = f"`{mod_name}.{member_name}` is a standard library {pos.lower()} provided by the `{mod_name}` module.\n\n{raw_doc}"

            code_snippet = f"import {mod_name}\nprint('Exploring {mod_name}.{member_name}:')\nprint(getattr({mod_name}, '{member_name}'))"
            if mod_name == "math" and member_name == "isclose":
                code_snippet = "import math\n# Avoid floating point comparison bugs (0.1 + 0.2 != 0.3)\nprint('Direct equality:', (0.1 + 0.2) == 0.3)\nprint('math.isclose:', math.isclose(0.1 + 0.2, 0.3))"
            elif mod_name == "math" and member_name == "comb":
                code_snippet = "import math\n# Combinations n choose k (Python 3.8+)\nprint('10 choose 3:', math.comb(10, 3))"
            elif mod_name == "math" and member_name == "gcd":
                code_snippet = "import math\nprint('GCD of 60 and 48:', math.gcd(60, 48))"
            elif mod_name == "re" and member_name == "compile":
                code_snippet = "import re\npattern = re.compile(r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b')\nprint('Compiled regex:', pattern)"
            elif mod_name == "json" and member_name == "dumps":
                code_snippet = "import json\ndata = {'title': 'PyKtionary', 'tags': ['python', 'lexicon'], 'stars': 100}\nprint(json.dumps(data, indent=2))"
            elif mod_name == "pathlib" and member_name == "Path":
                code_snippet = "from pathlib import Path\np = Path('/usr/local/bin')\nprint('Parent:', p.parent)\nprint('Name:', p.name)\nprint('Suffixes:', p.suffixes)"
            elif mod_name == "random" and member_name == "choice":
                code_snippet = "import random\noptions = ['Rock', 'Paper', 'Scissors']\nprint('Random pick:', random.choice(options))"
            elif mod_name == "hashlib" and member_name == "sha256":
                code_snippet = "import hashlib\nmsg = b'Hello Python'\nhash_hex = hashlib.sha256(msg).hexdigest()\nprint('SHA-256:', hash_hex)"

            std_simple = f"`{mod_name}.{member_name}` is a tool from Python's `{mod_name}` library. You need to `import {mod_name}` first, then call it. {summary}"
            cursor.execute("""
            INSERT INTO entries (
                slug, term, part_of_speech, pronunciation, category, signature,
                short_summary, simple_definition, full_description, parameters, returns, added_in_version,
                deprecated_in_version, pep_reference, pep_url, gotchas, cross_language, tags,
                senses, version_timeline
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                slug,
                f"{mod_name}.{member_name}",
                pos,
                f"/{member_name}/",
                "std_lib",
                sig_str,
                summary,
                std_simple,
                full_desc,
                json.dumps([]),
                json.dumps({"type": "Any", "description": summary}),
                "2.3",
                None,
                f"Module: {mod_name}",
                f"https://docs.python.org/3/library/{mod_name}.html#{mod_name}.{member_name}",
                json.dumps([f"Remember to `import {mod_name}` before accessing this member."]),
                json.dumps({}),
                json.dumps([mod_name, "std_lib", "utility"]),
                json.dumps([]),
                json.dumps([])
            ))

            cursor.execute("""
            INSERT INTO code_examples (entry_slug, title, code, expected_output, is_interactive)
            VALUES (?, ?, ?, ?, ?)
            """, (slug, f"Using {mod_name}.{member_name}", code_snippet, None, 1))

            cursor.execute("""
            INSERT INTO entries_fts (slug, term, short_summary, full_description, tags, category)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (slug, f"{mod_name}.{member_name}", summary, full_desc, f"{mod_name} std_lib utility", "std_lib"))
            existing_slugs.add(slug)

    conn.commit()
    conn.close()
    print("Extractor and Standard Library expansion completed successfully.")

if __name__ == "__main__":
    extract_builtins()
