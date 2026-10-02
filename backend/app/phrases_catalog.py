"""
PyDict — Python Idioms, Phrases & Cliches Catalog
Contains encyclopedic explanations, origins, plain-English breakdowns, and runnable code
for iconic Python idioms, cultural aphorisms, design philosophies, and community cliches.
"""

PHRASES_CATALOG = [
    {
        "slug": "eafp",
        "term": "EAFP (Easier to ask for forgiveness than permission)",
        "part_of_speech": "Idiom / Design Philosophy",
        "pronunciation": "/iː.eɪ.ɛf.piː/",
        "signature": "try: obj.action() except ExpectedError: fallback()",
        "short_summary": "Pythonic design style: assume valid keys, attributes, or states and catch exceptions rather than testing prerequisites upfront.",
        "simple_definition": "**EAFP** stands for *'Easier to ask for forgiveness than permission'*. In Python, this means you assume an operation will succeed and use a `try...except` block to catch failures if it doesn't, rather than cluttering your code with numerous preemptive `if` checks. It is faster on the happy path, cleaner to read, and avoids race conditions (TOCTOU).",
        "full_description": """**EAFP** is one of the most celebrated aphorisms in Python culture. Originally coined by computer programming pioneer Grace Hopper, it was adopted by Guido van Rossum and the Python community as a central design principle.

### Why Python Favors EAFP over LBYL
1. **Speed on the Happy Path**: In Python, entering a `try` block has virtually zero runtime overhead in Python 3.11+ (zero-cost exception tables). Preemptive `if` checks incur runtime performance costs on every single execution.
2. **Eliminates Race Conditions (TOCTOU)**: In file systems and multi-threaded applications, checking `if file.exists(): open(file)` creates a 'Time of Check to Time of Use' gap where the file might be deleted between the check and the open. EAFP performs the operation atomically.
3. **Duck Typing Harmony**: EAFP works seamlessly with duck typing: you simply call the method you need without asking for permission or checking object types.""",
        "title": "Real-world: EAFP vs LBYL in API Payload Parsing",
        "code": """# Real-world: Extracting optional user profile fields
user_payload = {"id": 849, "name": "Maya", "tier": "gold"}

# 1. The EAFP Way (Idiomatic Python):
try:
    discount_rate = 0.20 if user_payload["tier"] == "gold" else 0.05
except KeyError:
    discount_rate = 0.0  # Forgiveness granted; default applied

print(f"EAFP Discount: {discount_rate:.0%}")

# 2. File handling: Atomic EAFP vs Fragile LBYL
# Fragile LBYL: if os.path.exists('data.json'): with open('data.json')...
# Robust EAFP:
try:
    with open("config_override.json", "r", encoding="utf-8") as f:
        data = f.read()
except FileNotFoundError:
    data = "{}"  # Safe fallback without race condition

print("Config loaded safely via EAFP.")""",
        "gotchas": [
            "Never use bare `except:` or `except Exception:` with EAFP; catch ONLY the specific expected error (e.g. `except (KeyError, AttributeError):`).",
            "Keep the code inside the `try` block as small as possible so you don't accidentally catch unexpected exceptions from elsewhere."
        ],
        "tags": ["eafp", "idiom", "philosophy", "try-except", "style", "pythonic"]
    },

    {
        "slug": "lbyl",
        "term": "LBYL (Look before you leap)",
        "part_of_speech": "Programming Paradigm",
        "pronunciation": "/ɛl.biː.waɪ.ɛl/",
        "signature": "if condition_is_met: do_action() else: fallback()",
        "short_summary": "Coding style that explicitly tests for pre-conditions before making calls or lookups; the opposite of EAFP.",
        "simple_definition": "**LBYL** stands for *'Look before you leap'*. In this programming style, you explicitly test whether an attribute, key, file, or condition exists (using `if key in dict`, `if hasattr(obj, 'x')`, or `if os.path.exists()`) before attempting to use it. While common in C, C++, and Java, it is often considered unpythonic when overused.",
        "full_description": """**LBYL** is the classical defensive programming approach. While useful for validating user inputs at application boundaries (like form submissions or CLI parameters), relying on LBYL throughout internal Python code creates duplicate lookups, verbose code, and concurrency vulnerabilities.

### The Downside of LBYL in Python
- **Double Lookups**: Writing `if 'key' in my_dict: val = my_dict['key']` hashes the key and scans the hash table *twice*.
- **Race Conditions**: In multi-threaded programs or file I/O, the state can change between the 'check' and the 'action'.""",
        "title": "Real-world: LBYL Input Boundary Validation",
        "code": """# Real-world: Where LBYL IS appropriate — validating external boundary inputs
def register_user(raw_data):
    # LBYL is ideal for validating user-supplied web forms:
    required_keys = ["username", "email", "age"]
    missing = [k for k in required_keys if k not in raw_data]
    
    if missing:
        return f"Validation error: Missing required fields: {missing}"
    
    if not isinstance(raw_data["age"], int) or raw_data["age"] < 13:
        return "Validation error: User must be at least 13 years old."
    
    return f"User '{raw_data['username']}' registered successfully!"

payload = {"username": "alex_dev", "email": "alex@corp.com", "age": 22}
print(register_user(payload))""",
        "gotchas": [
            "Avoid writing `if 'key' in d: return d['key']`; use `d.get('key', default)` instead.",
            "In file systems, LBYL checks (`os.path.exists()`) are prone to race conditions if another process modifies the file."
        ],
        "tags": ["lbyl", "idiom", "validation", "defensive", "style"]
    },

    {
        "slug": "duck-typing",
        "term": "Duck Typing",
        "part_of_speech": "Type System Paradigm",
        "pronunciation": "/dʌk ˈtaɪ.pɪŋ/",
        "signature": "def process(duck): duck.quack(); duck.walk()",
        "short_summary": "Type checking philosophy: 'If it walks like a duck and quacks like a duck, it's a duck.' Focus on behavior over explicit class inheritance.",
        "simple_definition": "**Duck Typing** is Python's dynamic typing philosophy. Rather than checking an object's explicit class inheritance (`isinstance(obj, ExpectedClass)`), Python checks whether the object has the required methods and properties at runtime. If an object implements `.read()`, Python treats it as a file, regardless of whether it inherits from `io.IOBase`.",
        "full_description": """The term originates from the philosophical phrase popularized by James Whitcomb Riley: *'When I see a bird that walks like a duck and swims like a duck and quacks like a duck, I call that bird a duck.'*

In Python, duck typing enables extraordinary flexibility and composability. You do not need rigid interface declarations or complex inheritance trees. Any object that adheres to the expected protocol (such as iterables implementing `__iter__` or context managers implementing `__enter__` and `__exit__`) is immediately usable.""",
        "title": "Real-world: Duck Typing in Document Exporters",
        "code": """# Real-world: A reporter that accepts ANY stream-like object with a write() method
class CloudLogger:
    def write(self, message):
        print(f"[CLOUD LOG]: {message.strip()}")

class ConsoleWriter:
    def write(self, message):
        print(f"[CONSOLE]: {message.strip()}")

def export_audit_log(target_stream, event_name):
    # Duck typing: we don't care about class hierarchies, only that target_stream has .write()
    target_stream.write(f"AUDIT_EVENT: {event_name} timestamp=2026-10-02")

# Both completely unrelated classes work seamlessly:
export_audit_log(CloudLogger(), "UserLoginSuccess")
export_audit_log(ConsoleWriter(), "PaymentCaptured")""",
        "gotchas": [
            "Avoid checking `type(x) is list` or `isinstance(x, list)`; if you need a sequence, accept anything iterable.",
            "Use Python's `collections.abc` (like `Iterable`, `Mapping`, `Sequence`) if you need structural type checking."
        ],
        "tags": ["duck-typing", "oop", "types", "polymorphism", "pythonic"]
    },

    {
        "slug": "pythonic",
        "term": "Pythonic",
        "part_of_speech": "Adjective / Cultural Phrase",
        "pronunciation": "/paɪˈθɒn.ɪk/",
        "signature": "# Idiomatic Python embracing language features and PEP 8 readability",
        "short_summary": "Code that follows the idiomatic conventions, philosophy, and clean readability standards of the Python community.",
        "simple_definition": "**Pythonic** describes code that embraces Python's unique design principles, built-in features, and idioms rather than blindly copying coding patterns from other languages like C, Java, or JavaScript. Pythonic code is typically concise, highly readable, leverages context managers (`with`), list comprehensions, built-ins, and adheres to PEP 8.",
        "full_description": """When Python developers say a piece of code is 'Pythonic', they mean it feels natural, elegant, and expressive in Python.

### Characteristics of Pythonic Code
- Iterating directly over items (`for item in items:`) instead of counting indices (`for i in range(len(items)):`).
- Using context managers (`with open(...)`) instead of manual `.close()` calls.
- Using list/dict comprehensions instead of imperative accumulator loops.
- Using `@property` decorators instead of explicit `get_x()` and `set_x()` methods.
- Using f-strings (`f"{val}"`) instead of string concatenation (`str(val) + "..."`).""",
        "title": "Real-world: Unpythonic vs Pythonic Side-by-Side",
        "code": """# Comparing Unpythonic (C/Java style) vs Pythonic code

names = ["Alice", "Bob", "Charlie"]

# --- UNPYTHONIC ---
i = 0
while i < len(names):
    print("Unpythonic count:", str(i) + ": " + names[i])
    i += 1

# --- PYTHONIC ---
for index, name in enumerate(names, start=1):
    print(f"Pythonic count: {index}: {name}")

# Pythonic tuple unpacking & dictionary swapping
a, b = 10, 20
a, b = b, a  # Swaps variables without a temp variable!
print(f"Swapped: a={a}, b={b}")""",
        "gotchas": [
            "Being 'clever' or creating dense, unreadable 100-character one-liners is NOT Pythonic; readability always comes first.",
            "Pythonic code favors clarity over dogmatic brevity."
        ],
        "tags": ["pythonic", "idiom", "pep8", "style", "best-practices"]
    },

    {
        "slug": "unpythonic",
        "term": "Unpythonic",
        "part_of_speech": "Adjective / Cliche",
        "pronunciation": "/ʌn.paɪˈθɒn.ɪk/",
        "signature": "# Code that works but fights Python's natural design paradigms",
        "short_summary": "Code that functions correctly but violates Python conventions, idioms, or readability standards.",
        "simple_definition": "**Unpythonic** refers to Python code that is written as if it were translated directly from Java, C++, or PHP. Examples include creating Java-style getter and setter methods everywhere, manually managing loop indices with `range(len(...))`, using bare `except: pass`, or ignoring standard libraries.",
        "full_description": """Unpythonic code is not necessarily buggy or non-functional; rather, it ignores the language's native strengths, resulting in verbose, clumsy, and difficult-to-maintain codebases.

### Hallmarks of Unpythonic Code
1. `for i in range(len(lst)): print(lst[i])` (use `for item in lst:` or `enumerate`).
2. `def get_value(self): return self._val` (use `@property`).
3. `f = open('x'); content = f.read(); f.close()` (use `with open('x') as f:`).
4. `try: ... except: pass` (swallowing all exceptions blindly).""",
        "title": "Real-world: Refactoring Unpythonic Patterns",
        "code": """# Refactoring an Unpythonic accumulator loop
records = [{"status": "paid", "amount": 100}, {"status": "pending", "amount": 50}, {"status": "paid", "amount": 250}]

# UNPYTHONIC:
paid_total = 0
for i in range(len(records)):
    if records[i]["status"] == "paid":
        paid_total = paid_total + records[i]["amount"]

# PYTHONIC:
total = sum(r["amount"] for r in records if r["status"] == "paid")

print("Paid Total (Refactored):", total)""",
        "gotchas": [
            "Don't shame other developers for writing unpythonic code; use it as a learning opportunity to introduce Python's cleaner idioms."
        ],
        "tags": ["unpythonic", "antipattern", "style", "refactoring"]
    },

    {
        "slug": "zen-of-python",
        "term": "The Zen of Python (PEP 20)",
        "part_of_speech": "Guiding Aphorisms / Easter Egg",
        "pronunciation": "/zɛn əv ˈpaɪ.θɒn/",
        "signature": "import this",
        "short_summary": "The 19 guiding design principles written by Tim Peters that define the philosophy and soul of the Python language.",
        "simple_definition": "**The Zen of Python** (formalized as PEP 20) is a collection of 19 aphorisms written in 1999 by long-time Python contributor Tim Peters. It serves as both the guiding philosophy for Python's language designers and a famous built-in Easter egg invoked by typing `import this` in any Python terminal.",
        "full_description": """Written by Tim Peters, the Zen of Python articulates the core aesthetic and design philosophy of Python. When design decisions or PEP proposals are debated, community members frequently cite lines from the Zen of Python to justify language choices.

### The 19 Lines of the Zen of Python
1. Beautiful is better than ugly.
2. Explicit is better than implicit.
3. Simple is better than complex.
4. Complex is better than complicated.
5. Flat is better than nested.
6. Sparse is better than dense.
7. Readability counts.
8. Special cases aren't special enough to break the rules.
9. Although practicality beats purity.
10. Errors should never pass silently.
11. Unless explicitly silenced.
12. In the face of ambiguity, refuse the temptation to guess.
13. There should be one-- and preferably only one --obvious way to do it.
14. Although that way may not be obvious at first unless you're Dutch.
15. Now is better than never.
16. Although never is often better than *right* now.
17. If the implementation is hard to explain, it's a bad idea.
18. If the implementation is easy to explain, it may be a good idea.
19. Namespaces are one honking great idea -- let's do more of those!""",
        "title": "Real-world: Exploring The Zen of Python in Code",
        "code": """# Invoking Python's built-in philosophical Easter egg
import this

# The source code of 'this.py' in the standard library is actually ROT13 encoded,
# playfully demonstrating that even the Easter egg honors namespaces!
print("\\nTip: Type 'import this' in any Python REPL to reflect on code design.")""",
        "gotchas": [
            "Lines 9 and 8 intentionally acknowledge balance: 'Special cases aren't special enough to break the rules. Although practicality beats purity.'",
            "Line 14 ('unless you're Dutch') is a humorous reference to Python's creator, Guido van Rossum, who is from the Netherlands."
        ],
        "tags": ["zen-of-python", "pep20", "philosophy", "easter-egg", "tim-peters"]
    },

    {
        "slug": "explicit-is-better-than-implicit",
        "term": "Explicit is better than implicit",
        "part_of_speech": "Aphorism / Guiding Principle",
        "pronunciation": "/ɪkˈsplɪs.ɪt ɪz ˈbɛt.ər ðæn ɪmˈplɪs.ɪt/",
        "signature": "from module import function_name  # Explicit import",
        "short_summary": "Core Python principle: code should clearly reveal its intentions, arguments, and bindings rather than hiding them behind implicit magic.",
        "simple_definition": "**'Explicit is better than implicit'** is the second aphorism of the Zen of Python. It states that code should openly declare what it is doing rather than relying on hidden assumptions, magic global variables, or implicit dependencies. A prominent example is requiring `self` as an explicit first parameter in class methods.",
        "full_description": """In many programming languages, methods implicitly know about the current object (e.g. `this` in Java or C++). Python deliberately requires `self` to be written explicitly in method signatures so that it is always clear where a variable is scoped.

Another major manifestation is module imports: Python discourages wildcard imports (`from math import *`) because they implicitly inject hundreds of names into the local namespace, making it impossible to know where a function came from.""",
        "title": "Real-world: Explicit Namespaces vs Implicit Wildcards",
        "code": """# IMPLICIT (Unpythonic & Dangerous):
# from math import *  <-- Where did pow, log, or sin come from? What did it overwrite?

# EXPLICIT (Pythonic & Clean):
import math
from datetime import datetime, timezone

# Clearly declared source of functions
radius = 5.0
area = math.pi * (radius ** 2)
current_time = datetime.now(timezone.utc)

print(f"Area: {area:.2f} | Generated at: {current_time.isoformat()}")""",
        "gotchas": [
            "Never use `from module import *` in production code; it pollutes the namespace and breaks IDE autocompletion.",
            "Explicit `self` in Python classes is intentional design, not an oversight."
        ],
        "tags": ["explicit", "philosophy", "zen", "imports", "self"]
    },

    {
        "slug": "batteries-included",
        "term": "Batteries Included",
        "part_of_speech": "Philosophy / Phrase",
        "pronunciation": "/ˈbæt.ər.iz ɪnˈkluː.dɪd/",
        "signature": "import sqlite3, json, csv, urllib.request, math, hashlib, asyncio",
        "short_summary": "Python's design motto describing its vast, production-ready standard library included with every installation.",
        "simple_definition": "**'Batteries Included'** is Python's longstanding design philosophy meaning that the core Python installation comes out-of-the-box with a rich, robust standard library capable of performing almost any common programming task—from parsing JSON and managing SQLite databases to running HTTP servers and hashing passwords—without needing third-party packages.",
        "full_description": """Coined in Python's early days, 'Batteries Included' is one of the primary reasons Python became the dominant language for scripting, system administration, data science, and web development.

A fresh installation of Python allows you to immediately:
- Read and write SQLite databases (`sqlite3`)
- Spin up an instant HTTP file server (`python -m http.server`)
- Parse JSON, CSV, XML, and INI configuration files
- Perform cryptographic hashing (`hashlib`, `hmac`)
- Execute parallel threads and processes (`threading`, `multiprocessing`, `concurrent.futures`)
- Run asynchronous network loops (`asyncio`)""",
        "title": "Real-world: Instant SQLite & JSON Database with Zero Installs",
        "code": """# Real-world: Complete database application using ONLY built-in batteries!
import sqlite3
import json

# 1. In-memory SQLite database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, profile TEXT)")

# 2. Native JSON storage and retrieval
user_data = {"name": "Jordan", "role": "admin", "skills": ["Python", "SQL"]}
cursor.execute("INSERT INTO users (profile) VALUES (?)", (json.dumps(user_data),))

cursor.execute("SELECT profile FROM users WHERE id = 1")
retrieved_json = cursor.fetchone()[0]
user = json.loads(retrieved_json)

print(f"Loaded '{user['name']}' with role '{user['role']}' using 100% standard library!")
conn.close()""",
        "gotchas": [
            "While batteries are included, specialized domains (like deep learning with PyTorch or web frameworks like FastAPI) still benefit from PyPI packages."
        ],
        "tags": ["batteries-included", "stdlib", "philosophy", "sqlite", "json"]
    },

    {
        "slug": "errors-should-never-pass-silently",
        "term": "Errors should never pass silently",
        "part_of_speech": "Aphorism / Best Practice",
        "pronunciation": "/ˈɛr.ərz ʃʊd ˈnɛv.ər pæs ˈsaɪ.lənt.li/",
        "signature": "# Unless explicitly silenced: avoid bare except: pass",
        "short_summary": "Crucial principle from the Zen of Python forbidding the silent suppression of unexpected errors.",
        "simple_definition": "**'Errors should never pass silently (Unless explicitly silenced)'** warns against the dangerous practice of writing `try: ... except: pass`. Catching all exceptions without handling or logging them hides critical bugs, causes silent data corruption, and prevents programs from failing fast.",
        "full_description": """In poorly written code, developers sometimes wrap troublesome sections in `except Exception: pass` to make crashes disappear. This anti-pattern creates 'silent failures' where functions produce invalid data without warning, leading to hours of painful debugging later.

If an error must genuinely be ignored (for instance, cleaning up a temporary file that may or may not exist), silence it **explicitly** using `contextlib.suppress(FileNotFoundError)`.""",
        "title": "Real-world: Safe Explicit Silencing with contextlib.suppress",
        "code": """from contextlib import suppress
import os

# BAD (Blind silent suppression):
# try:
#     os.remove("temp.txt")
# except Exception:  # Catches KeyboardInterrupt, permissions, disk errors silently!
#     pass

# GOOD (Explicitly silencing ONLY expected FileNotFoundError):
with suppress(FileNotFoundError):
    os.remove("non_existent_cache.tmp")

print("Explicitly silenced FileNotFoundError without hiding other bugs.")""",
        "gotchas": [
            "Never use bare `except:` — it catches `KeyboardInterrupt` and `SystemExit`, making your script unkillable with Ctrl+C.",
            "Use `contextlib.suppress(SpecificError)` to explicitly silence known safe exceptions."
        ],
        "tags": ["errors", "zen", "exceptions", "best-practices", "suppress"]
    },

    {
        "slug": "one-obvious-way",
        "term": "There should be one obvious way to do it",
        "part_of_speech": "Aphorism / Design Philosophy",
        "pronunciation": "/ðɛər ʃʊd biː wʌn ˈɒb.vi.əs weɪ/",
        "signature": "# Strive for a single canonical, readable idiom",
        "short_summary": "Python's design philosophy contrasting with Perl's 'There's more than one way to do it' (TMTOWTDI).",
        "simple_definition": "**'There should be one-- and preferably only one --obvious way to do it'** is Tim Peters's famous counter-philosophy to Perl's motto *'There's more than one way to do it' (TMTOWTDI)*. It advocates that a programming language should have one clear, canonical, and readable idiom for any given task, making code predictable across teams.",
        "full_description": """In languages like Perl or Ruby, designers intentionally added multiple syntax variants for the same operation. While flexible, this meant two developers could write the same program in completely unrecognizable styles.

Python deliberately limits redundant syntax. For example, instead of having multiple looping constructs like `until`, `loop`, `foreach`, Python provides a single, powerful `for ... in` loop.""",
        "title": "Real-world: The One Obvious Way in Python",
        "code": """# In Python, string formatting evolved to one obvious, preferred way: f-strings!

name = "Sam"
score = 98.5

# Older approaches:
# "%s scored %.1f" % (name, score)  # C-style
# "{} scored {:.1f}".format(name, score)  # str.format()

# The one obvious, modern Pythonic way:
result = f"{name} scored {score:.1f}%"
print(result)""",
        "gotchas": [
            "As Python has grown over 30 years, occasional overlaps occur (e.g. `f-strings` vs `format()`), but PEPs regularly establish clear best-practice standards."
        ],
        "tags": ["philosophy", "zen", "perl", "canonical", "design"]
    },

    {
        "slug": "flat-is-better-than-nested",
        "term": "Flat is better than nested",
        "part_of_speech": "Aphorism / Style Principle",
        "pronunciation": "/flæt ɪz ˈbɛt.ər ðæn ˈnɛs.tɪd/",
        "signature": "# Guard clauses & early returns to eliminate deep indentation pyramids",
        "short_summary": "Style rule advising developers to avoid deeply nested if-statements and indentation pyramids.",
        "simple_definition": "**'Flat is better than nested'** is the fifth line of the Zen of Python. It advises developers to eliminate deeply nested code (the dreaded 'arrowhead' or 'pyramid of doom') by using guard clauses, early returns, and generator expressions, keeping indentation levels shallow and legible.",
        "full_description": """Deeply nested code increases cognitive load because the reader must hold multiple conditions in their head simultaneously. By checking invalid states first and returning immediately (guard clauses), the main execution path stays flat at the outer indentation level.""",
        "title": "Real-world: Refactoring Nested Logic into Flat Guard Clauses",
        "code": """# NESTED (Hard to read):
def process_order_nested(order):
    if order is not None:
        if order.get("paid"):
            if order.get("items"):
                return f"Shipping {len(order['items'])} items!"
            else:
                return "Order has no items."
        else:
            return "Order is unpaid."
    return "Invalid order."

# FLAT (Pythonic guard clauses):
def process_order_flat(order):
    if not order:
        return "Invalid order."
    if not order.get("paid"):
        return "Order is unpaid."
    if not order.get("items"):
        return "Order has no items."
    
    # Happy path is flat and easy to follow:
    return f"Shipping {len(order['items'])} items!"

sample = {"paid": True, "items": ["Laptop", "Mouse"]}
print(process_order_flat(sample))""",
        "gotchas": [
            "If your code indents more than 3 or 4 levels deep, it is almost always a candidate for refactoring."
        ],
        "tags": ["flat", "nesting", "zen", "refactoring", "clean-code"]
    },

    {
        "slug": "readability-counts",
        "term": "Readability counts",
        "part_of_speech": "Aphorism / Core Principle",
        "pronunciation": "/ˌriː.dəˈbɪl.ə.ti kaʊnts/",
        "signature": "# Clear, self-documenting code over clever, compressed obfuscation",
        "short_summary": "Python's foundational design rule: programs are read far more often than they are written.",
        "simple_definition": "**'Readability counts'** is the core axiom of Python. Popularized by Guido van Rossum, it highlights that code is read and maintained dozens of times more frequently than it is initially typed. Code should read almost like structured English, using clear variable names and obvious constructs rather than clever one-line tricks.",
        "full_description": """Many languages celebrate brevity or cryptic terseness. Python explicitly rejects this, prioritizing the human reader over the machine compiler. Python's mandatory whitespace indentation, plain-English keywords (`and`, `or`, `not` instead of `&&`, `||`, `!`), and descriptive naming conventions all derive from this principle.""",
        "title": "Real-world: Self-Documenting Readable Code",
        "code": """# Clever but unreadable (Cleverness for its own sake):
# res = [(x, y) for x in range(10) for y in range(10) if (x+y)%2==0 and x*y>15]

# Readable and self-documenting:
def is_valid_coordinate(x, y):
    is_even_sum = (x + y) % 2 == 0
    has_large_product = (x * y) > 15
    return is_even_sum and has_large_product

valid_pairs = [
    (x, y) 
    for x in range(10) 
    for y in range(10) 
    if is_valid_coordinate(x, y)
]

print(f"Found {len(valid_pairs)} valid coordinates.")""",
        "gotchas": [
            "Never sacrifice readability to reduce line count.",
            "Write code for the developer who will maintain it six months from now—which is often future you!"
        ],
        "tags": ["readability", "zen", "philosophy", "clean-code"]
    },

    {
        "slug": "bdfl",
        "term": "BDFL (Benevolent Dictator For Life)",
        "part_of_speech": "Community Title / Phrase",
        "pronunciation": "/biː.diː.ɛf.ɛl/",
        "signature": "Guido van Rossum (1991 - 2018) -> Steering Council (PEP 13)",
        "short_summary": "Historical title given to Python creator Guido van Rossum; language governance is now handled by an elected Steering Council.",
        "simple_definition": "**BDFL** (*Benevolent Dictator For Life*) was the affectionate title given to Guido van Rossum, the creator of Python. As BDFL, Guido held the ultimate decision-making authority on Python Enhancement Proposals (PEPs) and the language's syntax until his retirement from the role in July 2018. Python is now governed by an elected five-member Steering Council (PEP 13).",
        "full_description": """The term 'Benevolent Dictator For Life' was coined in 1995 when Guido joined the Corporation for National Research Initiatives. It reflected open-source governance where a single trusted founder guides a language's artistic vision and consistency.

In July 2018, following contentious debates over PEP 572 (the assignment expression `:=`), Guido stepped down as BDFL. The community voted on PEP 13, establishing a formal annual election of a 5-member Steering Council to oversee language evolution.""",
        "title": "Real-world: Inspecting Python Implementation & Governance",
        "code": """import sys
import platform

print("Python Version:", platform.python_version())
print("Compiler:", platform.python_compiler())
print("CPython Implementation:", platform.python_implementation())
print("Governance: Elected Steering Council (PEP 13)")""",
        "gotchas": [
            "Guido is no longer BDFL, but remains an active and revered contributor to the Python ecosystem."
        ],
        "tags": ["bdfl", "guido-van-rossum", "governance", "history", "community"]
    },

    {
        "slug": "gil",
        "term": "GIL (Global Interpreter Lock)",
        "part_of_speech": "Architecture Cliche / Acronym",
        "pronunciation": "/ɡɪl/",
        "signature": "# sys._is_gil_enabled() in free-threaded Python 3.13+",
        "short_summary": "CPython's internal mutex ensuring only one native thread executes Python bytecode at once; free-threading introduced in Python 3.13 (PEP 703).",
        "simple_definition": "**The GIL** (*Global Interpreter Lock*) is a mutex mechanism in CPython (the standard Python interpreter) that prevents multiple OS threads from executing Python bytecodes concurrently. It simplifies memory management and C extension integration, but means CPU-bound Python multithreading runs on a single core. In Python 3.13+ (PEP 703), free-threaded Python allows running without the GIL!",
        "full_description": """For CPU-bound tasks in standard CPython, multiple threads do not increase execution speed because the GIL serializes bytecode execution. For I/O-bound tasks (network requests, database queries, file reading), the GIL is released, allowing threads to achieve high concurrency.

### Workarounds and Future
1. **Multiprocessing**: Use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor` to spawn separate processes with their own GIL and memory space.
2. **Asyncio**: Cooperative single-threaded multitasking for I/O operations.
3. **PEP 703 (Python 3.13+)**: Free-threaded CPython build (`python3.13t`) that can run multi-threaded CPU workloads across all CPU cores without a GIL!""",
        "title": "Real-world: CPU-bound Parallelism via ProcessPoolExecutor (Bypassing GIL)",
        "code": """from concurrent.futures import ProcessPoolExecutor
import math

def compute_heavy_factors(n):
    # CPU-bound calculation
    return sum(math.isqrt(i) for i in range(1, n))

# When running CPU-bound jobs, use ProcessPoolExecutor to bypass the GIL:
if __name__ == "__main__":
    numbers = [50000, 60000, 70000]
    # Spawns separate processes, each utilizing 100% of an independent CPU core!
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(compute_heavy_factors, numbers))
    print("Computed parallel results across CPU cores:", results)""",
        "gotchas": [
            "The GIL does NOT make Python code thread-safe! Shared state across threads still requires `threading.Lock`.",
            "I/O-bound threading (downloading websites, querying databases) works great with standard threads because the GIL is released during I/O."
        ],
        "tags": ["gil", "threads", "concurrency", "cpython", "multiprocessing"]
    },

    {
        "slug": "walrus-operator",
        "term": "Walrus Operator (:=)",
        "part_of_speech": "Syntax Nickname / Operator",
        "pronunciation": "/ˈwɔːl.rəs ˈɒp.ə.reɪ.tər/",
        "signature": "name := expression",
        "short_summary": "Assignment expression operator introduced in Python 3.8 (PEP 572), named after the eyes and tusks of a walrus.",
        "simple_definition": "The **Walrus Operator** (`:=`), officially called an *assignment expression* (PEP 572), allows you to assign a value to a variable *inside* an expression. It was affectionately nicknamed the 'walrus operator' because the symbol `:=` resembles the sideways eyes and tusks of a walrus.",
        "full_description": """Introduced in Python 3.8 after extensive debate, assignment expressions allow developers to calculate a value, assign it to a variable name, and test it in a single concise line.

Common use cases include:
- Processing chunks of data in a `while` loop until empty.
- Filtering and transforming elements in list comprehensions without recalculating expensive functions.
- Regex pattern matching in conditional blocks.""",
        "title": "Real-world: Stream Processing & List Filtering with Walrus :=",
        "code": """# Real-world: Reading batches until empty without repeating code
stream_data = ["chunk_1", "chunk_2", "chunk_3", ""]

def fetch_chunk():
    return stream_data.pop(0) if stream_data else ""

# 1. Walrus in a while loop
# Assigns chunk and checks if non-empty in one step:
while (chunk := fetch_chunk()):
    print(f"Processing {chunk}")

# 2. Walrus in list comprehension (avoids calculating expensive function twice!)
raw_entries = ["  admin  ", "  ", "guest", "editor"]
cleaned = [clean for entry in raw_entries if (clean := entry.strip())]
print("Cleaned non-empty entries:", cleaned)""",
        "gotchas": [
            "Do not overuse the walrus operator where regular assignment is clearer.",
            "Assignment expressions do not create a new scope; the variable remains accessible in the outer scope."
        ],
        "tags": ["walrus", "pep572", "assignment-expression", "syntax", "python3.8"]
    },

    {
        "slug": "dunder",
        "term": "Dunder (Double Underscore)",
        "part_of_speech": "Jargon / Slang",
        "pronunciation": "/ˈdʌn.dər/",
        "signature": "def __init__(self): ... def __str__(self): ...",
        "short_summary": "Slang portmanteau of 'Double Under', referring to Python's special double-underscore methods and attributes.",
        "simple_definition": "**Dunder** is an informal contraction of *'Double Under'*. In Python, it refers to any method, attribute, or variable that begins and ends with double underscores, such as `__init__` ('dunder init'), `__str__` ('dunder str'), or `__len__` ('dunder len'). These are also called *magic methods* or *special methods*.",
        "full_description": """Instead of having to pronounce 'underscore underscore init underscore underscore', Python community members Mark Hammond and Robin Friedrich popularized the shorthand 'dunder init'.

Dunder methods form the backbone of Python's data model. When you write `len(my_obj)`, Python executes `my_obj.__len__()`. When you iterate over `for item in my_obj:`, Python calls `my_obj.__iter__()`.""",
        "title": "Real-world: Building a Custom Vector with Dunder Methods",
        "code": """# Real-world: Custom 2D Vector supporting +, len(), and str() via dunder methods
class Vector2D:
    def __init__(self, x, y):  # dunder init
        self.x = x
        self.y = y

    def __add__(self, other):  # dunder add: enables v1 + v2
        return Vector2D(self.x + other.x, self.y + other.y)

    def __repr__(self):  # dunder repr: clean developer representation
        return f"Vector2D({self.x}, {self.y})"

    def __abs__(self):  # dunder abs: enables abs(v)
        return (self.x ** 2 + self.y ** 2) ** 0.5

v1 = Vector2D(3, 4)
v2 = Vector2D(1, 2)
v3 = v1 + v2

print("Vector Addition:", v3)
print("Vector Magnitude (abs):", abs(v1))""",
        "gotchas": [
            "Never invent your own dunder names (e.g. `__my_custom_method__`); Python reserves all dunder identifiers for future language enhancements.",
            "Single underscore `_name` signifies private/internal by convention; double underscore `__name` inside classes triggers name mangling."
        ],
        "tags": ["dunder", "magic-methods", "oop", "data-model", "slang"]
    },

    {
        "slug": "monkey-patching",
        "term": "Monkey Patching",
        "part_of_speech": "Programming Phrase / Technique",
        "pronunciation": "/ˈmʌŋ.ki ˈpætʃ.ɪŋ/",
        "signature": "TargetClass.method = replacement_function",
        "short_summary": "Dynamically modifying or extending classes or modules at runtime without altering the original source code.",
        "simple_definition": "**Monkey Patching** refers to the dynamic modification of a class, function, or module at runtime. In Python, because classes and modules are mutable first-class objects, you can override attributes or methods dynamically. It is widely used in unit testing (mocking external APIs) and temporary bug hotfixes, but can lead to elusive bugs if overused in production.",
        "full_description": """The term was derived from *guerrilla patch* (changing code sneakily at runtime), which sounded like *gorilla*, and eventually morphed into *monkey patch*.

### Common Uses
- **Unit Testing**: Replacing network calls or database connections with fast mock functions (`unittest.mock.patch`).
- **Compatibility Bridges**: Polyfilling missing features in older library versions.""",
        "title": "Real-world: Safe Mocking via Monkey Patching in Tests",
        "code": """import time

class PaymentService:
    def charge_card(self, amount):
        print(f"Connecting to real bank API... Charging ${amount}")
        time.sleep(0.5)
        return {"status": "success", "charge_id": "ch_987"}

service = PaymentService()

# Monkey-patching the method for fast, offline testing:
def mock_charge_card(amount):
    print(f"[TEST MOCK]: Simulated instant charge of ${amount}")
    return {"status": "success", "charge_id": "test_mock_123"}

# Apply the patch
original_method = service.charge_card
service.charge_card = mock_charge_card

# Test execution runs instantaneously
result = service.charge_card(50)
print("Test Result:", result)

# Restore original method cleanly
service.charge_card = original_method""",
        "gotchas": [
            "Always restore monkey-patched methods after tests finish (or use context managers like `unittest.mock.patch`).",
            "Avoid monkey-patching in production libraries; it creates confusing debugging nightmares for other team members."
        ],
        "tags": ["monkey-patching", "testing", "mocking", "dynamic", "runtime"]
    },

    {
        "slug": "truthy-and-falsy",
        "term": "Truthy and Falsy",
        "part_of_speech": "Type Concept / Jargon",
        "pronunciation": "/ˈtruː.θi ænd ˈfɔːl.si/",
        "signature": "if container:  # Evaluates True if non-empty, False if empty",
        "short_summary": "Pythonic boolean evaluation: values that coerce to True or False in conditional statements.",
        "simple_definition": "**Truthy** and **Falsy** describe how Python values evaluate when coerced to booleans in `if` or `while` statements. In Python, you do not need to write `if len(items) > 0:` or `if name != '':`; non-empty containers and strings are inherently **Truthy**, while empty collections (`[]`, `{}`, `set()`, `""`), zero (`0`, `0.0`), and `None` are **Falsy**.",
        "full_description": """### The Complete List of Standard Falsy Values in Python:
- Constants: `None` and `False`
- Numeric zeros: `0`, `0.0`, `0j`, `Decimal(0)`, `Fraction(0, 1)`
- Empty sequences and collections: `""`, `()`, `[]`, `{}`, `set()`, `range(0)`
- Custom objects defining `__bool__()` returning `False` or `__len__()` returning `0`

**All other objects in Python are Truthy!**""",
        "title": "Real-world: Clean Truthy Checks vs Redundant Comparisons",
        "code": """# Real-world: Idiomatic truthiness checks in application code
pending_tasks = ["email_receipt", "sync_crm"]
user_comment = "   "

# UNPYTHONIC (Redundant comparisons):
if len(pending_tasks) > 0:
    print("Tasks exist (unpythonic check).")

# PYTHONIC (Direct truthiness check):
if pending_tasks:
    print(f"Processing {len(pending_tasks)} pending tasks (pythonic check).")

# Handling whitespace with truthiness:
cleaned_comment = user_comment.strip()
if not cleaned_comment:
    print("Comment rejected: Empty or whitespace-only.")""",
        "gotchas": [
            "Be careful with `0`: `if count:` evaluates to `False` when `count == 0`! If zero is a valid value, check `if count is not None:` explicitly.",
            "Custom classes can customize their truthiness by implementing the `__bool__()` or `__len__()` dunder methods."
        ],
        "tags": ["truthy", "falsy", "boolean", "idiom", "style"]
    },

    {
        "slug": "legb-rule",
        "term": "LEGB Rule (Scope Resolution)",
        "part_of_speech": "Mnemonic / Scope Rule",
        "pronunciation": "/lɛɡ.biː ruːl/",
        "signature": "Local -> Enclosing -> Global -> Built-in",
        "short_summary": "The order in which Python resolves variable names: Local, Enclosing, Global, and Built-in scopes.",
        "simple_definition": "The **LEGB Rule** is a mnemonic for the sequence of four scopes Python searches through when looking up a variable name: **L**ocal (inside the current function), **E**nclosing (in any enclosing nested functions/closures), **G**lobal (the current module's top-level namespace), and **B**uilt-in (Python's built-in namespace like `len` or `range`).",
        "full_description": """When you reference a name `x` in Python:
1. **L (Local)**: Python checks names assigned inside the local function block.
2. **E (Enclosing)**: Python checks outer enclosing function namespaces (lexical closures).
3. **G (Global)**: Python checks the top-level module globals.
4. **B (Built-in)**: Python checks the `builtins` module.
If the name is not found in any of these four scopes, Python raises a `NameError`.""",
        "title": "Real-world: Demonstrating the 4 Scopes of LEGB",
        "code": """# Global scope (G)
scope_var = "I am Global"

def outer_function():
    # Enclosing scope (E)
    scope_var = "I am Enclosing"

    def inner_function():
        # Local scope (L)
        scope_var = "I am Local"
        print("Inner lookup:", scope_var)

    inner_function()
    print("Outer lookup:", scope_var)

outer_function()
print("Module lookup:", scope_var)

# Built-in scope (B): functions like len(), sum(), min()
print("Built-in function lookup:", len([1, 2, 3]))""",
        "gotchas": [
            "Never name your variables `list`, `dict`, `str`, or `id`; doing so shadows the Built-in (B) scope with a Local or Global name.",
            "Use `nonlocal` to rebind an Enclosing variable; use `global` to rebind a Global variable."
        ],
        "tags": ["legb", "scope", "namespaces", "closures", "architecture"]
    },

    {
        "slug": "mro",
        "term": "MRO (Method Resolution Order)",
        "part_of_speech": "OOP Algorithm / Acronym",
        "pronunciation": "/ɛm.ɑːr.oʊ/",
        "signature": "ClassName.mro()  # Returns linearized method search order",
        "short_summary": "The deterministic order in which Python searches for methods and attributes in multiple-inheritance class hierarchies.",
        "simple_definition": "**MRO** stands for *Method Resolution Order*. It is the definitive, linear order Python follows when searching for methods and attributes across complex class inheritance hierarchies, especially when multiple inheritance or the 'Diamond Problem' is involved. Python uses the **C3 Linearization** algorithm to guarantee monotonicity and consistency.",
        "full_description": """Before Python 2.3, Python used depth-first search which caused subtle bugs in multiple inheritance. Starting in Python 2.3, Guido adopted the mathematically rigorous C3 Linearization algorithm.

You can inspect any class's MRO in Python by calling `Class.mro()` or accessing `Class.__mro__`.""",
        "title": "Real-world: Inspecting MRO in Multiple Inheritance & Mixins",
        "code": """# Real-world: Class hierarchy with mixins and cooperative super()
class BaseService:
    def execute(self):
        print("BaseService: executing core workload")

class LoggingMixin(BaseService):
    def execute(self):
        print("[LOG]: Execution started")
        super().execute()
        print("[LOG]: Execution finished")

class MetricsMixin(BaseService):
    def execute(self):
        print("[METRIC]: Timer started")
        super().execute()
        print("[METRIC]: Timer ended")

class PaymentWorker(LoggingMixin, MetricsMixin):
    pass

worker = PaymentWorker()
worker.execute()

print("\\nMethod Resolution Order (MRO):")
for idx, cls in enumerate(PaymentWorker.mro(), start=1):
    print(f"  {idx}. {cls.__name__}")""",
        "gotchas": [
            "Always use `super()` cooperatively in multiple inheritance to ensure all ancestor methods in the MRO execute.",
            "Attempting to create an invalid inheritance hierarchy that violates monotonicity raises `TypeError: Cannot create a consistent method resolution order (MRO)`."
        ],
        "tags": ["mro", "oop", "c3-linearization", "multiple-inheritance", "super"]
    },

    {
        "slug": "spam-and-eggs",
        "term": "Spam and Eggs (Monty Python)",
        "part_of_speech": "Cultural Cliche / Metasyntactic Variable",
        "pronunciation": "/spæm ænd ɛɡz/",
        "signature": "spam = 'eggs'; ham = 'knights_who_say_ni'",
        "short_summary": "Canonical Python metasyntactic placeholder names originating from the Monty Python comedy sketch.",
        "simple_definition": "In standard computer science, documentation commonly uses placeholder names like `foo` and `bar`. In the Python world, canonical examples use **spam**, **eggs**, and **ham**. This is because Python was named after the legendary British comedy troupe **Monty Python**, not the snake! The phrase references their famous 1970 cafe sketch where every menu item contains spam.",
        "full_description": """When Guido van Rossum began implementing Python in December 1989, he wanted a short, unique, and slightly mysterious name. Being a fan of *Monty Python's Flying Circus*, he named the language after the troupe.

Throughout the official Python documentation, tutorial examples, test suites, and standard library tests, you will see `spam`, `eggs`, `ham`, `lumberjack`, and `knights_who_say_ni` used instead of `foo` and `bar`.""",
        "title": "Real-world: Classic Monty Pythonic Example Code",
        "code": """# A classic Monty Python style Python snippet
menu = ["egg and bacon", "egg and spam", "spam, bacon, sausage and spam", "lobster thermidor"]

spam_dishes = [dish for dish in menu if "spam" in dish]
print("Spam-approved dishes:", spam_dishes)

def knights_who_say_ni():
    return "Bring us a shrubbery!"

print("The Knights decree:", knights_who_say_ni())""",
        "gotchas": [
            "In professional enterprise codebases, use meaningful domain variable names (`user_account`, `transaction_id`) rather than `spam` or `foo`."
        ],
        "tags": ["spam", "eggs", "monty-python", "history", "culture", "folklore"]
    },

    {
        "slug": "guidos-time-machine",
        "term": "Guido's Time Machine",
        "part_of_speech": "Community Folklore / Meme",
        "pronunciation": "/ˈɡiː.doʊz taɪm məˈʃiːn/",
        "signature": "# Guido van Rossum already implemented your idea 5 years ago",
        "short_summary": "Playful community folklore stating that whenever someone proposes a clever new Python feature, Guido had already added it years earlier.",
        "simple_definition": "**Guido's Time Machine** is an iconic inside joke in the Python development community. Whenever an excited developer comes up with what they believe is a groundbreaking new language feature or library pattern and posts it on the Python mailing list, veteran core developers would reply that Guido had already implemented it several versions ago using his mythical 'Time Machine'.",
        "full_description": """Coined on the `comp.lang.python` Usenet group in the late 1990s, the joke celebrated Guido van Rossum's uncanny foresight in anticipating programmer needs and designing clean, extensible abstractions before developers even realized they needed them.""",
        "title": "Real-world: Exploring Built-in Foresight in Python",
        "code": """# Example of Python's foresight: built-in extended sequence unpacking
records = ["GET", "/api/v1/users", "HTTP/1.1", 200, 1420]

# Python 3.0 added star unpacking:
method, path, *metadata = records

print(f"Method: {method}")
print(f"Path: {path}")
print(f"Remainder captured automatically: {metadata}")""",
        "gotchas": [
            "Before writing a complex custom utility, check the standard library (`itertools`, `collections`, `functools`)—Guido's Time Machine may have already built it for you!"
        ],
        "tags": ["guido-van-rossum", "time-machine", "folklore", "history", "humor"]
    },

    {
        "slug": "splat-operator",
        "term": "Splat Operator (* and **)",
        "part_of_speech": "Jargon / Slang",
        "pronunciation": "/splæt ˈɒp.ə.reɪ.tər/",
        "signature": "func(*args, **kwargs); merged = {**d1, **d2}",
        "short_summary": "Slang for the asterisk and double-asterisk unpacking operators used for variadic arguments and collection spreading.",
        "simple_definition": "The **Splat Operator** is informal jargon for the asterisk (`*`) and double-asterisk (`**`) unpacking operators in Python. A single asterisk (`*args`) unpacks sequences or tuples into positional arguments, while a double asterisk (`**kwargs`, or 'double splat') unpacks dictionaries into named keyword arguments.",
        "full_description": """Originally borrowed from the typography world (where '*' is sometimes called a splat), the phrase became common in Python, Ruby, and Perl.

In Python:
- `*args`: Collects or unpacks positional arguments.
- `**kwargs`: Collects or unpacks keyword arguments.
- Dictionary merging (Python 3.5+): `merged = {**defaults, **custom_overrides}`.
- Extended iterable unpacking: `first, *middle, last = [1, 2, 3, 4, 5]`.""",
        "title": "Real-world: Function Decorators & Dictionary Merging with Splats",
        "code": """# Real-world: A universal timing decorator using *args and **kwargs
import time

def benchmark(func):
    def wrapper(*args, **kwargs):  # Accepts ANY arguments
        start = time.perf_counter()
        result = func(*args, **kwargs)  # Unpacks them to target function
        duration_ms = (time.perf_counter() - start) * 1000
        print(f"[{func.__name__}] took {duration_ms:.3f}ms")
        return result
    return wrapper

@benchmark
def calculate_metrics(base, multiplier, discount=0.0):
    return (base * multiplier) - discount

print("Result:", calculate_metrics(100, 1.2, discount=10))

# Dictionary merging via double-splat:
config = {**{"theme": "dark", "port": 8000}, **{"port": 9000}}
print("Merged config:", config)""",
        "gotchas": [
            "In Python 3.9+, you can also use the union operator `|` to merge dictionaries (`d1 | d2`).",
            "`*args` produces a `tuple`; `**kwargs` produces a `dict`."
        ],
        "tags": ["splat", "unpacking", "args", "kwargs", "decorators", "syntax"]
    },

    {
        "slug": "practicality-beats-purity",
        "term": "Practicality beats purity",
        "part_of_speech": "Aphorism / Guiding Principle",
        "pronunciation": "/ˌpræk.tɪˈkæl.ə.ti biːts ˈpjʊə.rə.ti/",
        "signature": "# Real-world usefulness always trumps theoretical perfection",
        "short_summary": "Aphorism from the Zen of Python emphasizing that pragmatic solutions triumph over theoretical architectural perfection.",
        "simple_definition": "**'Although practicality beats purity'** is line 9 of the Zen of Python. It balances line 8 (*'Special cases aren't special enough to break the rules'*), declaring that while clean rules and purity are vital, real-world utility and practical programmer productivity take precedence when compromises are required.",
        "full_description": """Python is fundamentally a pragmatic language designed for humans to get work done quickly. This principle is why Python allows mutable default arguments (despite traps), supports multiple inheritance, and allows duck typing rather than enforcing rigid abstract type hierarchies.""",
        "title": "Real-world: Practicality over Theoretical Purity in Python",
        "code": """# In pure OOP theory, all data must be encapsulated in classes with getters/setters.
# In Python, practicality beats purity: simple dataclasses or namedtuples win!

from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

# Extremely practical, readable, and clean:
p = Point(10.5, 20.0)
print(f"Point coordinates: ({p.x}, {p.y})")""",
        "gotchas": [
            "Do not use 'practicality beats purity' as an excuse to write sloppy, untested, or unmaintainable code."
        ],
        "tags": ["practicality", "purity", "zen", "philosophy", "design"]
    },

    {
        "slug": "namespaces-are-one-honking-great-idea",
        "term": "Namespaces are one honking great idea",
        "part_of_speech": "Aphorism / Architecture Principle",
        "pronunciation": "/ˈneɪm.speɪs.ɪz ɑːr wʌn ˈhɒŋ.kɪŋ ɡreɪt aɪˈdɪə/",
        "signature": "import math; math.sqrt(25)  # math namespace keeps sqrt clean",
        "short_summary": "The enthusiastic concluding line of the Zen of Python celebrating modular isolation and namespace clarity.",
        "simple_definition": "**'Namespaces are one honking great idea -- let's do more of those!'** is the triumphant final line of the Zen of Python. It celebrates the power of namespaces (modules, packages, classes, and scopes) to keep identifiers isolated and prevent naming collisions across libraries.",
        "full_description": """Before namespaces became standard, programming languages placed all functions and variables into a single global pool, leading to catastrophic name collisions.

In Python, every `.py` file is automatically its own isolated module namespace. Writing `import json` and `import csv` keeps their respective `loads` and `reader` functions organized and conflict-free.""",
        "title": "Real-world: Namespace Isolation Across Modules",
        "code": """import json
import pickle

# Both modules serialize data, but namespaces keep them distinct:
data = {"user": "charlie", "score": 99}

json_bytes = json.dumps(data)
pickle_bytes = pickle.dumps(data)

print(f"JSON namespace string: {json_bytes}")
print(f"Pickle namespace bytes length: {len(pickle_bytes)}")""",
        "gotchas": [
            "Wildcard imports (`from module import *`) actively destroy the benefits of namespaces by dumping everything into the local scope."
        ],
        "tags": ["namespaces", "zen", "modules", "packages", "architecture"]
    },

    {
        "slug": "pythonista",
        "term": "Pythonista (Pythoneer)",
        "part_of_speech": "Demonym / Community Phrase",
        "pronunciation": "/ˌpaɪ.θəˈniː.stə/",
        "signature": "# A member of the welcoming global Python programming community",
        "short_summary": "The affectionate term for a programmer, enthusiast, or practitioner who writes Python.",
        "simple_definition": "**Pythonista** (or sometimes **Pythoneer**) is the affectionate title used to refer to someone who writes Python code, builds Python applications, or actively participates in the Python community. The community is celebrated globally for its inclusive culture, PyCon conferences, and emphasis on mentorship.",
        "full_description": """The Python community has earned a worldwide reputation for being one of the most welcoming and diverse open-source communities. Pythonistas span scientific researchers, machine learning engineers, web developers, educators, and hobbyists.""",
        "title": "Real-world: Welcome to the Python Community",
        "code": """# A warm greeting to all aspiring and experienced Pythonistas!
def pythonista_greeting(name):
    return f"Welcome, {name}! Happy Python programming with PyDict 🐍"

print(pythonista_greeting("Pythonista"))""",
        "gotchas": [
            "Whether you started coding yesterday or 20 years ago, if you enjoy writing Python, you are a Pythonista."
        ],
        "tags": ["pythonista", "pythoneer", "community", "culture"]
    }
]
