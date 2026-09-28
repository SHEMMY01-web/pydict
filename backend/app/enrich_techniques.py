"""
PyKtionary — Expanded Programming Techniques Seeder
Enriches the database with Python programming techniques under category 'technique'.
"""

import json
import sqlite3
from pathlib import Path
import sys

# Ensure backend root is in sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.seed_techniques import TECHNIQUES, DB_PATH, export_mobile_offline

ADDITIONAL_TECHNIQUES = [
    {
        "slug": "walrus-operator",
        "term": "walrus operator",
        "part_of_speech": "noun",
        "pronunciation": "/ˈwɔːl.ɹəs ˈɒp.ə.ɹeɪ.tə/",
        "category": "technique",
        "signature": "NAME := expr",
        "short_summary": "The assignment expression operator, enabling naming and assignment of intermediate values directly inside expressions.",
        "full_description": "The **walrus operator** (`:=`), officially known as an **assignment expression**, assigns values to variables as part of a larger expression. Introduced in Python 3.8 via PEP 572, it avoids redundant recalculations in `while` loop conditions, `if` statements, and list comprehensions while keeping variable scoping concise.",
        "parameters": [
            {"name": "NAME", "type": "identifier", "description": "The variable name to receive the assigned value.", "default": None},
            {"name": "expr", "type": "expression", "description": "Any valid Python expression whose evaluation is assigned to NAME.", "default": None}
        ],
        "returns": {"type": "Any", "description": "Returns the value of the evaluated expression."},
        "added_in_version": "3.8",
        "deprecated_in_version": None,
        "pep_reference": "PEP 572",
        "pep_url": "https://peps.python.org/pep-0572/",
        "gotchas": [
            "Cannot be used for top-level unparenthesized assignment: `x := 1` is invalid syntax; use standard `x = 1`.",
            "Can impact code readability if deeply nested inside complex boolean or ternary expressions."
        ],
        "cross_language": {
            "C / C++": "if ((val = func()) != NULL)",
            "Go": "if val := func(); val != nil",
            "JavaScript": "if ((val = func()) !== null)",
            "Rust": "if let Some(val) = func()"
        },
        "tags": ["syntax", "technique", "walrus", "assignment", "pep-572"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "while (chunk := file.read(8192)):",
                "summary": "(programming, idioms) Assignment of loop condition values to eliminate pre-loop priming reads.",
                "parameters": [],
                "returns": {"type": "Any", "description": "Evaluated chunk value."},
                "example_code": "data = [12, 45, 78, 23, 90]\nif (n := len(data)) > 3:\n    print(f'Batch has {n} items — processing in bulk!')"
            },
            {
                "sense_number": 2,
                "part_of_speech": "noun",
                "signature": "[y for x in data if (y := transform(x)) > 0]",
                "summary": "(comprehension, optimization) Retaining expensive intermediate computation inside comprehension filters.",
                "parameters": [],
                "returns": {"type": "Any", "description": "Assigned intermediate filtered value."},
                "example_code": "words = ['apple', 'banana', 'kiwi', 'strawberry']\nlong_words = [upper for w in words if (upper := w.upper()) and len(upper) > 5]\nprint(long_words)  # ['BANANA', 'STRAWBERRY']"
            }
        ],
        "version_timeline": [
            {"version": "3.8", "summary": "Introduced via PEP 572 (Assignment Expressions)."}
        ],
        "examples": [
            {
                "title": "Stream Reading & Condition Assignment",
                "code": "sample_stream = ['line1\\n', 'line2\\n', 'END\\n', 'extra\\n']\niterator = iter(sample_stream)\n\nlines = []\nwhile (item := next(iterator, None)) and item != 'END\\n':\n    lines.append(item.strip())\n\nprint('Collected lines:', lines)",
                "expected_output": "Collected lines: ['line1', 'line2']",
                "is_interactive": 1
            }
        ]
    },
    {
        "slug": "eafp-lbyl",
        "term": "EAFP programming style",
        "part_of_speech": "noun",
        "pronunciation": "/iː.eɪ.ɛfˈpiː/",
        "category": "technique",
        "signature": "try: ... except Exception: ...",
        "short_summary": "'Easier to Ask for Forgiveness than Permission' — Python's idiomatic coding style preferring exception handling over preemptive checks.",
        "full_description": "**EAFP** (*Easier to Ask for Forgiveness than Permission*) is a cornerstone Python philosophy that assumes valid keys, files, and attributes exist, catching and handling `KeyError`, `AttributeError`, or `FileNotFoundError` if the assumption fails. It stands in contrast to **LBYL** (*Look Before You Leap*), which checks existence (`if key in dict`) before access. EAFP avoids race conditions (TOCTOU) and is faster when happy-path outcomes dominate.",
        "parameters": [],
        "returns": {"type": "None", "description": "Flow control paradigm."},
        "added_in_version": "2.0",
        "deprecated_in_version": None,
        "pep_reference": None,
        "pep_url": None,
        "gotchas": [
            "Never use bare `except:` clauses; always catch the specific exception expected (e.g. `except KeyError:`).",
            "In Python, exceptions are fast when not raised, but have a minor performance cost when triggered in tight loops."
        ],
        "cross_language": {
            "C": "LBYL dominant: if (ptr != NULL) { ... }",
            "Java": "LBYL preferred for control flow; exceptions discouraged for normal paths.",
            "Go": "Explicit error returns: if err != nil { ... }"
        },
        "tags": ["idiom", "technique", "philosophy", "error-handling", "eafp", "lbyl"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "try: obj.action() except AttributeError: fallback()",
                "summary": "(philosophy, architecture) Assuming duck typing capability and catching failure rather than type checking.",
                "parameters": [],
                "returns": {"type": "None", "description": "Idiom description."},
                "example_code": "user_profile = {'username': 'victor', 'role': 'admin'}\n\n# EAFP Idiom\ntry:\n    email = user_profile['email']\nexcept KeyError:\n    email = 'no-reply@python.org'\nprint('User email:', email)"
            }
        ],
        "version_timeline": [
            {"version": "2.0", "summary": "Recognized as standard Pythonic design ethos by CPython core developers."}
        ],
        "examples": [
            {
                "title": "EAFP vs LBYL Comparison",
                "code": "# LBYL style\nuser = {'name': 'Alice'}\nif 'name' in user:\n    greeting = 'Hello ' + user['name']\n\n# EAFP style (Pythonic)\ntry:\n    greeting = 'Hello ' + user['name']\nexcept KeyError:\n    greeting = 'Hello Guest'\n\nprint(greeting)",
                "expected_output": "Hello Alice",
                "is_interactive": 1
            }
        ]
    },
    {
        "slug": "args-kwargs",
        "term": "variadic arguments (*args, **kwargs)",
        "part_of_speech": "noun",
        "pronunciation": "/vɛə.ɹiˈæd.ɪk ˈɑːɡz ænd kwɑːɡz/",
        "category": "technique",
        "signature": "def func(*args, **kwargs): ...",
        "short_summary": "Syntactic conventions allowing functions to accept arbitrary positional and keyword arguments packed into a tuple and dictionary.",
        "full_description": "**Variadic arguments** (`*args` and `**kwargs`) allow a Python callable to receive an open-ended number of parameters. `*args` collects extraneous positional arguments into an immutable `tuple`, while `**kwargs` collects extraneous keyword arguments into a mutable `dict`. This technique is essential for writing decorators, higher-order functions, and subclass constructors.",
        "parameters": [
            {"name": "*args", "type": "tuple", "description": "Arbitrary positional arguments.", "default": "()"},
            {"name": "**kwargs", "type": "dict", "description": "Arbitrary keyword arguments.", "default": "{}"}
        ],
        "returns": {"type": "None", "description": "Parameter binding mechanism."},
        "added_in_version": "2.0",
        "deprecated_in_version": None,
        "pep_reference": "PEP 3102",
        "pep_url": "https://peps.python.org/pep-3102/",
        "gotchas": [
            "The names 'args' and 'kwargs' are conventions; the single and double asterisks `*` and `**` provide the syntax.",
            "Positional-only parameters (introduced in 3.8 with `/`) must appear before `*args`."
        ],
        "cross_language": {
            "JavaScript": "function func(...args)",
            "Java": "void func(Object... args)",
            "C#": "void Func(params object[] args)",
            "Rust": "Macros or slices: fn func(args: &[T])"
        },
        "tags": ["syntax", "technique", "functions", "unpacking", "decorators"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "def wrapper(*args, **kwargs): return target(*args, **kwargs)",
                "summary": "(decorators, delegation) Universal parameter forwarding without coupling to target function signatures.",
                "parameters": [],
                "returns": {"type": "Any", "description": "Forwarded return value."},
                "example_code": "def log_calls(fn):\n    def wrapper(*args, **kwargs):\n        print(f'Calling {fn.__name__} with args={args} kwargs={kwargs}')\n        return fn(*args, **kwargs)\n    return wrapper\n\n@log_calls\ndef add(a, b, bonus=0):\n    return a + b + bonus\n\nprint('Result:', add(5, 10, bonus=3))"
            }
        ],
        "version_timeline": [
            {"version": "2.0", "summary": "Core variadic parameter support."},
            {"version": "3.0", "summary": "PEP 3102 Keyword-Only Arguments introduced after *args."}
        ],
        "examples": [
            {
                "title": "Flexible Math Accumulator",
                "code": "def custom_sum(initial, *numbers, **metadata):\n    total = initial + sum(numbers)\n    unit = metadata.get('unit', '')\n    return f'{total} {unit}'.strip()\n\nprint(custom_sum(100, 5, 15, 20, unit='USD'))",
                "expected_output": "140 USD",
                "is_interactive": 1
            }
        ]
    },
    {
        "slug": "extended-slicing",
        "term": "extended sequence slicing",
        "part_of_speech": "noun",
        "pronunciation": "/ɪkˈstɛn.dɪd ˈslaɪ.sɪŋ/",
        "category": "technique",
        "signature": "sequence[start:stop:step]",
        "short_summary": "Indexing technique utilizing `start:stop:step` strides to carve, reverse, or subsample sequence data structures.",
        "full_description": "**Extended slicing** allows slicing sequences with an optional third `step` parameter (`sequence[start:stop:step]`). Negative steps reverse traversal (e.g. `seq[::-1]`), while positive steps sample items at uniform intervals. Slicing constructs and passes a built-in `slice(start, stop, step)` object to the underlying `__getitem__()` method.",
        "parameters": [
            {"name": "start", "type": "int", "description": "Starting index (inclusive). Defaults to 0 or end if step < 0.", "default": "None"},
            {"name": "stop", "type": "int", "description": "Stopping index (exclusive). Defaults to sequence length.", "default": "None"},
            {"name": "step", "type": "int", "description": "Stride increment. Negative values reverse direction.", "default": "1"}
        ],
        "returns": {"type": "Sequence", "description": "A new sequence of the same type containing extracted elements."},
        "added_in_version": "2.3",
        "deprecated_in_version": None,
        "pep_reference": "PEP 238",
        "pep_url": "https://peps.python.org/pep-0238/",
        "gotchas": [
            "Slicing a list or string creates a shallow copy in memory. For huge sequences, use `itertools.islice()` to avoid allocation.",
            "Assignment to extended slices (e.g. `lst[::2] = [...]`) requires the replacement sequence to match the exact slice length."
        ],
        "cross_language": {
            "JavaScript": "str.split('').reverse().join('') or Array.slice()",
            "Rust": "&slice[start..end]",
            "Go": "slice[low:high:max]"
        },
        "tags": ["syntax", "technique", "slicing", "sequences", "strings"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "text[::-1]",
                "summary": "(idiom) Idiomatic, highly optimized sequence reversal.",
                "parameters": [],
                "returns": {"type": "Sequence", "description": "Reversed sequence."},
                "example_code": "palindrome = 'racecar'\nis_palindrome = palindrome == palindrome[::-1]\nprint(f'{palindrome} is palindrome: {is_palindrome}')"
            }
        ],
        "version_timeline": [
            {"version": "2.3", "summary": "Extended slicing with step supported on all built-in sequence types."}
        ],
        "examples": [
            {
                "title": "Subsampling & Reversal",
                "code": "evens = list(range(10))[::2]\nreversed_evens = evens[::-1]\nprint('Evens:', evens)\nprint('Reversed:', reversed_evens)",
                "expected_output": "Evens: [0, 2, 4, 6, 8]\nReversed: [8, 6, 4, 2, 0]",
                "is_interactive": 1
            }
        ]
    },
    {
        "slug": "global-interpreter-lock",
        "term": "Global Interpreter Lock (GIL)",
        "part_of_speech": "noun",
        "pronunciation": "/ˈɡloʊ.bəl ɪnˈtɜː.pɹə.tə lɒk/",
        "category": "technique",
        "signature": "sys.getswitchinterval() / PEP 703 Free-Threading",
        "short_summary": "A mutex mechanism that protects Python objects, ensuring only one native thread executes Python bytecode at a time in CPython.",
        "full_description": "The **Global Interpreter Lock (GIL)** is a mutual-exclusion lock used by the CPython implementation to synchronize memory management and prevent race conditions with reference counting (`ob_refcnt`). Because of the GIL, CPU-bound Python multithreaded programs do not scale across multiple physical CPU cores (requiring `multiprocessing` or native C/Rust extensions instead). Python 3.13 introduces experimental free-threading via PEP 703 to disable the GIL.",
        "parameters": [],
        "returns": {"type": "None", "description": "CPython architectural subsystem."},
        "added_in_version": "1.5",
        "deprecated_in_version": None,
        "pep_reference": "PEP 703",
        "pep_url": "https://peps.python.org/pep-0703/",
        "gotchas": [
            "The GIL is released during I/O operations (network, disk read/write) and inside external C libraries like NumPy/OpenCV.",
            "Threads are still ideal for concurrency in I/O-bound tasks; use `concurrent.futures.ProcessPoolExecutor` for CPU-heavy parallelism."
        ],
        "cross_language": {
            "Java": "No GIL; true multithreading with fine-grained JVM memory locks.",
            "Go": "No GIL; goroutines scheduled natively across M:N OS threads.",
            "Node.js": "Single-threaded event loop by default, with Worker threads."
        },
        "tags": ["architecture", "technique", "concurrency", "gil", "pep-703"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "sys.getswitchinterval()",
                "summary": "(architecture, concurrency) The thread synchronization mechanism governing CPython bytecode evaluation.",
                "parameters": [],
                "returns": {"type": "float", "description": "Thread check interval in seconds."},
                "example_code": "import sys\nprint('CPython GIL thread switch interval:', sys.getswitchinterval(), 'seconds')"
            }
        ],
        "version_timeline": [
            {"version": "1.5", "summary": "Initial CPython GIL implementation."},
            {"version": "3.2", "summary": "New GIL implementation by Antoine Pitrou reducing thread starvation."},
            {"version": "3.13", "summary": "PEP 703 Experimental Free-Threading support (build without GIL)."}
        ],
        "examples": [
            {
                "title": "Inspecting GIL Switch Interval",
                "code": "import sys\ninterval = sys.getswitchinterval()\nprint(f'Thread switch interval: {interval * 1000:.1f} milliseconds')",
                "expected_output": "Thread switch interval: 5.0 milliseconds",
                "is_interactive": 1
            }
        ]
    },
    {
        "slug": "dunder-methods",
        "term": "dunder methods (data model)",
        "part_of_speech": "noun",
        "pronunciation": "/ˈdʌn.də ˈmɛθ.ədz/",
        "category": "technique",
        "signature": "def __special__(self, ...): ...",
        "short_summary": "Special double-underscore methods that hook directly into Python operators, iteration, formatting, and object lifecycle.",
        "full_description": "**Dunder methods** (short for *double underscore methods*, also known as *magic methods* or *special methods*) are predefined methods in Python's object data model. By implementing methods like `__init__`, `__repr__`, `__len__`, `__getitem__`, `__add__`, and `__iter__`, custom user classes seamlessly integrate with Python syntax operators (`+`, `in`, `len()`, `for x in obj:`) and standard library protocols.",
        "parameters": [],
        "returns": {"type": "None", "description": "Python data model convention."},
        "added_in_version": "2.0",
        "deprecated_in_version": None,
        "pep_reference": None,
        "pep_url": None,
        "gotchas": [
            "Never invent your own double-underscore methods like `__my_method__`; future Python versions might reserve the name.",
            "Dunder lookups bypass instance `__dict__` and are queried directly on the object's class for speed."
        ],
        "cross_language": {
            "C++": "Operator overloading: T operator+(const T& other)",
            "Ruby": "Method symbols: def +(other)",
            "Rust": "Trait implementations: impl std::ops::Add for MyStruct"
        },
        "tags": ["dunder", "technique", "oop", "data-model", "operators"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "def __str__(self): ...",
                "summary": "(oop, polymorphism) Implementing user-friendly string representation and arithmetic protocols.",
                "parameters": [],
                "returns": {"type": "str", "description": "Formatted string."},
                "example_code": "class Vector:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n    def __repr__(self):\n        return f'Vector({self.x}, {self.y})'\n    def __add__(self, other):\n        return Vector(self.x + other.x, self.y + other.y)\n\nv1 = Vector(2, 3)\nv2 = Vector(5, 7)\nprint('Added vectors:', v1 + v2)"
            }
        ],
        "version_timeline": [
            {"version": "2.2", "summary": "Unification of types and classes in Python's new-style object model."}
        ],
        "examples": [
            {
                "title": "Custom Collection Protocol",
                "code": "class BookShelf:\n    def __init__(self, books):\n        self._books = list(books)\n    def __len__(self):\n        return len(self._books)\n    def __getitem__(self, idx):\n        return self._books[idx]\n\nshelf = BookShelf(['Fluent Python', 'Automate the Boring Stuff'])\nprint('Length:', len(shelf))\nprint('First book:', shelf[0])",
                "expected_output": "Length: 2\nFirst book: Fluent Python",
                "is_interactive": 1
            }
        ]
    },
    {
        "slug": "contextlib-manager",
        "term": "generator-based context manager",
        "part_of_speech": "noun",
        "pronunciation": "/ˈdʒɛn.ə.ɹeɪ.tə beɪst ˈkɒn.tɛkst ˈmæn.ɪ.dʒə/",
        "category": "technique",
        "signature": "@contextmanager def helper(): yield",
        "short_summary": "Technique utilizing `contextlib.contextmanager` to turn generator functions with a single `yield` into robust context managers.",
        "full_description": "The **generator-based context manager** pattern uses the `@contextmanager` decorator from Python's standard `contextlib` module. Instead of writing a full class with boilerplate `__enter__` and `__exit__` methods, a developer writes a generator function containing a `try ... finally` block with a single `yield`. Everything before `yield` executes upon entering `with`, and everything after `yield` executes on exit.",
        "parameters": [
            {"name": "func", "type": "GeneratorFunction", "description": "A generator function yielding exactly once.", "default": None}
        ],
        "returns": {"type": "ContextManager", "description": "A callable object implementing __enter__ and __exit__."},
        "added_in_version": "2.5",
        "deprecated_in_version": None,
        "pep_reference": "PEP 343",
        "pep_url": "https://peps.python.org/pep-0343/",
        "gotchas": [
            "Always wrap the `yield` statement in a `try ... finally` block, otherwise exceptions in the `with` block will cause cleanup code to be skipped.",
            "If the generator yields more than once or fails to yield, a `RuntimeError` is raised."
        ],
        "cross_language": {
            "C#": "using (var res = new Resource()) { ... }",
            "Java": "try-with-resources: try (AutoCloseable res = ...) { ... }",
            "Rust": "RAII Drop trait implementation."
        },
        "tags": ["technique", "context-manager", "contextlib", "generators", "pep-343"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "@contextmanager def managed_resource(): ... yield ...",
                "summary": "(resource-management, idiom) Streamlining resource lifecycle management with generator yields.",
                "parameters": [],
                "returns": {"type": "Any", "description": "Yielded target resource."},
                "example_code": "import time\nfrom contextlib import contextmanager\n\n@contextmanager\ndef timer(label):\n    start = time.perf_counter()\n    try:\n        yield\n    finally:\n        elapsed = time.perf_counter() - start\n        print(f'{label}: {elapsed:.4f}s')\n\nwith timer('Loop'):\n    sum(i**2 for i in range(10000))"
            }
        ],
        "version_timeline": [
            {"version": "2.5", "summary": "Introduced in contextlib module via PEP 343."}
        ],
        "examples": [
            {
                "title": "Temporary State Modifier",
                "code": "from contextlib import contextmanager\n\nstate = {'debug': False}\n\n@contextmanager\ndef debug_mode():\n    old_state = state['debug']\n    state['debug'] = True\n    try:\n        yield\n    finally:\n        state['debug'] = old_state\n\nprint('Before:', state['debug'])\nwith debug_mode():\n    print('Inside with:', state['debug'])\nprint('After:', state['debug'])",
                "expected_output": "Before: False\nInside with: True\nAfter: False",
                "is_interactive": 1
            }
        ]
    },
    {
        "slug": "method-chaining",
        "term": "method chaining",
        "part_of_speech": "noun",
        "pronunciation": "/ˈmɛθ.əd ˈtʃeɪ.nɪŋ/",
        "category": "technique",
        "signature": "obj.step1().step2().step3()",
        "short_summary": "An object-oriented design technique where consecutive methods return `self` to allow sequential method invocations on a single line.",
        "full_description": "**Method chaining** (also known as a **fluent interface**) is an idiom where mutating or transforming methods of a class return the instance itself (`return self`). This allows callers to string together multiple operation calls sequentially without assigning intermediate variables. Common in query builders, data pipelines (pandas, Polars), and configuration objects.",
        "parameters": [],
        "returns": {"type": "Self", "description": "The current instance."},
        "added_in_version": "2.0",
        "deprecated_in_version": None,
        "pep_reference": "PEP 673 (typing.Self in Python 3.11)",
        "pep_url": "https://peps.python.org/pep-0673/",
        "gotchas": [
            "In Python standard library, in-place mutating methods like `list.sort()` and `list.reverse()` return `None` (by design, to avoid confusion with non-mutating equivalents `sorted()` and `reversed()`).",
            "Debugging multi-line chained statements can be harder if an exception occurs mid-chain unless formatted across multiple lines."
        ],
        "cross_language": {
            "JavaScript": "array.filter(...).map(...).reduce(...)",
            "Java": "Stream API / Builder pattern",
            "Rust": "Iterator method chaining: iter.filter().map().collect()"
        },
        "tags": ["oop", "technique", "fluent-interface", "design-pattern"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "class Builder: def add(self): return self",
                "summary": "(design-pattern, api-design) Cascading method calls on an object by returning self.",
                "parameters": [],
                "returns": {"type": "Self", "description": "Instance reference."},
                "example_code": "class QueryBuilder:\n    def __init__(self):\n        self.parts = []\n    def select(self, fields):\n        self.parts.append(f'SELECT {fields}')\n        return self\n    def from_table(self, table):\n        self.parts.append(f'FROM {table}')\n        return self\n    def build(self):\n        return ' '.join(self.parts)\n\nq = QueryBuilder().select('id, name').from_table('users').build()\nprint('Generated query:', q)"
            }
        ],
        "version_timeline": [
            {"version": "2.0", "summary": "Common design pattern in Python OOP."},
            {"version": "3.11", "summary": "PEP 673 introduces typing.Self to accurately annotate method chaining returns."}
        ],
        "examples": [
            {
                "title": "Fluent Calculator Chain",
                "code": "class Calculator:\n    def __init__(self, value=0):\n        self.value = value\n    def add(self, n):\n        self.value += n\n        return self\n    def multiply(self, n):\n        self.value *= n\n        return self\n    def get(self):\n        return self.value\n\nresult = Calculator(5).add(10).multiply(2).get()\nprint('Result of (5 + 10) * 2 =', result)",
                "expected_output": "Result of (5 + 10) * 2 = 30",
                "is_interactive": 1
            }
        ]
    }
]

def run_enrichment():
    all_tech = []
    # 1. Update existing techniques category to 'technique'
    for t in TECHNIQUES:
        t_copy = dict(t)
        t_copy["category"] = "technique"
        all_tech.append(t_copy)

    # 2. Append additional techniques
    all_tech.extend(ADDITIONAL_TECHNIQUES)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    inserted = 0
    updated = 0

    for t in all_tech:
        params_json = json.dumps(t.get("parameters", []))
        returns_json = json.dumps(t.get("returns", {}))
        gotchas_json = json.dumps(t.get("gotchas", []))
        cross_lang_json = json.dumps(t.get("cross_language", {}))
        tags_json = json.dumps(t.get("tags", []))
        senses_json = json.dumps(t.get("senses", []))
        timeline_json = json.dumps(t.get("version_timeline", []))

        existing = cursor.execute("SELECT id FROM entries WHERE slug = ?", (t["slug"],)).fetchone()
        if existing:
            cursor.execute("""
                UPDATE entries SET
                    term = ?,
                    part_of_speech = ?,
                    pronunciation = ?,
                    category = ?,
                    signature = ?,
                    short_summary = ?,
                    full_description = ?,
                    parameters = ?,
                    returns = ?,
                    added_in_version = ?,
                    deprecated_in_version = ?,
                    pep_reference = ?,
                    pep_url = ?,
                    gotchas = ?,
                    cross_language = ?,
                    tags = ?,
                    senses = ?,
                    version_timeline = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE slug = ?
            """, (
                t["term"], t["part_of_speech"], t["pronunciation"], t["category"],
                t["signature"], t["short_summary"], t["full_description"],
                params_json, returns_json, t["added_in_version"], t["deprecated_in_version"],
                t["pep_reference"], t["pep_url"], gotchas_json, cross_lang_json,
                tags_json, senses_json, timeline_json, t["slug"]
            ))
            updated += 1
        else:
            cursor.execute("""
                INSERT INTO entries (
                    slug, term, part_of_speech, pronunciation, category,
                    signature, short_summary, full_description, parameters,
                    returns, added_in_version, deprecated_in_version,
                    pep_reference, pep_url, gotchas, cross_language, tags,
                    senses, version_timeline
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                t["slug"], t["term"], t["part_of_speech"], t["pronunciation"], t["category"],
                t["signature"], t["short_summary"], t["full_description"],
                params_json, returns_json, t["added_in_version"], t["deprecated_in_version"],
                t["pep_reference"], t["pep_url"], gotchas_json, cross_lang_json,
                tags_json, senses_json, timeline_json
            ))
            inserted += 1

        # Code examples
        cursor.execute("DELETE FROM code_examples WHERE entry_slug = ?", (t["slug"],))
        for ex in t.get("examples", []):
            cursor.execute("""
                INSERT INTO code_examples (entry_slug, title, code, expected_output, is_interactive)
                VALUES (?, ?, ?, ?, ?)
            """, (t["slug"], ex["title"], ex["code"], ex.get("expected_output"), ex.get("is_interactive", 1)))

    conn.commit()
    conn.close()
    print(f"Enrichment finished: {inserted} inserted, {updated} updated (Total techniques: {len(all_tech)})")

    # Export to mobile bundle
    export_mobile_offline()

if __name__ == "__main__":
    run_enrichment()
