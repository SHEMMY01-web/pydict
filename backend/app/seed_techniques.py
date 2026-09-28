"""
PyKtionary — Advanced Python Techniques & Syntax Concepts Seeder
Enriches the database with core Python programming techniques in strict Wiktionary Vector format.
"""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "pyktionary.db"

TECHNIQUES = [
    {
        "slug": "list-comprehension",
        "term": "list comprehension",
        "part_of_speech": "noun",
        "pronunciation": "/lɪst kɒm.pɹɪˈhɛn.ʃən/",
        "category": "syntax",
        "signature": "[<expression> for <item> in <iterable> if <condition>]",
        "short_summary": "A concise syntactic construct for creating a new list by mapping and filtering elements of an existing iterable.",
        "full_description": "A **list comprehension** is a compact syntactic idiom in Python for constructing lists from existing iterables. It replaces verbose multi-line `for` loops and `list.append()` calls with a single readable expression inspired by set-builder notation in mathematics and functional programming languages such as Haskell.",
        "parameters": [
            {"name": "expression", "type": "Any", "description": "The value or transformation applied to each item to produce list elements.", "default": None},
            {"name": "item", "type": "variable", "description": "Loop variable bound to elements of the iterable.", "default": None},
            {"name": "iterable", "type": "Iterable", "description": "Any iterable sequence (list, tuple, range, generator, etc.).", "default": None},
            {"name": "condition", "type": "bool (optional)", "description": "Optional predicate filter; only items where this evaluates to truthy are included.", "default": "None"}
        ],
        "returns": {"type": "list", "description": "A newly allocated list containing the computed elements."},
        "added_in_version": "2.0",
        "deprecated_in_version": None,
        "pep_reference": "PEP 202",
        "pep_url": "https://peps.python.org/pep-0202/",
        "gotchas": [
            "Creates the entire list in memory eagerly. For massive sequences, prefer generator expressions `(...)`.",
            "In Python 2, the iteration variable leaked into the enclosing scope; fixed in Python 3 where comprehensions have their own local scope."
        ],
        "cross_language": {
            "Haskell": "[x * 2 | x <- list, x > 0]",
            "JavaScript": "list.filter(x => x > 0).map(x => x * 2)",
            "Rust": "list.into_iter().filter(|&x| x > 0).map(|x| x * 2).collect()",
            "C#": "from x in list where x > 0 select x * 2"
        },
        "tags": ["syntax", "comprehension", "functional", "pep-202"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "[expr for x in iterable]",
                "summary": "(programming, functional) An expression that constructs a new list by applying a transformation to every element of an iterable.",
                "parameters": [],
                "returns": {"type": "list", "description": "New transformed list."},
                "example_code": "squares = [x**2 for x in range(5)]\nprint(squares)  # [0, 1, 4, 9, 16]"
            },
            {
                "sense_number": 2,
                "part_of_speech": "noun",
                "signature": "[expr for x in iterable if condition]",
                "summary": "(programming, filtering) An expression that maps and filters items concurrently.",
                "parameters": [],
                "returns": {"type": "list", "description": "Filtered and transformed list."},
                "example_code": "evens = [x for x in range(10) if x % 2 == 0]\nprint(evens)  # [0, 2, 4, 6, 8]"
            }
        ],
        "version_timeline": [
            {"version": "2.0", "change_type": "introduced", "title": "List Comprehensions", "description": "Introduced via PEP 202.", "pep": "PEP 202"},
            {"version": "3.0", "change_type": "changed", "title": "Proper Lexical Scope", "description": "Comprehension variables no longer leak into outer scope.", "pep": "PEP 3100"}
        ],
        "examples": [
            {
                "title": "Basic Transformation & Filtering",
                "code": "# Square only positive odd numbers\nnumbers = [-3, -2, -1, 0, 1, 2, 3, 4, 5]\nresult = [x**2 for x in numbers if x > 0 and x % 2 != 0]\nprint(result)",
                "expected_output": "[1, 9, 25]",
                "is_interactive": True
            },
            {
                "title": "Flattening a 2D Matrix",
                "code": "matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nflat = [val for row in matrix for val in row]\nprint(flat)",
                "expected_output": "[1, 2, 3, 4, 5, 6, 7, 8, 9]",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "dict-comprehension",
        "term": "dict comprehension",
        "part_of_speech": "noun",
        "pronunciation": "/dɪkt kɒm.pɹɪˈhɛn.ʃən/",
        "category": "syntax",
        "signature": "{<key_expr>: <val_expr> for <item> in <iterable> if <condition>}",
        "short_summary": "A syntactic construct for generating a dictionary from an iterable of items.",
        "full_description": "A **dict comprehension** constructs a newly allocated `dict` object by evaluating key-value expression pairs over an iterable sequence, optionally applying conditional predicates.",
        "parameters": [
            {"name": "key_expr", "type": "Hashable", "description": "Expression computing the dictionary key.", "default": None},
            {"name": "val_expr", "type": "Any", "description": "Expression computing the associated dictionary value.", "default": None},
            {"name": "item", "type": "variable", "description": "Iteration variable.", "default": None},
            {"name": "iterable", "type": "Iterable", "description": "Source sequence.", "default": None}
        ],
        "returns": {"type": "dict", "description": "Newly allocated dictionary."},
        "added_in_version": "2.7",
        "deprecated_in_version": None,
        "pep_reference": "PEP 274",
        "pep_url": "https://peps.python.org/pep-0274/",
        "gotchas": [
            "If duplicate keys are produced during iteration, later values silently overwrite earlier values.",
            "Keys must evaluate to hashable objects."
        ],
        "cross_language": {
            "JavaScript": "Object.fromEntries(entries.map(([k, v]) => [k, v * 2]))",
            "Rust": "entries.into_iter().collect::<HashMap<_, _>>()",
            "C#": "list.ToDictionary(x => x.Key, x => x.Value)"
        },
        "tags": ["syntax", "comprehension", "dict", "pep-274"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "{k: v for item in iterable}",
                "summary": "(programming) An expression constructing a dictionary from mapped key-value pairs.",
                "parameters": [],
                "returns": {"type": "dict", "description": "Constructed dictionary."},
                "example_code": "lookup = {x: x**3 for x in range(4)}\nprint(lookup)  # {0: 0, 1: 1, 2: 8, 3: 27}"
            }
        ],
        "version_timeline": [
            {"version": "2.7", "change_type": "introduced", "title": "Dict Comprehensions Backported", "description": "Introduced in Python 3.0 and backported to 2.7 via PEP 274.", "pep": "PEP 274"}
        ],
        "examples": [
            {
                "title": "Inverting a Dictionary",
                "code": "original = {'a': 1, 'b': 2, 'c': 3}\ninverted = {v: k for k, v in original.items()}\nprint(inverted)",
                "expected_output": "{1: 'a', 2: 'b', 3: 'c'}",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "generator-expression",
        "term": "generator expression",
        "part_of_speech": "noun",
        "pronunciation": "/ˈdʒɛn.ə.ɹeɪ.tɚ ɪkˈspɹɛʃ.ən/",
        "category": "syntax",
        "signature": "(<expression> for <item> in <iterable> if <condition>)",
        "short_summary": "A lazy syntactic expression that yields items on demand without allocating entire collections in memory.",
        "full_description": "A **generator expression** is a memory-efficient comprehension enclosed in parentheses. Instead of building a concrete list or set in memory, it produces a generator object that computes values on-the-fly as requested by `next()` or iteration.",
        "parameters": [
            {"name": "expression", "type": "Any", "description": "Yielded value expression.", "default": None},
            {"name": "iterable", "type": "Iterable", "description": "Source sequence.", "default": None}
        ],
        "returns": {"type": "generator", "description": "An iterator object yielding items lazily."},
        "added_in_version": "2.4",
        "deprecated_in_version": None,
        "pep_reference": "PEP 289",
        "pep_url": "https://peps.python.org/pep-0289/",
        "gotchas": [
            "Can only be consumed once. Second iterations will be empty.",
            "Parentheses can be omitted when passed as the sole argument to a function: `sum(x**2 for x in range(10))`."
        ],
        "cross_language": {
            "Rust": "iter.map(|x| x * 2)",
            "C#": "list.Select(x => x * 2)",
            "JavaScript": "function* () { for(const x of list) yield x * 2; }"
        },
        "tags": ["syntax", "generator", "lazy-evaluation", "memory", "pep-289"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "(expr for x in iterable)",
                "summary": "(programming, memory) An iterator created via comprehension syntax evaluated lazily.",
                "parameters": [],
                "returns": {"type": "generator", "description": "Lazy generator object."},
                "example_code": "gen = (x * 2 for x in range(5))\nprint(next(gen))  # 0\nprint(next(gen))  # 2"
            }
        ],
        "version_timeline": [
            {"version": "2.4", "change_type": "introduced", "title": "Generator Expressions", "description": "Introduced via PEP 289 to avoid memory overhead of lists.", "pep": "PEP 289"}
        ],
        "examples": [
            {
                "title": "Summing Large Sequences with Zero Memory Overhead",
                "code": "# Summing squares without allocating a list of 1,000,000 ints\ntotal = sum(x**2 for x in range(100))\nprint('Sum of first 100 squares:', total)",
                "expected_output": "Sum of first 100 squares: 328350",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "decorator",
        "term": "decorator",
        "part_of_speech": "noun",
        "pronunciation": "/ˈdɛk.ə.ɹeɪ.tɚ/",
        "category": "concept",
        "signature": "@decorator_func\ndef target_func(): ...",
        "short_summary": "A callable that extends or alters the behavior of another function or class without modifying its code.",
        "full_description": "A **decorator** is a design pattern and syntactic feature (`@decorator`) in Python. It takes a callable as an argument, wraps or transforms it, and returns a new callable. It is syntactic sugar for `target = decorator(target)`.",
        "parameters": [
            {"name": "func", "type": "Callable", "description": "The function or class being wrapped.", "default": None}
        ],
        "returns": {"type": "Callable", "description": "The enhanced wrapper callable."},
        "added_in_version": "2.4",
        "deprecated_in_version": None,
        "pep_reference": "PEP 318",
        "pep_url": "https://peps.python.org/pep-0318/",
        "gotchas": [
            "Always use `functools.wraps` in wrapper functions to preserve the original function's `__name__`, `__doc__`, and signature.",
            "Decorator execution happens at function definition time (module import), not at call time."
        ],
        "cross_language": {
            "TypeScript": "@decorator class Example {}",
            "Java": "@Annotation",
            "C#": "[Attribute]"
        },
        "tags": ["concept", "metaprogramming", "decorators", "pep-318"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "@dec\ndef f(): ...",
                "summary": "(programming) A function that wraps another function to add cross-cutting behavior like logging, authorization, or caching.",
                "parameters": [],
                "returns": {"type": "Callable", "description": "Wrapped function."},
                "example_code": "def shout(f):\n    return lambda: f().upper()\n\n@shout\ndef greet():\n    return 'hello'\n\nprint(greet())  # 'HELLO'"
            }
        ],
        "version_timeline": [
            {"version": "2.4", "change_type": "introduced", "title": "Function Decorators", "description": "PEP 318 introduced `@` decorator syntax for functions.", "pep": "PEP 318"},
            {"version": "2.6", "change_type": "added", "title": "Class Decorators", "description": "PEP 3129 allowed decorators on class declarations.", "pep": "PEP 3129"}
        ],
        "examples": [
            {
                "title": "Timing & Logging Decorator",
                "code": "import time\nfrom functools import wraps\n\ndef measure(func):\n    @wraps(func)\n    def wrapper(*args, **kwargs):\n        start = time.perf_counter()\n        val = func(*args, **kwargs)\n        duration = time.perf_counter() - start\n        print(f'{func.__name__} executed in {duration:.4f}s')\n        return val\n    return wrapper\n\n@measure\ndef compute_factorial(n):\n    import math\n    return math.factorial(n)\n\nprint('Factorial 10:', compute_factorial(10))",
                "expected_output": "compute_factorial executed in 0.0000s\nFactorial 10: 3628800",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "context-manager",
        "term": "context manager",
        "part_of_speech": "noun",
        "pronunciation": "/ˈkɒn.tɛkst ˈmæn.ɪ.dʒɚ/",
        "category": "concept",
        "signature": "with <context_manager> as <target>: ...",
        "short_summary": "An object that manages the runtime context of a block of code, ensuring deterministic resource cleanup via __enter__ and __exit__.",
        "full_description": "A **context manager** is an object designed to be used in conjunction with the `with` statement. It encapsulates resource setup (`__enter__`) and guaranteed teardown (`__exit__`), ensuring resources like files, database connections, and locks are safely released even if unhandled exceptions occur.",
        "parameters": [
            {"name": "__enter__", "type": "method", "description": "Invoked before block execution; return value bound to `as target`.", "default": None},
            {"name": "__exit__", "type": "method", "description": "Invoked after block exit; receives (exc_type, exc_val, exc_tb).", "default": None}
        ],
        "returns": {"type": "Any", "description": "The target resource or context handle."},
        "added_in_version": "2.5",
        "deprecated_in_version": None,
        "pep_reference": "PEP 343",
        "pep_url": "https://peps.python.org/pep-0343/",
        "gotchas": [
            "If `__exit__` returns `True`, exceptions raised inside the block are suppressed; if it returns falsy, exceptions propagate.",
            "Can also be implemented cleanly using `@contextlib.contextmanager` and a single `yield` statement."
        ],
        "cross_language": {
            "C#": "using (var resource = new Resource()) { ... }",
            "Java": "try (Resource r = new Resource()) { ... }",
            "Go": "defer cleanup()",
            "Rust": "Drop trait / RAII"
        },
        "tags": ["concept", "context-manager", "with", "cleanup", "pep-343"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "with manager() as val:",
                "summary": "(programming) An object governing the acquisition and guaranteed release of external resources.",
                "parameters": [],
                "returns": {"type": "ContextManager", "description": "Active manager context."},
                "example_code": "with open('/tmp/test.txt', 'w') as f:\n    f.write('hello')\n# File handle automatically closed here"
            }
        ],
        "version_timeline": [
            {"version": "2.5", "change_type": "introduced", "title": "The with Statement", "description": "PEP 343 introduced context management protocol.", "pep": "PEP 343"},
            {"version": "3.10", "change_type": "enhanced", "title": "Parenthesized Context Managers", "description": "Allowed enclosing multiple context managers across lines inside parentheses.", "pep": "PEP 317"}
        ],
        "examples": [
            {
                "title": "Custom Timer Context Manager",
                "code": "import time\n\nclass ExecutionTimer:\n    def __enter__(self):\n        self.start = time.perf_counter()\n        return self\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        self.elapsed = time.perf_counter() - self.start\n        print(f'Elapsed: {self.elapsed:.4f}s')\n        return False\n\nwith ExecutionTimer():\n    total = sum(range(100_000))\nprint('Done calculation.')",
                "expected_output": "Elapsed: 0.0035s\nDone calculation.",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "generator",
        "term": "generator",
        "part_of_speech": "noun",
        "pronunciation": "/ˈdʒɛn.ə.ɹeɪ.tɚ/",
        "category": "concept",
        "signature": "def gen_func(): yield <value>",
        "short_summary": "A function that yields values incrementally using the yield statement, preserving local state between calls.",
        "full_description": "A **generator** is a function containing one or more `yield` statements. Calling it returns a generator iterator without running the function body immediately. Each call to `next()` advances execution until the next `yield` is encountered, freezing frame state until the subsequent request.",
        "parameters": [
            {"name": "yield", "type": "keyword", "description": "Yields an intermediate value and pauses execution.", "default": None}
        ],
        "returns": {"type": "GeneratorType", "description": "An iterator supporting `__next__()` and `.send()`."},
        "added_in_version": "2.2",
        "deprecated_in_version": None,
        "pep_reference": "PEP 255",
        "pep_url": "https://peps.python.org/pep-0255/",
        "gotchas": [
            "Once a generator raises `StopIteration` or runs out of code, attempting to advance it will raise `StopIteration` permanently.",
            "Generators are single-pass iterators. You cannot reset or rewind a generator."
        ],
        "cross_language": {
            "JavaScript": "function* gen() { yield 1; }",
            "C#": "IEnumerable<int> Gen() { yield return 1; }",
            "Rust": "impl Iterator for Gen"
        },
        "tags": ["concept", "iterator", "generator", "yield", "lazy"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "yield value",
                "summary": "(programming) A function that acts as an iterator producer, computing elements lazily on demand.",
                "parameters": [],
                "returns": {"type": "generator", "description": "Generator iterator."},
                "example_code": "def count(n):\n    for i in range(n):\n        yield i\n\nfor x in count(3):\n    print(x)"
            }
        ],
        "version_timeline": [
            {"version": "2.2", "change_type": "introduced", "title": "Simple Generators", "description": "PEP 255 introduced generator functions and the yield keyword.", "pep": "PEP 255"},
            {"version": "3.3", "change_type": "enhanced", "title": "yield from Syntax", "description": "PEP 380 enabled delegating to a sub-generator.", "pep": "PEP 380"}
        ],
        "examples": [
            {
                "title": "Infinite Fibonacci Generator",
                "code": "def fibonacci():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b\n\nfib = fibonacci()\nsequence = [next(fib) for _ in range(8)]\nprint('Fibonacci first 8:', sequence)",
                "expected_output": "Fibonacci first 8: [0, 1, 1, 2, 3, 5, 8, 13]",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "coroutine",
        "term": "coroutine",
        "part_of_speech": "noun",
        "pronunciation": "/koʊˈɹuː.tiːn/",
        "category": "concept",
        "signature": "async def func(): await <awaitable>",
        "short_summary": "A cooperative subroutine that can suspend execution via await and resume later without blocking the thread.",
        "full_description": "A **coroutine** is an asynchronous function defined with `async def`. When invoked, it returns a coroutine object without running. Coroutines collaborate with an event loop (such as `asyncio`), yielding control whenever I/O operations are awaiting completion, allowing massive concurrent I/O on a single thread.",
        "parameters": [
            {"name": "awaitable", "type": "Awaitable", "description": "A coroutine, Task, or Future object.", "default": None}
        ],
        "returns": {"type": "coroutine", "description": "Awaitable coroutine object."},
        "added_in_version": "3.5",
        "deprecated_in_version": None,
        "pep_reference": "PEP 492",
        "pep_url": "https://peps.python.org/pep-0492/",
        "gotchas": [
            "Calling an `async def` function without `await` or scheduling it on an event loop does not run the code and emits a `RuntimeWarning: coroutine was never awaited`.",
            "Do not execute CPU-bound heavy loops inside coroutines; they will block the entire event loop thread."
        ],
        "cross_language": {
            "JavaScript": "async function f() { await promise; }",
            "C#": "async Task F() { await task; }",
            "Rust": "async fn f() { future.await; }"
        },
        "tags": ["concept", "async", "asyncio", "concurrency", "pep-492"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "async def f(): ...",
                "summary": "(programming, concurrency) A function capable of asynchronous pause and resume operations.",
                "parameters": [],
                "returns": {"type": "coroutine", "description": "Async coroutine object."},
                "example_code": "import asyncio\nasync def fetch():\n    return 'data'\n# asyncio.run(fetch())"
            }
        ],
        "version_timeline": [
            {"version": "3.5", "change_type": "introduced", "title": "Native Coroutines", "description": "PEP 492 introduced async and await keywords.", "pep": "PEP 492"},
            {"version": "3.11", "change_type": "enhanced", "title": "TaskGroups", "description": "Introduced structured concurrency with asyncio.TaskGroup.", "pep": "PEP 654"}
        ],
        "examples": [
            {
                "title": "Concurrent Coroutine Execution",
                "code": "import asyncio\n\nasync def fetch_user(user_id):\n    await asyncio.sleep(0.01)  # Simulating network latency\n    return f'User_{user_id}'\n\nasync def main():\n    results = await asyncio.gather(fetch_user(1), fetch_user(2), fetch_user(3))\n    print('Fetched:', results)\n\nasyncio.run(main())",
                "expected_output": "Fetched: ['User_1', 'User_2', 'User_3']",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "duck-typing",
        "term": "duck typing",
        "part_of_speech": "noun",
        "pronunciation": "/dʌk ˈtaɪ.pɪŋ/",
        "category": "concept",
        "signature": "isinstance() avoidance / protocol adherence",
        "short_summary": "A dynamic typing discipline where an object's suitability is determined by its methods and attributes rather than class inheritance.",
        "full_description": "Derived from the aphorism *\"If it walks like a duck and quacks like a duck, it's a duck\"*, **duck typing** is the central design philosophy of Python object semantics. Functions do not verify explicit class hierarchies; instead, they attempt to invoke required methods (e.g. `read()`, `__iter__()`) directly (EAFP: Easier to Ask for Forgiveness than Permission).",
        "parameters": [],
        "returns": {"type": "concept", "description": "Semantic typing model."},
        "added_in_version": "1.0",
        "deprecated_in_version": None,
        "pep_reference": None,
        "pep_url": None,
        "gotchas": [
            "Over-relying on duck typing without defensive exception handling can lead to unexpected `AttributeError` at deep stack depths.",
            "Modern Python complements duck typing with `typing.Protocol` (PEP 544) for static validation of structural subtyping."
        ],
        "cross_language": {
            "Go": "Implicit structural interfaces",
            "TypeScript": "Structural type system",
            "Ruby": "Duck typing (core philosophy)"
        },
        "tags": ["concept", "typing", "oop", "eafp", "philosophy"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "obj.method()",
                "summary": "(programming) Polymorphism determined by attribute capability rather than nominal type.",
                "parameters": [],
                "returns": {"type": "None", "description": "Design concept."},
                "example_code": "class Duck:\n    def quack(self): return 'Quack!'\nclass Person:\n    def quack(self): return 'I am impersonating a duck!'\ndef make_it_quack(d):\n    print(d.quack())"
            }
        ],
        "version_timeline": [
            {"version": "3.8", "change_type": "formalized", "title": "Protocols (Structural Subtyping)", "description": "PEP 544 formalized static duck typing with typing.Protocol.", "pep": "PEP 544"}
        ],
        "examples": [
            {
                "title": "Duck Typing in Action",
                "code": "class FakeFile:\n    def read(self):\n        return 'Simulated file stream content'\n\ndef process_stream(stream):\n    # Any object with a .read() method works\n    content = stream.read()\n    print('Length:', len(content))\n\nprocess_stream(FakeFile())",
                "expected_output": "Length: 30",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "closure",
        "term": "closure",
        "part_of_speech": "noun",
        "pronunciation": "/ˈkloʊ.ʒɚ/",
        "category": "concept",
        "signature": "def outer(x): def inner(): return x",
        "short_summary": "A nested function that retains bindings to variables in its enclosing lexical scope even after the outer function has returned.",
        "full_description": "A **closure** is a function object that remembers values in enclosing scopes regardless of whether those scopes are still present in memory. Python implements closures via cell objects stored in the inner function's `__closure__` attribute, capturing read-only or mutable references (via `nonlocal`).",
        "parameters": [
            {"name": "nonlocal", "type": "keyword", "description": "Declares that a variable inside a nested function refers to a previously bound variable in the nearest enclosing scope.", "default": None}
        ],
        "returns": {"type": "function", "description": "Closure function holding captured cell references."},
        "added_in_version": "2.1",
        "deprecated_in_version": None,
        "pep_reference": "PEP 227",
        "pep_url": "https://peps.python.org/pep-0227/",
        "gotchas": [
            "Late binding gotcha: Closures in loops capture the variable reference, not the value at time of definition. Use default argument binding `def inner(x=x):` to capture values eagerly.",
            "Reassigning an enclosing variable without declaring `nonlocal` creates a local shadow variable instead."
        ],
        "cross_language": {
            "JavaScript": "function makeCounter() { let c = 0; return () => ++c; }",
            "Rust": "Closures with move keyword",
            "Go": "func() func() int { ... }"
        },
        "tags": ["concept", "functional", "scope", "closure", "nonlocal"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "def f(): ...",
                "summary": "(programming) A function carrying references to its lexical environment.",
                "parameters": [],
                "returns": {"type": "function", "description": "Bound closure."},
                "example_code": "def make_multiplier(n):\n    return lambda x: x * n\ndouble = make_multiplier(2)\nprint(double(5))  # 10"
            }
        ],
        "version_timeline": [
            {"version": "2.1", "change_type": "introduced", "title": "Statically Nested Scopes", "description": "PEP 227 introduced full lexical closures in Python.", "pep": "PEP 227"},
            {"version": "3.0", "change_type": "enhanced", "title": "The nonlocal Keyword", "description": "PEP 3104 added nonlocal to allow re-binding enclosing variables.", "pep": "PEP 3104"}
        ],
        "examples": [
            {
                "title": "Stateful Counter Closure with nonlocal",
                "code": "def create_counter(start=0):\n    count = start\n    def increment(step=1):\n        nonlocal count\n        count += step\n        return count\n    return increment\n\ncounter = create_counter(10)\nprint(counter())    # 11\nprint(counter(5))   # 16\nprint(counter())    # 17",
                "expected_output": "11\n16\n17",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "dataclass",
        "term": "dataclass",
        "part_of_speech": "noun",
        "pronunciation": "/ˈdeɪ.tə.klæs/",
        "category": "concept",
        "signature": "@dataclass\nclass Point:\n    x: float\n    y: float",
        "short_summary": "A decorator that automatically generates boilerplate special methods (__init__, __repr__, __eq__) from class type annotations.",
        "full_description": "Introduced in Python 3.7 via PEP 557, **dataclasses** provide a clean declarative syntax for classes primarily intended to store state. The `@dataclass` decorator inspects class annotations and generates `__init__`, `__repr__`, `__eq__`, and optionally comparison (`__lt__`) and immutability (`frozen=True`) methods automatically.",
        "parameters": [
            {"name": "init", "type": "bool", "description": "Generate `__init__` method.", "default": "True"},
            {"name": "repr", "type": "bool", "description": "Generate formatted `__repr__` method.", "default": "True"},
            {"name": "eq", "type": "bool", "description": "Generate equality comparison `__eq__` method.", "default": "True"},
            {"name": "order", "type": "bool", "description": "Generate `<, <=, >, >=` comparison methods.", "default": "False"},
            {"name": "frozen", "type": "bool", "description": "Make instances immutable (read-only attributes).", "default": "False"},
            {"name": "slots", "type": "bool", "description": "Generate `__slots__` automatically (Python 3.10+).", "default": "False"}
        ],
        "returns": {"type": "type", "description": "The decorated class with generated dunder methods."},
        "added_in_version": "3.7",
        "deprecated_in_version": None,
        "pep_reference": "PEP 557",
        "pep_url": "https://peps.python.org/pep-0557/",
        "gotchas": [
            "Mutable default values (like `list` or `dict`) must use `field(default_factory=list)` to avoid sharing instances across objects.",
            "Inheritance order matters: subclasses cannot define non-default fields after a parent class has defined default fields."
        ],
        "cross_language": {
            "Kotlin": "data class Point(val x: Double, val y: Double)",
            "Scala": "case class Point(x: Double, y: Double)",
            "Rust": "#[derive(Debug, PartialEq)] struct Point { ... }",
            "C#": "public record Point(double X, double Y);"
        },
        "tags": ["concept", "oop", "dataclass", "boilerplate", "pep-557"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "@dataclass class C: ...",
                "summary": "(programming, OOP) A declarative class generator eliminating repetitive constructor and representation boilerplate.",
                "parameters": [],
                "returns": {"type": "class", "description": "Enriched class type."},
                "example_code": "from dataclasses import dataclass\n@dataclass\nclass User:\n    id: int\n    name: str = 'Anonymous'\nu = User(1)\nprint(u)  # User(id=1, name='Anonymous')"
            }
        ],
        "version_timeline": [
            {"version": "3.7", "change_type": "introduced", "title": "Data Classes", "description": "PEP 557 introduced the dataclasses module.", "pep": "PEP 557"},
            {"version": "3.10", "change_type": "enhanced", "title": "slots Parameter", "description": "Added slots=True and kw_only parameters.", "pep": "PEP 603"}
        ],
        "examples": [
            {
                "title": "Immutable & Comparable Dataclass",
                "code": "from dataclasses import dataclass, field\n\n@dataclass(frozen=True, order=True)\nclass PriorityItem:\n    priority: int\n    name: str = field(compare=False)\n\na = PriorityItem(1, 'Task A')\nb = PriorityItem(2, 'Task B')\nprint('Is a < b?', a < b)\nprint('Repr:', a)",
                "expected_output": "Is a < b? True\nRepr: PriorityItem(priority=1, name='Task A')",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "type-hinting",
        "term": "type hinting",
        "part_of_speech": "noun",
        "pronunciation": "/taɪp ˈhɪn.tɪŋ/",
        "category": "concept",
        "signature": "def greet(name: str) -> str: ...",
        "short_summary": "A formal syntax for annotating variables, function arguments, and return types for static type analysis.",
        "full_description": "Python **type hints** (type annotations) allow developers to declare explicit types for static analysis tools like `mypy`, IDE autocomplete engines, and runtime validators (e.g. `pydantic`). Python itself does not enforce types at runtime; type hints are purely annotations accessible via `__annotations__`.",
        "parameters": [
            {"name": "annotation", "type": "type expression", "description": "Type specification, e.g. `int`, `str | None`, `list[int]`.", "default": None}
        ],
        "returns": {"type": "None", "description": "Annotations do not alter runtime execution."},
        "added_in_version": "3.5",
        "deprecated_in_version": None,
        "pep_reference": "PEP 484",
        "pep_url": "https://peps.python.org/pep-0484/",
        "gotchas": [
            "Python does not throw TypeError at runtime if you pass the wrong type; validation is strictly static unless a runtime library is used.",
            "Forward references (using a class before it is defined) required string quotes `'MyClass'` until `from __future__ import annotations` (PEP 563)."
        ],
        "cross_language": {
            "TypeScript": "function greet(name: string): string { ... }",
            "PHP": "function greet(string $name): string { ... }",
            "Rust": "fn greet(name: &str) -> String { ... }"
        },
        "tags": ["concept", "typing", "annotations", "mypy", "pep-484"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "x: int = 5",
                "summary": "(programming) Syntactic type metadata attached to variable declarations and function signatures.",
                "parameters": [],
                "returns": {"type": "None", "description": "Static annotation."},
                "example_code": "def double(val: int) -> int:\n    return val * 2"
            }
        ],
        "version_timeline": [
            {"version": "3.5", "change_type": "introduced", "title": "Type Hints", "description": "PEP 484 introduced standard type hints.", "pep": "PEP 484"},
            {"version": "3.9", "change_type": "enhanced", "title": "Built-in Generics", "description": "PEP 585 enabled using list[int] directly instead of typing.List.", "pep": "PEP 585"},
            {"version": "3.10", "change_type": "enhanced", "title": "Union Operator |", "description": "PEP 604 enabled X | Y syntax instead of typing.Union[X, Y].", "pep": "PEP 604"}
        ],
        "examples": [
            {
                "title": "Modern Modern Type Hints (Python 3.10+)",
                "code": "def process_id(identifier: int | str) -> dict[str, str]:\n    return {'id': str(identifier), 'status': 'active'}\n\nprint(process_id(101))\nprint(process_id('USR_404'))",
                "expected_output": "{'id': '101', 'status': 'active'}\n{'id': 'USR_404', 'status': 'active'}",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "memoization",
        "term": "memoization",
        "part_of_speech": "noun",
        "pronunciation": "/ˌmɛm.oʊ.ɪˈzeɪ.ʃən/",
        "category": "concept",
        "signature": "@functools.lru_cache(maxsize=128)\ndef expensive(n): ...",
        "short_summary": "An optimization technique that caches the return values of expensive function calls based on input arguments.",
        "full_description": "Derived from the Latin *memorandum*, **memoization** is a functional caching strategy that eliminates redundant calculations. In Python, the standard library provides `@functools.cache` (unbounded) and `@functools.lru_cache` (Least Recently Used bounded cache), converting exponential recursive functions into linear time algorithms.",
        "parameters": [
            {"name": "maxsize", "type": "int | None", "description": "Maximum number of cached entries. If None, LRU logic is disabled and cache is unbounded.", "default": "128"},
            {"name": "typed", "type": "bool", "description": "If True, arguments of different types are cached separately (e.g. 3 and 3.0).", "default": "False"}
        ],
        "returns": {"type": "Callable", "description": "Cached function wrapper with `.cache_info()` and `.cache_clear()`."},
        "added_in_version": "3.2",
        "deprecated_in_version": None,
        "pep_reference": None,
        "pep_url": None,
        "gotchas": [
            "All function arguments must be hashable objects (e.g. tuples instead of lists).",
            "Functions with side-effects (e.g. network requests or database mutations) should not be memoized."
        ],
        "cross_language": {
            "JavaScript": "lodash.memoize(fn)",
            "Clojure": "(memoize fn)",
            "Go": "sync.Map memoized closures"
        },
        "tags": ["concept", "optimization", "caching", "functools", "lru_cache"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "@lru_cache def f(): ...",
                "summary": "(optimization) Deterministic function caching based on argument hash keys.",
                "parameters": [],
                "returns": {"type": "Callable", "description": "Cached wrapper."},
                "example_code": "from functools import cache\n@cache\ndef fib(n):\n    return n if n < 2 else fib(n-1) + fib(n-2)\nprint(fib(30))  # 832040 (instantaneous)"
            }
        ],
        "version_timeline": [
            {"version": "3.2", "change_type": "introduced", "title": "lru_cache", "description": "functools.lru_cache added to standard library."},
            {"version": "3.9", "change_type": "added", "title": "functools.cache", "description": "Added simpler unbounded cache decorator."}
        ],
        "examples": [
            {
                "title": "Exponential to Linear Recursion with @cache",
                "code": "from functools import cache\n\n@cache\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\n\nprint('Fib(35):', fib(35))\nprint('Cache stats:', fib.cache_info())",
                "expected_output": "Fib(35): 9227465\nCache stats: CacheInfo(hits=33, misses=36, maxsize=None, currsize=36)",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "lambda-expression",
        "term": "lambda expression",
        "part_of_speech": "noun",
        "pronunciation": "/ˈlæm.də ɪkˈspɹɛʃ.ən/",
        "category": "syntax",
        "signature": "lambda <arguments>: <expression>",
        "short_summary": "An anonymous, inline function construct restricted to a single evaluated expression.",
        "full_description": "A **lambda expression** creates an anonymous function object at runtime. Unlike standard functions defined with `def`, lambdas are syntactically restricted to a single expression whose evaluated result is automatically returned. They are commonly passed as key functions to `sorted()`, `min()`, `max()`, and higher-order functions.",
        "parameters": [
            {"name": "arguments", "type": "parameter list", "description": "Comma-separated list of formal parameters.", "default": None},
            {"name": "expression", "type": "Any", "description": "Single expression evaluated and returned.", "default": None}
        ],
        "returns": {"type": "function", "description": "An anonymous function object."},
        "added_in_version": "1.0",
        "deprecated_in_version": None,
        "pep_reference": None,
        "pep_url": None,
        "gotchas": [
            "Cannot contain statements (e.g. `pass`, `return`, `assert`, or assignments).",
            "PEP 8 discourages binding a lambda directly to an identifier (`f = lambda x: ...`); use standard `def f(x):` instead for clearer tracebacks."
        ],
        "cross_language": {
            "JavaScript": "(x, y) => x + y",
            "Java": "(x, y) -> x + y",
            "Rust": "|x, y| x + y",
            "C#": "(x, y) => x + y"
        },
        "tags": ["syntax", "functional", "lambda", "anonymous-function"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "lambda x: expr",
                "summary": "(programming, functional) An inline anonymous function.",
                "parameters": [],
                "returns": {"type": "function", "description": "Callable function."},
                "example_code": "double = lambda x: x * 2\nprint(double(4))  # 8"
            }
        ],
        "version_timeline": [
            {"version": "1.0", "change_type": "introduced", "title": "Lambda Syntax", "description": "Introduced in Python 1.0 along with map, filter, and reduce."}
        ],
        "examples": [
            {
                "title": "Custom Sorting with Lambda Key",
                "code": "users = [\n    {'name': 'Alice', 'score': 88},\n    {'name': 'Bob', 'score': 95},\n    {'name': 'Charlie', 'score': 72}\n]\n# Sort by score descending\nranked = sorted(users, key=lambda u: u['score'], reverse=True)\nfor u in ranked:\n    print(f\"{u['name']}: {u['score']}\")",
                "expected_output": "Bob: 95\nAlice: 88\nCharlie: 72",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "set-comprehension",
        "term": "set comprehension",
        "part_of_speech": "noun",
        "pronunciation": "/sɛt kɒm.pɹɪˈhɛn.ʃən/",
        "category": "syntax",
        "signature": "{<expression> for <item> in <iterable> if <condition>}",
        "short_summary": "A syntactic construct for generating a unique, unordered set from an iterable.",
        "full_description": "A **set comprehension** constructs a newly allocated `set` object, deduplicating elements by applying an expression to items in an iterable. Introduced in Python 2.7 and 3.0 via PEP 274.",
        "parameters": [
            {"name": "expression", "type": "Hashable", "description": "Expression computing elements added to the set.", "default": None},
            {"name": "iterable", "type": "Iterable", "description": "Source sequence.", "default": None}
        ],
        "returns": {"type": "set", "description": "Constructed set of unique hashable elements."},
        "added_in_version": "2.7",
        "deprecated_in_version": None,
        "pep_reference": "PEP 274",
        "pep_url": "https://peps.python.org/pep-0274/",
        "gotchas": [
            "All produced items must be hashable. Sets cannot contain lists or dicts.",
            "`{}` creates an empty dict, not an empty set; use `set()` for empty sets."
        ],
        "cross_language": {
            "JavaScript": "new Set(array.map(x => x * 2))",
            "Rust": "list.into_iter().collect::<HashSet<_>>()",
            "Haskell": "Data.Set.fromList [x * 2 | x <- list]"
        },
        "tags": ["syntax", "comprehension", "set", "pep-274"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "{expr for x in iterable}",
                "summary": "(programming) An expression constructing a unique set from mapped items.",
                "parameters": [],
                "returns": {"type": "set", "description": "Unique set collection."},
                "example_code": "words = ['apple', 'pear', 'apple', 'banana']\nlengths = {len(w) for w in words}\nprint(lengths)  # {4, 5, 6}"
            }
        ],
        "version_timeline": [
            {"version": "2.7", "change_type": "introduced", "title": "Set Comprehensions", "description": "PEP 274 added set comprehensions.", "pep": "PEP 274"}
        ],
        "examples": [
            {
                "title": "Extracting Unique Word Lengths",
                "code": "text = 'the quick brown fox jumps over the lazy dog'\nvowels = {char for char in text if char in 'aeiou'}\nprint('Unique vowels found:', sorted(vowels))",
                "expected_output": "Unique vowels found: ['a', 'e', 'i', 'o', 'u']",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "monkey-patching",
        "term": "monkey patching",
        "part_of_speech": "noun",
        "pronunciation": "/ˈmʌŋ.ki ˈpætʃ.ɪŋ/",
        "category": "concept",
        "signature": "target_module.target_func = custom_func",
        "short_summary": "The dynamic runtime modification of a module, class, or function's attributes or behavior.",
        "full_description": "Derived etymologically from *guerrilla patching* corrupted into *gorilla*, and softened to **monkey patching**, this dynamic programming technique alters code at runtime without modifying original source files. Widely utilized in unit testing (mocking network calls) and gevent/eventlet async event-loop patching.",
        "parameters": [],
        "returns": {"type": "None", "description": "In-place runtime modification."},
        "added_in_version": "1.0",
        "deprecated_in_version": None,
        "pep_reference": None,
        "pep_url": None,
        "gotchas": [
            "Introduces subtle non-deterministic side-effects if patches bleed across test suites. Always un-patch or use `unittest.mock.patch` as a context manager.",
            "Can break C-extension types (e.g. `str`, `int`, `list`) whose attributes are immutable and raise `TypeError: can't set attributes on built-in type`."
        ],
        "cross_language": {
            "Ruby": "Open classes / Monkey patching",
            "JavaScript": "Prototype pollution / runtime reassignment",
            "Go": "Not supported (compiled static binary)"
        },
        "tags": ["concept", "dynamic", "testing", "metaprogramming"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "obj.attr = new_val",
                "summary": "(programming, dynamic) Overwriting methods or attributes of a class or module at runtime.",
                "parameters": [],
                "returns": {"type": "None", "description": "Attribute rebinding."},
                "example_code": "import math\nmath.cos = lambda x: 42.0  # Patched cosine\nprint(math.cos(0))  # 42.0"
            }
        ],
        "version_timeline": [
            {"version": "3.3", "change_type": "standardized", "title": "unittest.mock in stdlib", "description": "PEP 0413 standardized mock patching tools in standard library."}
        ],
        "examples": [
            {
                "title": "Mocking Network Call with Monkey Patching",
                "code": "class PaymentGateway:\n    def charge(self, amount):\n        return f'Live charge of ${amount}'\n\n# Patching charge method for testing\ndef mock_charge(self, amount):\n    return f'MOCK OK: ${amount}'\n\nPaymentGateway.charge = mock_charge\ngateway = PaymentGateway()\nprint(gateway.charge(100))",
                "expected_output": "MOCK OK: $100",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "metaclass",
        "term": "metaclass",
        "part_of_speech": "noun",
        "pronunciation": "/ˈmɛt.ə.klæs/",
        "category": "concept",
        "signature": "class Meta(type):\n    def __new__(cls, name, bases, dct): ...",
        "short_summary": "A class whose instances are themselves classes; the blueprint and constructor of class definitions.",
        "full_description": "In Python's object model, *everything is an object, and classes are instances of metaclasses*. The default metaclass is `type`. Defining a custom metaclass inherits from `type` and overrides `__new__` or `__init__`, enabling deep metaprogramming such as automatic registry pattern, API validation, and ORM field synthesis.",
        "parameters": [
            {"name": "name", "type": "str", "description": "Name of the class being created.", "default": None},
            {"name": "bases", "type": "tuple[type]", "description": "Tuple of parent base classes.", "default": None},
            {"name": "dct", "type": "dict", "description": "Class namespace dictionary of methods and attributes.", "default": None}
        ],
        "returns": {"type": "type", "description": "A newly constructed class object."},
        "added_in_version": "2.2",
        "deprecated_in_version": None,
        "pep_reference": "PEP 3115",
        "pep_url": "https://peps.python.org/pep-3115/",
        "gotchas": [
            "Tim Peters quote: *'Metaclasses are deeper magic than 99% of users should ever worry about. If you wonder whether you need them, you don't.'*",
            "In Python 3.6+, `__init_subclass__` (PEP 487) satisfies 90% of metaclass use-cases with far less complexity."
        ],
        "cross_language": {
            "Ruby": "Eigenclasses / Singleton classes",
            "Smalltalk": "Metaclass architecture",
            "C++": "Template metaprogramming"
        },
        "tags": ["concept", "metaprogramming", "oop", "pep-3115"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "class M(type): ...",
                "summary": "(programming, OOP) The constructor class responsible for instantiating new class definitions.",
                "parameters": [],
                "returns": {"type": "type", "description": "Constructed class."},
                "example_code": "class AutoRegister(type):\n    registry = {}\n    def __new__(cls, name, bases, dct):\n        new_cls = super().__new__(cls, name, bases, dct)\n        cls.registry[name] = new_cls\n        return new_cls"
            }
        ],
        "version_timeline": [
            {"version": "3.0", "change_type": "changed", "title": "metaclass Keyword", "description": "Replaced __metaclass__ attribute with class MyClass(metaclass=M): syntax.", "pep": "PEP 3115"},
            {"version": "3.6", "change_type": "alternative", "title": "__init_subclass__", "description": "PEP 487 provided a simpler alternative to metaclasses.", "pep": "PEP 487"}
        ],
        "examples": [
            {
                "title": "Plugin Auto-Registration Metaclass",
                "code": "class PluginRegistry(type):\n    plugins = []\n    def __new__(cls, name, bases, dct):\n        new_class = super().__new__(cls, name, bases, dct)\n        if bases:  # Don't register the base class itself\n            cls.plugins.append(new_class)\n        return new_class\n\nclass BasePlugin(metaclass=PluginRegistry):\n    pass\n\nclass JsonExporter(BasePlugin):\n    pass\n\nclass CsvExporter(BasePlugin):\n    pass\n\nprint('Registered plugins:', [p.__name__ for p in PluginRegistry.plugins])",
                "expected_output": "Registered plugins: ['JsonExporter', 'CsvExporter']",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "dunder-slots",
        "term": "__slots__",
        "part_of_speech": "noun",
        "pronunciation": "/ˈslɒts/",
        "category": "dunder",
        "signature": "class Point:\n    __slots__ = ('x', 'y')",
        "short_summary": "A class attribute that statically declares instance attributes, eliminating per-instance __dict__ and optimizing memory.",
        "full_description": "By default, Python instances store attributes in a dynamic dictionary (`__dict__`). Declaring `__slots__ = ('attr1', 'attr2')` instructs Python to allocate a fixed-size descriptor array, reducing memory usage by 40-60% and speeding up attribute access.",
        "parameters": [
            {"name": "__slots__", "type": "Iterable[str]", "description": "Tuple or list of valid instance attribute names.", "default": None}
        ],
        "returns": {"type": "None", "description": "Class declaration directive."},
        "added_in_version": "2.2",
        "deprecated_in_version": None,
        "pep_reference": None,
        "pep_url": None,
        "gotchas": [
            "Instances without `__dict__` cannot have new attributes assigned dynamically at runtime.",
            "Subclasses must also declare `__slots__` or they will automatically create a `__dict__`."
        ],
        "cross_language": {
            "C": "struct fields",
            "Rust": "struct layout",
            "Java": "Standard class fields"
        },
        "tags": ["dunder", "memory", "optimization", "slots", "oop"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "__slots__ = ('a', 'b')",
                "summary": "(memory, OOP) Fixed attribute declaration descriptor avoiding dynamic dictionary overhead.",
                "parameters": [],
                "returns": {"type": "None", "description": "Descriptor array allocation."},
                "example_code": "class SlotPoint:\n    __slots__ = ('x', 'y')\n    def __init__(self, x, y):\n        self.x, self.y = x, y"
            }
        ],
        "version_timeline": [
            {"version": "2.2", "change_type": "introduced", "title": "New-Style Classes & __slots__", "description": "Introduced descriptor-based slot allocation for memory efficiency."}
        ],
        "examples": [
            {
                "title": "Restricted Dynamic Attributes with __slots__",
                "code": "class StrictItem:\n    __slots__ = ('name', 'price')\n    def __init__(self, name, price):\n        self.name = name\n        self.price = price\n\nitem = StrictItem('Widget', 9.99)\nprint(f'{item.name}: ${item.price}')\ntry:\n    item.unknown = 'error'\nexcept AttributeError:\n    print('AttributeError caught as expected.')",
                "expected_output": "Widget: $9.99\nAttributeError caught as expected.",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "descriptor-protocol",
        "term": "descriptor protocol",
        "part_of_speech": "noun",
        "pronunciation": "/dɪˈskɹɪp.tɚ ˈpɹoʊ.tə.kɒl/",
        "category": "concept",
        "signature": "def __get__(self, instance, owner): ...",
        "short_summary": "The mechanism underlying properties, methods, and classmethods, overriding attribute access via __get__, __set__, and __delete__.",
        "full_description": "A **descriptor** is any object that implements at least one of `__get__()`, `__set__()`, or `__delete__()`. All Python methods, `@property`, `@classmethod`, and `@staticmethod` are implemented via descriptors.",
        "parameters": [
            {"name": "__get__", "type": "method", "description": "(self, instance, owner) -> value", "default": None},
            {"name": "__set__", "type": "method", "description": "(self, instance, value) -> None", "default": None},
            {"name": "__delete__", "type": "method", "description": "(self, instance) -> None", "default": None}
        ],
        "returns": {"type": "Any", "description": "Custom attribute resolution."},
        "added_in_version": "2.2",
        "deprecated_in_version": None,
        "pep_reference": None,
        "pep_url": None,
        "gotchas": [
            "Data descriptors take precedence over an instance's `__dict__`.",
            "Non-data descriptors can be shadowed by instance attributes."
        ],
        "cross_language": {
            "C#": "Property getters and setters",
            "JavaScript": "Object.defineProperty(obj, prop, { get, set })"
        },
        "tags": ["concept", "oop", "descriptor", "property", "internals"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "__get__(self, inst, owner)",
                "summary": "(programming, OOP) An object protocol customizing attribute access and assignment.",
                "parameters": [],
                "returns": {"type": "Any", "description": "Resolved attribute."},
                "example_code": "class Descr:\n    def __get__(self, instance, owner): return 42"
            }
        ],
        "version_timeline": [
            {"version": "2.2", "change_type": "introduced", "title": "Descriptor Protocol", "description": "Introduced with new-style classes to power properties and methods."},
            {"version": "3.6", "change_type": "enhanced", "title": "__set_name__", "description": "PEP 487 added __set_name__ hook to automatically capture attribute names."}
        ],
        "examples": [
            {
                "title": "Validation Descriptor with __set_name__",
                "code": "class ValidatedAge:\n    def __set_name__(self, owner, name):\n        self.private_name = f'_{name}'\n    def __get__(self, instance, owner):\n        return getattr(instance, self.private_name, 0)\n    def __set__(self, instance, value):\n        if not (0 <= value <= 130):\n            raise ValueError('Invalid age range.')\n        setattr(instance, self.private_name, value)\n\nclass Person:\n    age = ValidatedAge()\n\np = Person()\np.age = 25\nprint('Person age:', p.age)",
                "expected_output": "Person age: 25",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "f-string",
        "term": "f-string (formatted string literal)",
        "part_of_speech": "noun",
        "pronunciation": "/ˈɛf.stɹɪŋ/",
        "category": "syntax",
        "signature": "f\"Hello, {name}! Value is {value:.2f}\"",
        "short_summary": "A string literal prefixed with 'f' that evaluates interpolated expressions directly inside curly braces at runtime.",
        "full_description": "Introduced in Python 3.6 via PEP 498, **formatted string literals** (f-strings) provide readable and fast string interpolation. Expressions inside `{}` are evaluated in the current scope at runtime and formatted using Python's format specification mini-language.",
        "parameters": [
            {"name": "expression", "type": "Any", "description": "Python expression evaluated inside `{}`.", "default": None},
            {"name": "format_spec", "type": "str", "description": "Optional formatting rule following colon (e.g. `:.2f`).", "default": None}
        ],
        "returns": {"type": "str", "description": "Interpolated and formatted string."},
        "added_in_version": "3.6",
        "deprecated_in_version": None,
        "pep_reference": "PEP 498",
        "pep_url": "https://peps.python.org/pep-0498/",
        "gotchas": [
            "Cannot contain backslashes `\\` inside expressions in Python versions prior to 3.12.",
            "Use `{{` and `}}` to produce literal curly brace characters."
        ],
        "cross_language": {
            "JavaScript": "`Hello, ${name}!`",
            "C#": "$\"Hello, {name}!\"",
            "Ruby": "\"Hello, #{name}!\""
        },
        "tags": ["syntax", "strings", "formatting", "pep-498"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "f\"{var}\"",
                "summary": "(syntax, strings) A string literal evaluating embedded expressions.",
                "parameters": [],
                "returns": {"type": "str", "description": "Formatted string."},
                "example_code": "val = 3.14159\nprint(f'Pi is {val:.2f}')  # Pi is 3.14"
            }
        ],
        "version_timeline": [
            {"version": "3.6", "change_type": "introduced", "title": "Formatted String Literals", "description": "PEP 498 introduced f-strings.", "pep": "PEP 498"},
            {"version": "3.8", "change_type": "enhanced", "title": "Debug Specifier =", "description": "Added f'{x=}' which prints 'x=value' for rapid debugging."},
            {"version": "3.12", "change_type": "enhanced", "title": "Syntactic Formalization", "description": "PEP 701 lifted quote reuse and nesting restrictions."}
        ],
        "examples": [
            {
                "title": "Debug Specifier & Number Formatting",
                "code": "price = 49.95\nquantity = 3\ntotal = price * quantity\nprint(f'{price=} | {quantity=} | Total: ${total:,.2f}')",
                "expected_output": "price=49.95 | quantity=3 | Total: $149.85",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "structural-pattern-matching",
        "term": "structural pattern matching",
        "part_of_speech": "noun",
        "pronunciation": "/ˈstɹʌk.tʃɚ.əl ˈpæt.ɚn ˈmætʃ.ɪŋ/",
        "category": "syntax",
        "signature": "match <subject>:\n    case <pattern> if <guard>: ...",
        "short_summary": "A control flow statement that unpacks, matches, and binds complex data structures based on shape and type.",
        "full_description": "Introduced in Python 3.10 via PEP 634, **structural pattern matching** inspects the structure and types of sequences, mappings, or class instances, matches against patterns, validates optional guard conditions (`if`), and binds variables in a single declarative block.",
        "parameters": [
            {"name": "match", "type": "keyword", "description": "Evaluates the subject expression.", "default": None},
            {"name": "case", "type": "keyword", "description": "Declares pattern to match against subject structure.", "default": None}
        ],
        "returns": {"type": "control flow", "description": "Executes the first matching branch."},
        "added_in_version": "3.10",
        "deprecated_in_version": None,
        "pep_reference": "PEP 634",
        "pep_url": "https://peps.python.org/pep-0634/",
        "gotchas": [
            "`case _:` acts as the default wildcard fallback; placing it before other cases will make them unreachable.",
            "Variable names in patterns bind variables; to match constants, use dotted names like `case Color.RED:`."
        ],
        "cross_language": {
            "Rust": "match subject { Pattern => ... }",
            "Scala": "subject match { case Pattern => ... }",
            "C#": "switch expression with pattern matching"
        },
        "tags": ["syntax", "pattern-matching", "control-flow", "pep-634"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "match val: case ...:",
                "summary": "(syntax) Pattern-based structural destructuring and branching control statement.",
                "parameters": [],
                "returns": {"type": "None", "description": "Executes branch."},
                "example_code": "def parse(cmd):\n    match cmd.split():\n        case ['quit']: return 'Exiting'\n        case ['load', file]: return f'Loading {file}'\n        case _: return 'Unknown'"
            }
        ],
        "version_timeline": [
            {"version": "3.10", "change_type": "introduced", "title": "Structural Pattern Matching", "description": "PEP 634/635/636 introduced match and case statements.", "pep": "PEP 634"}
        ],
        "examples": [
            {
                "title": "Matching Complex Nested Shapes",
                "code": "def process_event(event):\n    match event:\n        case {'type': 'click', 'pos': (x, y)}:\n            return f'Clicked at ({x}, {y})'\n        case {'type': 'keypress', 'key': str(k)} if len(k) == 1:\n            return f'Character pressed: {k}'\n        case _:\n            return 'Ignored event'\n\nprint(process_event({'type': 'click', 'pos': (10, 20)}))\nprint(process_event({'type': 'keypress', 'key': 'A'}))",
                "expected_output": "Clicked at (10, 20)\nCharacter pressed: A",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "extended-unpacking",
        "term": "extended iterable unpacking",
        "part_of_speech": "noun",
        "pronunciation": "/ɪkˈstɛn.dɪd ʌnˈpæk.ɪŋ/",
        "category": "syntax",
        "signature": "first, *rest, last = sequence",
        "short_summary": "The use of the asterisk (*) operator to unpack remaining elements of an iterable into a list during assignment.",
        "full_description": "Introduced in Python 3.0 via PEP 3132, **extended iterable unpacking** generalizes sequence unpacking by allowing a single starred variable `*target` in assignment targets. It absorbs all items between preceding and succeeding mandatory variables into a newly allocated list.",
        "parameters": [
            {"name": "*target", "type": "variable", "description": "Starred variable that collects remaining items as a list.", "default": None}
        ],
        "returns": {"type": "list", "description": "Starred variable is always bound to a list."},
        "added_in_version": "3.0",
        "deprecated_in_version": None,
        "pep_reference": "PEP 3132",
        "pep_url": "https://peps.python.org/pep-3132/",
        "gotchas": [
            "At most one starred expression can appear in an assignment target (`*a, *b = seq` is a SyntaxError).",
            "Extended dictionary unpacking `{**dict1, **dict2}` (PEP 448) was added in Python 3.5."
        ],
        "cross_language": {
            "JavaScript": "const [first, ...rest] = array;",
            "Ruby": "first, *rest = array"
        },
        "tags": ["syntax", "unpacking", "assignment", "pep-3132"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "a, *b, c = seq",
                "summary": "(syntax) Assignment syntax collecting arbitrary intermediate items.",
                "parameters": [],
                "returns": {"type": "list", "description": "Captured sublist."},
                "example_code": "head, *tail = [1, 2, 3, 4]\nprint(head)  # 1\nprint(tail)  # [2, 3, 4]"
            }
        ],
        "version_timeline": [
            {"version": "3.0", "change_type": "introduced", "title": "Extended Iterable Unpacking", "description": "PEP 3132 added *rest assignment syntax.", "pep": "PEP 3132"},
            {"version": "3.5", "change_type": "enhanced", "title": "Additional Unpacking Generalizations", "description": "PEP 448 allowed multiple * and ** unpackings in calls, tuples, lists, and dicts.", "pep": "PEP 448"}
        ],
        "examples": [
            {
                "title": "Head, Middle, and Tail Partitioning",
                "code": "record = ['ID_001', 'Alice', 'Engineer', 2024, 'Active']\nuid, *details, status = record\nprint('UID:', uid)\nprint('Middle details:', details)\nprint('Status:', status)",
                "expected_output": "UID: ID_001\nMiddle details: ['Alice', 'Engineer', 2024]\nStatus: Active",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "copy-shallow-deep",
        "term": "shallow copy vs deep copy",
        "part_of_speech": "noun",
        "pronunciation": "/ˈʃæl.oʊ ˈkɒp.i vɜːr.səs diːp ˈkɒp.i/",
        "category": "concept",
        "signature": "import copy\ncopy.copy(obj) vs copy.deepcopy(obj)",
        "short_summary": "The distinction between duplicating only the outer container (shallow) versus recursively duplicating all nested objects (deep).",
        "full_description": "In Python, assignment statements (`b = a`) bind names to existing objects rather than copying values. The `copy` module provides two distinct copying semantics:\n1. **Shallow copy** (`copy.copy()`): Constructs a new compound object and inserts *references* to child objects.\n2. **Deep copy** (`copy.deepcopy()`): Recursively duplicates every nested object, ensuring complete mutability isolation.",
        "parameters": [
            {"name": "x", "type": "Any", "description": "Object to copy.", "default": None}
        ],
        "returns": {"type": "Any", "description": "Copied compound object."},
        "added_in_version": "1.0",
        "deprecated_in_version": None,
        "pep_reference": None,
        "pep_url": None,
        "gotchas": [
            "Mutating a nested list in a shallow copy unexpectedly mutates the original object's nested list.",
            "`deepcopy` maintains a memo dictionary to handle circular references safely."
        ],
        "cross_language": {
            "JavaScript": "{ ...obj } vs structuredClone(obj)",
            "C++": "Copy constructor vs deep clone"
        },
        "tags": ["concept", "memory", "copy", "deepcopy", "mutability"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "copy.copy(x)",
                "summary": "(memory) A clone of the outer container preserving shared child references.",
                "parameters": [],
                "returns": {"type": "Any", "description": "Shallow duplicated object."},
                "example_code": "import copy\na = [[1, 2], [3, 4]]\nb = copy.copy(a)\nb[0].append(99)\nprint(a[0])  # [1, 2, 99]"
            }
        ],
        "version_timeline": [
            {"version": "1.0", "change_type": "introduced", "title": "copy Module", "description": "Standard copy module included since Python 1.0."}
        ],
        "examples": [
            {
                "title": "Shallow vs Deep Copy Demonstration",
                "code": "import copy\noriginal = {'items': [1, 2, 3]}\nshallow = copy.copy(original)\ndeep = copy.deepcopy(original)\n\nshallow['items'].append(4)\ndeep['items'].append(999)\n\nprint('Original:', original['items'])\nprint('Shallow: ', shallow['items'])\nprint('Deep:    ', deep['items'])",
                "expected_output": "Original: [1, 2, 3, 4]\nShallow:  [1, 2, 3, 4]\nDeep:     [1, 2, 3, 999]",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "currying-partial",
        "term": "partial application & currying",
        "part_of_speech": "noun",
        "pronunciation": "/ˈpɑːr.ʃəl ˌæp.lɪˈkeɪ.ʃən/",
        "category": "concept",
        "signature": "from functools import partial\nbase_func = partial(func, *fixed_args, **fixed_kwargs)",
        "short_summary": "The technique of fixing a subset of a function's arguments to produce a new callable with a simpler signature.",
        "full_description": "**Partial application** binds specific positional or keyword arguments to a function, producing a new `partial` object that can be called with the remaining parameters. Named after logician Haskell Curry, it simplifies callbacks and higher-order function orchestration.",
        "parameters": [
            {"name": "func", "type": "Callable", "description": "The base function.", "default": None},
            {"name": "*args", "type": "Any", "description": "Pre-filled positional arguments.", "default": None}
        ],
        "returns": {"type": "functools.partial", "description": "Partially applied callable object."},
        "added_in_version": "2.5",
        "deprecated_in_version": None,
        "pep_reference": "PEP 309",
        "pep_url": "https://peps.python.org/pep-0309/",
        "gotchas": [
            "Positional arguments are prepended to new arguments, while keyword arguments are merged/overwritten."
        ],
        "cross_language": {
            "Haskell": "Implicit currying for all functions",
            "JavaScript": "fn.bind(null, arg1)"
        },
        "tags": ["concept", "functional", "partial", "currying", "functools"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "noun",
                "signature": "partial(f, x)",
                "summary": "(functional) Pre-binding arguments of a function to generate specialized callables.",
                "parameters": [],
                "returns": {"type": "Callable", "description": "Specialized function."},
                "example_code": "from functools import partial\nbinary_to_int = partial(int, base=2)\nprint(binary_to_int('1010'))  # 10"
            }
        ],
        "version_timeline": [
            {"version": "2.5", "change_type": "introduced", "title": "functools.partial", "description": "PEP 309 introduced partial function application.", "pep": "PEP 309"}
        ],
        "examples": [
            {
                "title": "Creating Specialized Power Functions",
                "code": "from functools import partial\n\ndef power(base, exponent):\n    return base ** exponent\n\nsquare = partial(power, exponent=2)\ncube = partial(power, exponent=3)\n\nprint('5 squared:', square(5))\nprint('5 cubed:  ', cube(5))",
                "expected_output": "5 squared: 25\n5 cubed:   125",
                "is_interactive": True
            }
        ]
    }
]

def seed_techniques():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    inserted_count = 0
    updated_count = 0

    for t in TECHNIQUES:
        cursor.execute("SELECT id FROM entries WHERE slug = ?", (t["slug"],))
        existing = cursor.fetchone()

        params_json = json.dumps(t.get("parameters", []))
        returns_json = json.dumps(t.get("returns", {}))
        gotchas_json = json.dumps(t.get("gotchas", []))
        cross_lang_json = json.dumps(t.get("cross_language", {}))
        tags_json = json.dumps(t.get("tags", []))
        senses_json = json.dumps(t.get("senses", []))
        timeline_json = json.dumps(t.get("version_timeline", []))

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
            updated_count += 1
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
            inserted_count += 1

        # Seed examples
        cursor.execute("DELETE FROM code_examples WHERE entry_slug = ?", (t["slug"],))
        for ex in t.get("examples", []):
            cursor.execute("""
                INSERT INTO code_examples (entry_slug, title, code, expected_output, is_interactive)
                VALUES (?, ?, ?, ?, ?)
            """, (t["slug"], ex["title"], ex["code"], ex.get("expected_output"), ex.get("is_interactive", 1)))

    conn.commit()
    conn.close()
    print(f"Techniques seeded: {inserted_count} inserted, {updated_count} updated.")

    # Export complete database to mobile offlineData.json
    export_mobile_offline()

def export_mobile_offline():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    rows = cursor.execute("SELECT * FROM entries ORDER BY term ASC").fetchall()
    all_entries = []

    for r in rows:
        item = dict(r)
        # Parse JSON fields
        for field in ["parameters", "returns", "gotchas", "cross_language", "tags", "senses", "version_timeline"]:
            if item.get(field):
                try:
                    item[field] = json.loads(item[field])
                except Exception:
                    pass

        # Attach examples
        ex_rows = cursor.execute("SELECT title, code, expected_output, is_interactive FROM code_examples WHERE entry_slug = ?", (item["slug"],)).fetchall()
        item["examples"] = [dict(e) for e in ex_rows]
        all_entries.append(item)

    conn.close()

    offline_path = Path("/home/olaewevictor01/PY DICT/mobile/src/services/offlineData.json")
    if offline_path.parent.exists():
        with open(offline_path, "w") as f:
            json.dump(all_entries, f, indent=2)
        print(f"Updated mobile offlineData.json: {len(all_entries)} total entries bundled.")
    else:
        print("Mobile directory not present, skipping mobile offline bundle.")

if __name__ == "__main__":
    seed_techniques()
