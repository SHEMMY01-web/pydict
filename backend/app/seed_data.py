import json
import sqlite3
from .database import get_db, init_db

ENTRIES = [
    {
        "slug": "type",
        "term": "type",
        "part_of_speech": "Polysemic: Built-in Function / Metaclass / Soft Keyword",
        "pronunciation": "/taɪp/",
        "category": "builtin",
        "signature": "type(object) OR type(name, bases, dict, **kwds) OR type Alias = ...",
        "short_summary": "Polysemic Python symbol: inspects an object's type, dynamically constructs new classes as a metaclass, or declares type aliases in Python 3.12+.",
        "simple_definition": "Think of `type()` as asking Python \"what kind of thing is this?\" When you pass it one thing, it tells you what it is (like checking if something is a number or a string). With three arguments, it can actually create a brand new class on the fly — like building a blueprint at runtime instead of writing `class MyClass:`.",
        "full_description": "The `type` symbol in Python is famously polysemic, serving three distinct foundational roles in the language:\n\n1. **Object Inspection:** Passed 1 argument (`type(obj)`), it returns the class of which `obj` is an instance.\n2. **Dynamic Class Metaclass Constructor:** Passed 3 arguments (`type(name, bases, dict)`), it acts as the primordial metaclass and constructs a brand new class object dynamically at runtime.\n3. **Type Alias Soft Keyword (Python 3.12+):** Introduced in **PEP 695**, `type` acts as a statement keyword to declare formal type aliases with generic parameters.",
        "parameters": [
            {
                "name": "object_or_name",
                "type": "object | str",
                "description": "Either an object instance to inspect (Sense 1), or a string class name (Sense 2).",
                "default": None
            },
            {
                "name": "bases",
                "type": "tuple[type, ...]",
                "description": "Tuple of base classes to inherit from (Sense 2 only).",
                "default": None
            },
            {
                "name": "dict",
                "type": "dict[str, Any]",
                "description": "Class namespace dictionary defining methods and attributes (Sense 2 only).",
                "default": None
            }
        ],
        "returns": {
            "type": "type",
            "description": "Returns the class of object, or a newly constructed class object."
        },
        "added_in_version": "1.0",
        "deprecated_in_version": None,
        "pep_reference": "PEP 695 (Type Parameter Syntax)",
        "pep_url": "https://peps.python.org/pep-0695/",
        "gotchas": [
            "Always prefer `isinstance(x, MyClass)` over `type(x) == MyClass` when checking types, because `type()` checks exact equality and does not recognize subclasses.",
            "`type` is its own type: `isinstance(type, type)` and `type(type) is type` both evaluate to True!",
            "When dynamically building classes with `type(name, bases, dict)`, forgetting to pass `object` in Python 2 or tuples for bases can cause subtle inheritance bugs."
        ],
        "cross_language": {
            "JavaScript": "typeof obj (Sense 1) / class constructor (Sense 2) / type Alias (TypeScript, Sense 3)",
            "Rust": "std::any::type_name::<T>() / struct / type Alias = ...",
            "Go": "reflect.TypeOf(x) / type Name struct / type Name = ..."
        },
        "tags": ["polysemy", "metaclass", "oop", "typing", "pep-695", "builtins"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "Built-in Inspection Function",
                "signature": "type(object) -> type",
                "summary": "Returns the exact class type of the given object.",
                "description": "Standard inspection primitive. Returns the `__class__` attribute of the object. Useful when strict identity of the exact type is needed without inheritance polymorphism.",
                "parameters": [
                    {"name": "object", "type": "Any", "description": "Any Python object or value.", "default": None}
                ],
                "returns": {"type": "type", "description": "The exact class/type of the object."},
                "example_code": "# Real-world: Validating user input types in a form processor\ndef process_field(value):\n    if type(value) is str:\n        return value.strip().title()\n    elif type(value) is int:\n        return max(0, value)  # No negative numbers\n    elif type(value) is list:\n        return [v for v in value if v]  # Remove empty items\n    return value\n\nprint(process_field('  john doe  '))   # 'John Doe'\nprint(process_field(-5))               # 0\nprint(process_field(['a', '', 'b']))   # ['a', 'b']"
            },
            {
                "sense_number": 2,
                "part_of_speech": "Metaclass Class Constructor",
                "signature": "type(name, bases, dict, **kwds) -> type",
                "summary": "Dynamically generates and returns a new class object at runtime.",
                "description": "This is what Python's `class` statement calls under the hood. It dynamically creates a class with specified name, base classes, and attribute dictionary.",
                "parameters": [
                    {"name": "name", "type": "str", "description": "Name of the new class.", "default": None},
                    {"name": "bases", "type": "tuple[type, ...]", "description": "Tuple of superclasses.", "default": None},
                    {"name": "dict", "type": "dict[str, Any]", "description": "Class namespace dict containing attributes and methods.", "default": None}
                ],
                "returns": {"type": "type", "description": "The newly minted class object."},
                "example_code": "# Real-world: Plugin system that creates handler classes from config\ndef make_handler(name, action):\n    def handle(self, data):\n        return f'{self.name} processed: {action(data)}'\n    return type(name, (), {'name': name, 'handle': handle})\n\nUpperHandler = make_handler('UpperHandler', str.upper)\nTrimHandler = make_handler('TrimHandler', str.strip)\n\nprint(UpperHandler().handle('hello'))       # UpperHandler processed: HELLO\nprint(TrimHandler().handle('  spaces  '))  # TrimHandler processed: spaces"
            },
            {
                "sense_number": 3,
                "part_of_speech": "Language Soft Keyword (PEP 695)",
                "signature": "type Alias[T] = definition",
                "summary": "Declares a formal type alias with lazy generic parameter evaluation.",
                "description": "Introduced in Python 3.12 (PEP 695). Replaces old `TypeAlias` typing annotations with a first-class statement syntax.",
                "parameters": [
                    {"name": "Alias", "type": "identifier", "description": "The new type alias identifier.", "default": None}
                ],
                "returns": {"type": "TypeAliasType", "description": "A TypeAliasType instance."},
                "example_code": "# Python 3.12+ Type Alias Statement\n# type Coordinate = tuple[float, float]\n# type Vector[T] = list[T]\nprint('PEP 695 formalizes type alias syntax into Python grammar.')"
            }
        ],
        "version_timeline": [
            {
                "version": "1.0",
                "change_type": "feature",
                "title": "Initial Type Inspector & Metaclass",
                "description": "Included in standard library since the inception of Python for object type inspection."
            },
            {
                "version": "2.2",
                "change_type": "feature",
                "title": "Unification of Types and Classes",
                "description": "PEP 252 & 253 unified user-defined classes and built-in types into a single hierarchy; 'type' became the root metaclass."
            },
            {
                "version": "3.0",
                "change_type": "optimization",
                "title": "Old-Style Classes Removed",
                "description": "Classic old-style classes were eradicated; all classes now implicitly inherit from object and are instances of type."
            },
            {
                "version": "3.12",
                "change_type": "pep",
                "title": "PEP 695 Type Statement Keyword",
                "description": "'type' added as a soft keyword to declare formal type aliases with lazy parameter scoping.",
                "pep": "PEP 695"
            }
        ],
        "examples": [
            {
                "title": "Real-world: Smart Data Validator",
                "code": "# Building a simple data validator that checks field types\ndef validate_record(record, schema):\n    errors = []\n    for field, expected_type in schema.items():\n        value = record.get(field)\n        if value is None:\n            errors.append(f'Missing field: {field}')\n        elif type(value) is not expected_type:\n            errors.append(f'{field}: expected {expected_type.__name__}, got {type(value).__name__}')\n    return errors\n\nuser_schema = {'name': str, 'age': int, 'active': bool}\nuser_data = {'name': 'Alice', 'age': '25', 'active': True}\n\nresult = validate_record(user_data, user_schema)\nfor err in result:\n    print(f'  ⚠ {err}')",
                "expected_output": "  ⚠ age: expected int, got str",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "unpacking-star",
        "term": "* / ** (Unpacking Operators)",
        "part_of_speech": "Polysemic: Operators / Syntax Markers",
        "pronunciation": "/stɑːr / ˈdʌb.əl stɑːr/ (star / double star)",
        "category": "syntax",
        "signature": "*iterable / **mapping / def f(*args, **kwargs)",
        "short_summary": "Polysemic syntax operators: used for multiplication/power, iterable/dictionary unpacking in calls and literals, variadic parameters, and keyword-only argument boundaries.",
        "simple_definition": "The `*` and `**` symbols do different things depending on where you use them. In math, `*` multiplies and `**` raises to a power. In front of a list, `*` \"unpacks\" it — spreading its items out like emptying a bag. `**` does the same for dictionaries. In function definitions, `*args` lets you accept any number of inputs, and `**kwargs` accepts any named inputs.",
        "full_description": "The asterisk symbols `*` and `**` possess extensive polysemy in Python, varying significantly depending on syntactic context:\n\n* **Arithmetic:** Binary `*` is multiplication; binary `**` is exponentiation.\n* **Positional Unpacking:** `*iterable` unpacks elements into a function call or sequence literal (`[*a, *b]`).\n* **Mapping Unpacking:** `**mapping` unpacks key-value pairs into function keyword calls or dict literals (`{**d1, **d2}`).\n* **Variadic Function Parameters:** In parameter lists, `*args` captures arbitrary positional arguments, and `**kwargs` captures arbitrary keyword arguments.\n* **Keyword-Only Boundary:** A bare `*` in a function signature enforces that all subsequent parameters must be specified as keyword arguments.",
        "parameters": [],
        "returns": None,
        "added_in_version": "1.0",
        "deprecated_in_version": None,
        "pep_reference": "PEP 3102 / PEP 3132 / PEP 448",
        "pep_url": "https://peps.python.org/pep-0448/",
        "gotchas": [
            "In dict unpacking `{**a, **b}`, keys in `b` silently overwrite identical keys from `a`.",
            "Bare `*` in parameter lists cannot be assigned a value: it is purely a syntactic boundary separating positional-or-keyword from keyword-only arguments."
        ],
        "cross_language": {
            "JavaScript": "...spread operator (for both arrays and objects) / rest parameters (...args)",
            "Rust": "No direct equivalent; uses slices, macro rep, or Default",
            "Go": "...variadic parameters (slices only)"
        },
        "tags": ["polysemy", "operators", "unpacking", "syntax", "pep-448"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "Arithmetic Operators",
                "signature": "a * b (multiplication) | a ** b (exponentiation)",
                "summary": "Performs numeric multiplication or calculates base raised to a power.",
                "description": "Dispatches to __mul__ and __pow__ special methods respectively.",
                "example_code": "# Real-world: Calculate compound interest\nprincipal = 1000\nrate = 0.05\nyears = 10\nfinal = principal * (1 + rate) ** years\nprint(f'${principal} at {rate*100}% for {years} years = ${final:.2f}')"
            },
            {
                "sense_number": 2,
                "part_of_speech": "Iterable Sequence Unpacking",
                "signature": "*iterable",
                "summary": "Splats sequence elements into function calls or sequence literals.",
                "description": "Expanded in PEP 448 to allow arbitrary multiple unpackings in list, tuple, and set literals.",
                "example_code": "# Real-world: Merging shopping cart items from multiple sources\nfavorites = ['Python Book', 'Mechanical Keyboard']\nnew_arrivals = ['USB-C Hub', 'Monitor Light']\nrecommended = ['Standing Desk']\n\nfull_cart = [*favorites, *new_arrivals, *recommended]\nprint('Your cart:', full_cart)\nprint(f'Total items: {len(full_cart)}')"
            },
            {
                "sense_number": 3,
                "part_of_speech": "Dictionary Mapping Unpacking",
                "signature": "**mapping",
                "summary": "Unpacks key-value mappings into function keyword calls or dictionary literals.",
                "description": "Merges dictionary key-value pairs into a new dictionary literal.",
                "example_code": "# Real-world: Merging app config with user preferences\ndefault_config = {'theme': 'dark', 'font_size': 14, 'language': 'en'}\nuser_prefs = {'font_size': 18, 'sidebar': True}\n\nfinal_config = {**default_config, **user_prefs}\nprint('Final config:')\nfor key, val in final_config.items():\n    print(f'  {key}: {val}')"
            },
            {
                "sense_number": 4,
                "part_of_speech": "Variadic Function Parameters",
                "signature": "def func(*args, **kwargs):",
                "summary": "Collects variable numbers of positional arguments into a tuple, and keyword arguments into a dict.",
                "description": "Provides flexible function signatures accepting arbitrary arguments.",
                "example_code": "# Real-world: Flexible logging function\ndef log(level, *messages, **metadata):\n    tag = f'[{level.upper()}]'\n    body = ' '.join(str(m) for m in messages)\n    extras = ' | '.join(f'{k}={v}' for k, v in metadata.items())\n    print(f'{tag} {body}' + (f' ({extras})' if extras else ''))\n\nlog('info', 'User logged in', user='alice', ip='192.168.1.1')\nlog('error', 'Connection failed', 'retrying...', attempts=3)"
            },
            {
                "sense_number": 5,
                "part_of_speech": "Keyword-Only Parameter Barrier",
                "signature": "def func(pos, *, keyword_only):",
                "summary": "A bare asterisk enforces that all subsequent parameters must be passed using keywords.",
                "description": "Introduced in PEP 3102 for Python 3.0 to prevent ambiguous call sites for boolean flags.",
                "example_code": "# Real-world: API client with clear config options\ndef fetch_data(url, *, timeout=30, retries=3, verify_ssl=True):\n    print(f'Fetching {url}')\n    print(f'  timeout={timeout}s, retries={retries}, SSL={verify_ssl}')\n\nfetch_data('https://api.example.com/users', timeout=10, verify_ssl=False)"
            }
        ],
        "version_timeline": [
            {
                "version": "1.0",
                "change_type": "feature",
                "title": "Basic Arithmetic & *args, **kwargs",
                "description": "Multiplication, exponentiation, and variadic function argument packing."
            },
            {
                "version": "3.0",
                "change_type": "pep",
                "title": "PEP 3102 Keyword-Only Arguments & PEP 3132 Extended Unpacking",
                "description": "Introduced bare '*' in signatures for keyword-only parameters, and 'first, *rest = seq' extended unpacking in assignments.",
                "pep": "PEP 3102"
            },
            {
                "version": "3.5",
                "change_type": "pep",
                "title": "PEP 448 Additional Unpacking Generalizations",
                "description": "Allowed multiple *iterable and **dict unpackings inside function calls and sequence/dictionary literals: [*a, *b], {**d1, **d2}.",
                "pep": "PEP 448"
            }
        ],
        "examples": [
            {
                "title": "Real-world: Building a User Profile from Multiple Data Sources",
                "code": "# Combining data from database, API, and local cache\ndb_record = {'name': 'Alice', 'email': 'alice@example.com'}\napi_data = {'avatar_url': 'https://img.example.com/alice.png', 'role': 'admin'}\nlocal_prefs = {'theme': 'dark', 'notifications': True}\n\n# Merge all sources into one profile dict\nprofile = {**db_record, **api_data, **local_prefs}\nprint('Complete user profile:')\nfor key, value in profile.items():\n    print(f'  {key}: {value}')\n\n# Extended unpacking in assignment\nscores = [95, 88, 76, 91, 83, 70]\nbest, second, *rest = sorted(scores, reverse=True)\nprint(f'\\nTop 2 scores: {best}, {second}')\nprint(f'Remaining: {rest}')",
                "expected_output": "Complete user profile:\n  name: Alice\n  email: alice@example.com\n  avatar_url: https://img.example.com/alice.png\n  role: admin\n  theme: dark\n  notifications: True\n\nTop 2 scores: 95, 91\nRemaining: [88, 83, 76, 70]",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "subscript-brackets",
        "term": "[] (Brackets / Subscript Syntax)",
        "part_of_speech": "Polysemic: Literal / Indexing / Slicing / Generics",
        "pronunciation": "/ˈbræk.ɪts/ (brackets)",
        "category": "syntax",
        "signature": "[items] | obj[index] | seq[start:stop:step] | type[params]",
        "short_summary": "Polysemic syntax brackets: used for list literals, sequence/mapping indexing, slicing, and generic type parameterization.",
        "simple_definition": "Square brackets `[]` are one of the most used symbols in Python. They create lists (`[1, 2, 3]`), grab items by position (`my_list[0]` gets the first item), slice out chunks (`my_list[1:3]`), and even describe types in modern Python (`list[str]` means \"a list of strings\").",
        "full_description": "Square brackets `[]` fulfill four core syntactic purposes in Python:\n\n1. **List Literal Creation:** `[1, 2, 3]` instantiates a new mutable list object.\n2. **Subscript Indexing:** `seq[0]` or `mapping['key']` invokes the `__getitem__` or `__setitem__` special method.\n3. **Slicing Notation:** `seq[start:stop:step]` passes a `slice` object for sub-sequence extraction.\n4. **Generic Type Parameterization (Python 3.9+):** Standard collection types support type subscriptions like `list[str]` or `dict[str, int]` without importing from `typing` (PEP 585).",
        "parameters": [],
        "returns": None,
        "added_in_version": "1.0",
        "deprecated_in_version": None,
        "pep_reference": "PEP 585 (Type Hinting Generics in Standard Collections)",
        "pep_url": "https://peps.python.org/pep-0585/",
        "gotchas": [
            "Negative indexes wrap around from the end: `seq[-1]` is the last element.",
            "Slicing creates a shallow copy: mutating nested objects within a sliced list mutates them in the original list as well."
        ],
        "cross_language": {
            "JavaScript": "Arrays [1, 2], indexing obj[key], and TypeScript generics Array<T> or T[]",
            "Rust": "Arrays [1, 2, 3], slices &slice[1..3], and generics Vec<T>",
            "Go": "Slices []int{1, 2}, indexing slice[0], and generics []T"
        },
        "tags": ["polysemy", "syntax", "indexing", "slicing", "generics", "pep-585"],
        "senses": [
            {
                "sense_number": 1,
                "part_of_speech": "List Literal Constructor",
                "signature": "[item1, item2, ...]",
                "summary": "Constructs a new mutable sequence list.",
                "description": "Instantiates a Python list object in memory.",
                "example_code": "# Real-world: Todo list manager\ntasks = ['Buy groceries', 'Write report', 'Call dentist']\nprint(f'You have {len(tasks)} tasks:')\nfor i, task in enumerate(tasks, 1):\n    print(f'  {i}. {task}')"
            },
            {
                "sense_number": 2,
                "part_of_speech": "Sequence & Mapping Indexing",
                "signature": "target[key_or_index]",
                "summary": "Fetches or assigns an element using its zero-based index or dictionary key.",
                "description": "Dispatches directly to target.__getitem__(key) or target.__setitem__(key, val).",
                "example_code": "# Real-world: Student grade lookup\ngrades = {'Alice': 92, 'Bob': 85, 'Charlie': 78}\nstudent = 'Alice'\nprint(f\"{student}'s grade: {grades[student]}\")\nprint(f'Class average: {sum(grades.values()) / len(grades):.1f}')"
            },
            {
                "sense_number": 3,
                "part_of_speech": "Sequence Slicing Notation",
                "signature": "seq[start:stop:step]",
                "summary": "Extracts a contiguous or stepped sub-sequence.",
                "description": "Evaluates to a slice object slice(start, stop, step) passed to __getitem__.",
                "example_code": "# Real-world: Paginating search results\nall_results = [f'Result {i}' for i in range(1, 51)]\npage = 2\nper_page = 10\nstart = (page - 1) * per_page\n\ncurrent_page = all_results[start : start + per_page]\nprint(f'Page {page} of {len(all_results)//per_page}:')\nfor item in current_page:\n    print(f'  {item}')"
            },
            {
                "sense_number": 4,
                "part_of_speech": "Generic Type Subscripting (PEP 585)",
                "signature": "collection[type_param]",
                "summary": "Parameterizes standard collection classes for type checking.",
                "description": "Enables list[str], dict[str, int], and tuple[int, ...] directly on built-in types without typing.List.",
                "example_code": "# Real-world: Type-hinted function signatures\ndef get_top_students(grades: dict[str, int], threshold: int = 90) -> list[str]:\n    return [name for name, score in grades.items() if score >= threshold]\n\nclass_grades = {'Alice': 95, 'Bob': 82, 'Charlie': 91, 'Diana': 78}\nhonor_roll = get_top_students(class_grades)\nprint('Honor roll:', honor_roll)"
            }
        ],
        "version_timeline": [
            {
                "version": "1.0",
                "change_type": "feature",
                "title": "List Literals, Indexing & Simple Slicing",
                "description": "Standard brackets indexing and list syntax present since Python 1.0."
            },
            {
                "version": "2.3",
                "change_type": "feature",
                "title": "Extended Slices (Step Parameter)",
                "description": "Extended slicing syntax [start:stop:step] made uniform across all built-in sequences."
            },
            {
                "version": "3.9",
                "change_type": "pep",
                "title": "PEP 585 Standard Collections as Generics",
                "description": "Enabled subscription syntax on standard collections: list[int], dict[str, int] without importing from typing.",
                "pep": "PEP 585"
            }
        ],
        "examples": [
            {
                "title": "Real-world: Log File Analyzer with Slicing",
                "code": "# Analyzing recent server log entries\nlogs = [\n    '2024-01-15 INFO: Server started',\n    '2024-01-15 WARN: High memory usage',\n    '2024-01-15 ERROR: Database timeout',\n    '2024-01-15 INFO: Request served in 45ms',\n    '2024-01-15 ERROR: Connection refused',\n    '2024-01-15 INFO: Backup completed',\n]\n\n# Get last 3 entries\nprint('Recent logs:')\nfor log in logs[-3:]:\n    print(f'  {log}')\n\n# Get only ERROR entries\nerrors = [log for log in logs if 'ERROR' in log]\nprint(f'\\nFound {len(errors)} error(s):')\nfor err in errors:\n    print(f'  ⚠ {err}')",
                "expected_output": "Recent logs:\n  2024-01-15 INFO: Request served in 45ms\n  2024-01-15 ERROR: Connection refused\n  2024-01-15 INFO: Backup completed\n\nFound 2 error(s):\n  ⚠ 2024-01-15 ERROR: Database timeout\n  ⚠ 2024-01-15 ERROR: Connection refused",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "enumerate",
        "term": "enumerate",
        "part_of_speech": "Built-in Function",
        "pronunciation": "/ɪˈnjuːmərˌeɪt/ (eh-NEW-mer-ate)",
        "category": "builtin",
        "signature": "enumerate(iterable, start=0) -> enumerate",
        "short_summary": "Returns an enumerate object that yields pairs of index count and values from an iterable.",
        "simple_definition": "When you loop through a list and need to know \"which number item am I on?\", `enumerate()` gives you both the position number and the item itself. Instead of tracking a counter variable manually, it pairs each item with its index automatically.",
        "full_description": "The `enumerate()` built-in simplifies loops where both the current index and element are required. Rather than manually tracking an index variable or indexing with `range(len(seq))`, `enumerate` wraps an iterable in a generator-like iterator yielding `(index, value)` tuples.\n\n### Etymology & Origin\nIntroduced in **PEP 279** for Python 2.3 to eliminate the anti-pattern `i = 0; for x in seq: ...; i += 1` or `for i in range(len(seq)): x = seq[i]`.",
        "parameters": [
            {
                "name": "iterable",
                "type": "Iterable[T]",
                "description": "Any sequence, iterator, or object supporting iteration (__iter__ or __getitem__).",
                "default": None
            },
            {
                "name": "start",
                "type": "int",
                "description": "The initial index counter value. Defaults to 0.",
                "default": "0"
            }
        ],
        "returns": {
            "type": "enumerate[tuple[int, T]]",
            "description": "An iterator yielding tuples containing a count (from start) and the values obtained from iterating over iterable."
        },
        "added_in_version": "2.3",
        "deprecated_in_version": None,
        "pep_reference": "PEP 279",
        "pep_url": "https://peps.python.org/pep-0279/",
        "gotchas": [
            "Returns an iterator, not a list. Once exhausted, iterating over it again yields nothing.",
            "Memory efficient: it generates tuples lazily on each step, consuming O(1) auxiliary memory.",
            "Be mindful when unpacking: if the element itself is a tuple, use `for idx, (a, b) in enumerate(pairs):`."
        ],
        "cross_language": {
            "JavaScript": "array.entries() or array.forEach((val, idx) => ...)",
            "Rust": "iterator.enumerate()",
            "Go": "for idx, val := range slice",
            "Ruby": "enumerable.each_with_index { |val, idx| ... }"
        },
        "tags": ["iterators", "builtins", "loops", "idiomatic"],
        "version_timeline": [
            {
                "version": "2.3",
                "change_type": "pep",
                "title": "PEP 279 Introduction",
                "description": "Introduced in Python 2.3 to eliminate manual loop counter increments.",
                "pep": "PEP 279"
            },
            {
                "version": "2.6",
                "change_type": "feature",
                "title": "start Parameter Added",
                "description": "Added optional 'start' parameter allowing custom offset initialization (e.g. 1-based indexing)."
            }
        ],
        "examples": [
            {
                "title": "Real-world: Restaurant Menu Display",
                "code": "# Building a numbered restaurant menu\nmenu_items = [\n    ('Margherita Pizza', 12.99),\n    ('Caesar Salad', 8.50),\n    ('Grilled Salmon', 18.75),\n    ('Chocolate Cake', 7.25),\n]\n\nprint('=== Today\\'s Menu ===')\nfor num, (dish, price) in enumerate(menu_items, start=1):\n    print(f'  {num}. {dish:.<25} ${price:.2f}')\nprint(f'\\n  ({len(menu_items)} items available)')",
                "expected_output": "=== Today's Menu ===\n  1. Margherita Pizza......... $12.99\n  2. Caesar Salad............. $8.50\n  3. Grilled Salmon........... $18.75\n  4. Chocolate Cake........... $7.25\n\n  (4 items available)",
                "is_interactive": True
            },
            {
                "title": "Real-world: Find Errors in a Config File",
                "code": "# Scanning a config file for problems\nconfig_lines = [\n    'host=localhost',\n    'port=8080',\n    'debug=yes',\n    '',                   # Empty line — bad!\n    'database=myapp_db',\n    'password=',          # Empty value — bad!\n    'timeout=30',\n]\n\nprint('Config validation report:')\nfor line_num, line in enumerate(config_lines, start=1):\n    if not line.strip():\n        print(f'  Line {line_num}: ⚠ Empty line detected')\n    elif '=' in line and not line.split('=', 1)[1].strip():\n        print(f'  Line {line_num}: ⚠ Missing value for \"{line.split(\"=\")[0]}\"')\n    else:\n        print(f'  Line {line_num}: ✓ {line}')",
                "expected_output": "Config validation report:",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "zip",
        "term": "zip",
        "part_of_speech": "Built-in Function",
        "pronunciation": "/zɪp/ (zip)",
        "category": "builtin",
        "signature": "zip(*iterables, strict=False) -> zip object",
        "short_summary": "Iterates over several iterables in parallel, producing tuples with an item from each one.",
        "simple_definition": "`zip()` is like a zipper on a jacket — it joins two (or more) lists side by side. If you have a list of names and a list of scores, `zip()` pairs them up: name 1 with score 1, name 2 with score 2, etc. It stops when the shortest list runs out (unless you use `strict=True` to catch mismatches).",
        "full_description": "Takes multiple iterables and aggregates corresponding elements into tuples. In Python 3, `zip()` returns a lazy iterator. \n\nBy default, `zip()` stops when the shortest input iterable is exhausted. Starting in **Python 3.10 (PEP 618)**, the `strict=True` parameter raises a `ValueError` if the iterables are of different lengths, preventing silent data truncation bugs.",
        "parameters": [
            {
                "name": "*iterables",
                "type": "Iterable[Any]",
                "description": "Zero or more iterables to be zipped in parallel.",
                "default": None
            },
            {
                "name": "strict",
                "type": "bool",
                "description": "If True, raises ValueError if one iterable is exhausted before the others (Python 3.10+).",
                "default": "False"
            }
        ],
        "returns": {
            "type": "Iterator[Tuple[Any, ...]]",
            "description": "An iterator yielding tuples where the i-th tuple contains the i-th element from each of the argument iterables."
        },
        "added_in_version": "2.0",
        "deprecated_in_version": None,
        "pep_reference": "PEP 618 (strict parameter)",
        "pep_url": "https://peps.python.org/pep-0618/",
        "gotchas": [
            "Silent truncation: without `strict=True`, extra elements in longer iterables are discarded without warning!",
            "Unzipping: you can unzip a list of pairs back into separate tuples using `zip(*pairs)`.",
            "Consumes iterables lazily: if you pass generator expressions, they will only be evaluated as zip advances."
        ],
        "cross_language": {
            "JavaScript": "lodash.zip() or Array.from({length}, (_, i) => [a[i], b[i]])",
            "Rust": "iter_a.zip(iter_b)",
            "Go": "Manual parallel loop index: a[i], b[i]",
            "Ruby": "arr1.zip(arr2)"
        },
        "tags": ["iterators", "builtins", "tuples", "parallel", "pep-618"],
        "version_timeline": [
            {
                "version": "2.0",
                "change_type": "feature",
                "title": "zip() Introduced",
                "description": "Initial introduction in Python 2.0 returning a full list of paired tuples."
            },
            {
                "version": "3.0",
                "change_type": "optimization",
                "title": "Lazy Iterator Semantics",
                "description": "In Python 3.0, zip was changed from eagerly returning a memory-heavy list to returning a lazy iterator."
            },
            {
                "version": "3.10",
                "change_type": "pep",
                "title": "PEP 618: strict Parameter",
                "description": "Added strict=True argument to raise ValueError when lengths mismatch, eliminating silent data loss bugs.",
                "pep": "PEP 618"
            }
        ],
        "examples": [
            {
                "title": "Real-world: Employee Payroll Report",
                "code": "# Building a payroll summary from parallel data\nemployees = ['Alice Johnson', 'Bob Smith', 'Charlie Brown']\nhours_worked = [42, 38, 45]\nhourly_rate = [55.00, 48.50, 62.00]\n\nprint('=== Weekly Payroll ===')\ntotal_payroll = 0\nfor name, hours, rate in zip(employees, hours_worked, hourly_rate):\n    pay = hours * rate\n    total_payroll += pay\n    overtime = max(0, hours - 40)\n    print(f'  {name}: {hours}h × ${rate:.2f} = ${pay:,.2f}' + \n          (f' (incl. {overtime}h overtime)' if overtime else ''))\n\nprint(f'\\n  Total payroll: ${total_payroll:,.2f}')",
                "expected_output": "=== Weekly Payroll ===",
                "is_interactive": True
            },
            {
                "title": "Real-world: CSV Column Transposer",
                "code": "# Transpose rows into columns using zip + unzip trick\ncsv_rows = [\n    ['Name', 'Age', 'City'],\n    ['Alice', '30', 'NYC'],\n    ['Bob', '25', 'LA'],\n    ['Charlie', '35', 'Chicago'],\n]\n\n# Unzip: convert rows to columns\ncolumns = list(zip(*csv_rows))\nfor col in columns:\n    header = col[0]\n    values = col[1:]\n    print(f'{header}: {list(values)}')",
                "expected_output": "Name: ['Alice', 'Bob', 'Charlie']\nAge: ['30', '25', '35']\nCity: ['NYC', 'LA', 'Chicago']",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "yield",
        "term": "yield",
        "part_of_speech": "Keyword / Expression Statement",
        "pronunciation": "/jiːld/ (yeeld)",
        "category": "keyword",
        "signature": "yield [expression_list] / yield from subgen",
        "short_summary": "Pauses function execution and produces an intermediate value to the caller, creating a generator function.",
        "simple_definition": "`yield` turns a regular function into a generator — a function that can pause and resume. Instead of computing everything at once and returning it all, it hands you one value at a time, like a vending machine that dispenses items one by one. This is great for handling large datasets without loading everything into memory.",
        "full_description": "When a function definition contains `yield`, calling it returns a **generator iterator** instead of executing the body immediately. Each time `next()` is called on the generator, execution proceeds until reaching the `yield` statement.\n\n### History & PEPs\n- **PEP 255** (Simple Generators, Python 2.2)\n- **PEP 342** (Coroutines via Enhanced Generators: `.send()`, `.throw()`, `.close()`, Python 2.5)\n- **PEP 380** (Syntax for Delegating to a Subgenerator: `yield from`, Python 3.3).",
        "parameters": [
            {
                "name": "expression_list",
                "type": "Any",
                "description": "Optional expression whose evaluated value is yielded to the caller.",
                "default": "None"
            }
        ],
        "returns": {
            "type": "GeneratorType",
            "description": "The function produces a generator object implementing the iterator protocol (__iter__ and __next__)."
        },
        "added_in_version": "2.2",
        "deprecated_in_version": None,
        "pep_reference": "PEP 255 / PEP 380",
        "pep_url": "https://peps.python.org/pep-0255/",
        "gotchas": [
            "Local state is preserved between yields: variables, loop states, and try/finally blocks remain intact.",
            "Generator can only be consumed once: iterating a second time yields 0 items unless recreated.",
            "`return value` inside a generator raises `StopIteration(value)` (used in coroutines)."
        ],
        "cross_language": {
            "JavaScript": "function* () { yield x; }",
            "Rust": "async/await streams or custom Iterator trait",
            "Go": "Goroutines + channels (go func() { ch <- val }())",
            "C#": "yield return value;"
        },
        "tags": ["generators", "concurrency", "keywords", "memory-efficient", "pep-380"],
        "version_timeline": [
            {
                "version": "2.2",
                "change_type": "pep",
                "title": "PEP 255 Simple Generators",
                "description": "Introduced yield statement creating generators.",
                "pep": "PEP 255"
            },
            {
                "version": "2.5",
                "change_type": "pep",
                "title": "PEP 342 Coroutines via Enhanced Generators",
                "description": "Added .send(), .throw(), and .close() making generators bidirectional data consumers.",
                "pep": "PEP 342"
            },
            {
                "version": "3.3",
                "change_type": "pep",
                "title": "PEP 380 Syntax for Delegating to a Subgenerator",
                "description": "Added 'yield from' syntax to transparently delegate iteration to nested generators.",
                "pep": "PEP 380"
            }
        ],
        "examples": [
            {
                "title": "Real-world: Reading Large Files Line by Line",
                "code": "# Simulating a large log file reader that processes one line at a time\ndef read_log_entries(log_data):\n    \"\"\"Generator that yields parsed log entries without loading all into memory.\"\"\"\n    for line in log_data:\n        if not line.strip():\n            continue  # Skip blank lines\n        parts = line.split(' ', 2)\n        yield {\n            'timestamp': parts[0],\n            'level': parts[1] if len(parts) > 1 else 'UNKNOWN',\n            'message': parts[2] if len(parts) > 2 else ''\n        }\n\n# Sample log data (imagine this is a 10GB file)\nlog_lines = [\n    '10:01 INFO Server started on port 8080',\n    '10:02 WARN Memory usage at 85%',\n    '',\n    '10:05 ERROR Database connection lost',\n    '10:06 INFO Reconnected successfully',\n]\n\n# Process lazily — only one entry in memory at a time\nfor entry in read_log_entries(log_lines):\n    if entry['level'] in ('ERROR', 'WARN'):\n        print(f\"⚠ [{entry['level']}] {entry['message']}\")",
                "expected_output": "⚠ [WARN] Memory usage at 85%\n⚠ [ERROR] Database connection lost",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "gil",
        "term": "GIL (Global Interpreter Lock)",
        "part_of_speech": "Core Architectural Concept",
        "pronunciation": "/dʒɪl/ or /ɡɪl/ (jill or gill)",
        "category": "concept",
        "signature": "sys._is_gil_enabled() [Python 3.13+]",
        "short_summary": "A mutex that prevents multiple native OS threads from executing CPython bytecode simultaneously.",
        "simple_definition": "The GIL is like a microphone at a meeting — only one person (thread) can speak (run Python code) at a time. Even if you have 8 CPU cores, standard Python threads take turns running one at a time. This keeps things safe but limits speed for number-crunching tasks. For I/O tasks like downloading files, it's not a problem because threads release the \"microphone\" while waiting.",
        "full_description": "The GIL is a mutual-exclusion lock used by the CPython implementation to protect memory management and reference counting from race conditions. While it simplifies C extension authoring and single-threaded performance, it means pure CPU-bound Python threads do not execute in parallel across multiple CPU cores on standard CPython.\n\n### Modern Evolution\n- **PEP 703** (Making the Global Interpreter Lock Optional in CPython) was approved for Python 3.13, offering a free-threaded build option (`python3.13t`) that removes the GIL!",
        "parameters": [],
        "returns": None,
        "added_in_version": "1.0 (PEP 703 free-threading in 3.13)",
        "deprecated_in_version": None,
        "pep_reference": "PEP 703",
        "pep_url": "https://peps.python.org/pep-0703/",
        "gotchas": [
            "I/O-bound tasks release the GIL! Python threading is great for network downloads, file reads, and database operations.",
            "C extensions (like NumPy, OpenCV, PyTorch) release the GIL during heavy numerical computations, enabling multi-core execution.",
            "For multi-core CPU-bound tasks in standard Python, use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`."
        ],
        "cross_language": {
            "JavaScript / Node.js": "Single-threaded event loop with Worker Threads",
            "Go": "Goroutines with M:N multiplexing on all OS threads without a GIL",
            "Rust": "Fearless concurrency with Send/Sync traits and true multi-threading"
        },
        "tags": ["architecture", "concurrency", "cpython", "threading", "pep-703"],
        "version_timeline": [
            {
                "version": "1.0",
                "change_type": "feature",
                "title": "Initial GIL Architecture",
                "description": "Original GIL mutex added to CPython to simplify memory reference counting."
            },
            {
                "version": "3.2",
                "change_type": "optimization",
                "title": "New GIL Implementation",
                "description": "Antoine Pitrou rewritten GIL introduced to reduce thread switching contention on multicore systems."
            },
            {
                "version": "3.13",
                "change_type": "pep",
                "title": "PEP 703 Free-Threaded CPython",
                "description": "Experimental no-GIL build ('python3.13t') approved, enabling multi-threaded multicore execution in pure Python.",
                "pep": "PEP 703"
            }
        ],
        "examples": [
            {
                "title": "Real-world: Threading for I/O vs CPU Tasks",
                "code": "import threading\nimport time\n\n# Simulating I/O-bound work (GIL is released during sleep/IO)\ndef download_file(name, seconds):\n    print(f'⬇ Starting download: {name}')\n    time.sleep(seconds)  # Simulates network I/O\n    print(f'✓ Finished: {name}')\n\n# Run 3 downloads concurrently\nstart = time.time()\nthreads = [\n    threading.Thread(target=download_file, args=('data.csv', 0.5)),\n    threading.Thread(target=download_file, args=('image.png', 0.3)),\n    threading.Thread(target=download_file, args=('report.pdf', 0.4)),\n]\nfor t in threads:\n    t.start()\nfor t in threads:\n    t.join()\n\nelapsed = time.time() - start\nprint(f'\\nAll downloads completed in {elapsed:.2f}s (not 1.2s — threads ran concurrently!)')",
                "expected_output": "⬇ Starting download: data.csv",
                "is_interactive": True
            }
        ]
    },
    # ===== NEW PROGRAMMING TECHNIQUE ENTRIES =====
    {
        "slug": "list-comprehension",
        "term": "List Comprehension",
        "part_of_speech": "Programming Technique / Syntax Sugar",
        "pronunciation": "/lɪst kɒmprɪˈhenʃən/",
        "category": "technique",
        "signature": "[expression for item in iterable if condition]",
        "short_summary": "A concise, readable syntax for creating new lists by applying an expression to each item in an iterable, with optional filtering.",
        "simple_definition": "A list comprehension is a one-liner shortcut for building lists. Instead of writing a for-loop that appends items one by one, you describe what you want in a single line inside square brackets. Think of it as saying: \"Give me [this thing] for [each item] in [this collection] if [some condition is true].\"",
        "full_description": "List comprehensions provide a compact and expressive way to create lists from existing iterables. They combine the functionality of `map()` and `filter()` into a single readable expression.\n\n### Structure\n```\n[expression for variable in iterable if condition]\n```\n\n**Equivalent loop:**\n```python\nresult = []\nfor variable in iterable:\n    if condition:\n        result.append(expression)\n```\n\n### Nested Comprehensions\nYou can nest loops: `[expr for x in iter1 for y in iter2]` flattens nested structures.\n\n### Etymology\nInspired by mathematical set-builder notation: {x² | x ∈ ℕ, x > 0}.",
        "parameters": [],
        "returns": {"type": "list", "description": "A new list containing the results of the expression applied to each filtered item."},
        "added_in_version": "2.0",
        "deprecated_in_version": None,
        "pep_reference": "PEP 202 (List Comprehensions)",
        "pep_url": "https://peps.python.org/pep-0202/",
        "gotchas": [
            "Don't overuse: if a comprehension spans multiple lines or has more than 2 nested loops, a regular for-loop is more readable.",
            "List comprehensions always create a full list in memory. For large data, use a generator expression `(x for x in ...)` instead.",
            "Variables defined inside a comprehension are scoped to it (Python 3) — they don't leak into the surrounding scope."
        ],
        "cross_language": {
            "JavaScript": "array.map(x => expr).filter(x => cond) or Array.from()",
            "Rust": "iter.filter(|x| cond).map(|x| expr).collect::<Vec<_>>()",
            "Go": "No native equivalent; use a for loop with append",
            "Haskell": "[expr | x <- list, condition]"
        },
        "tags": ["technique", "syntax-sugar", "lists", "idiomatic", "functional", "pep-202"],
        "senses": [],
        "version_timeline": [
            {"version": "2.0", "change_type": "pep", "title": "PEP 202 List Comprehensions", "description": "Introduced list comprehension syntax as a concise way to build lists from iterables.", "pep": "PEP 202"},
            {"version": "3.0", "change_type": "feature", "title": "Scoped Variables", "description": "Loop variables in list comprehensions no longer leak into the enclosing scope."}
        ],
        "examples": [
            {
                "title": "Real-world: Cleaning User Input Data",
                "code": "# Processing raw form submissions from a website\nraw_emails = [\n    '  Alice@Example.COM  ',\n    'bob@gmail.com',\n    '',\n    '  CHARLIE@Yahoo.com',\n    '   ',\n    'diana@outlook.com  ',\n]\n\n# Clean: strip whitespace, lowercase, remove empties\nclean_emails = [email.strip().lower() for email in raw_emails if email.strip()]\n\nprint(f'Valid emails ({len(clean_emails)}):')\nfor email in clean_emails:\n    print(f'  ✉ {email}')\n\n# Bonus: Extract just the domains\ndomains = [email.split('@')[1] for email in clean_emails]\nprint(f'\\nUnique domains: {sorted(set(domains))}')",
                "expected_output": "Valid emails (4):\n  ✉ alice@example.com\n  ✉ bob@gmail.com\n  ✉ charlie@yahoo.com\n  ✉ diana@outlook.com\n\nUnique domains: ['example.com', 'gmail.com', 'outlook.com', 'yahoo.com']",
                "is_interactive": True
            },
            {
                "title": "Real-world: Transforming Product Data for an API",
                "code": "# Converting raw product data into API-ready format\nproducts = [\n    {'name': 'Laptop', 'price': 999.99, 'in_stock': True},\n    {'name': 'Mouse', 'price': 29.99, 'in_stock': True},\n    {'name': 'Webcam', 'price': 79.99, 'in_stock': False},\n    {'name': 'Keyboard', 'price': 149.99, 'in_stock': True},\n    {'name': 'Monitor', 'price': 449.99, 'in_stock': False},\n]\n\n# Get only available products with formatted prices\navailable = [\n    f\"{p['name']} — ${p['price']:.2f}\"\n    for p in products\n    if p['in_stock']\n]\n\nprint('🛒 Available products:')\nfor item in available:\n    print(f'  {item}')\n\n# Calculate total value of in-stock inventory\ntotal = sum(p['price'] for p in products if p['in_stock'])\nprint(f'\\n💰 In-stock inventory value: ${total:,.2f}')",
                "expected_output": "🛒 Available products:\n  Laptop — $999.99\n  Mouse — $29.99\n  Keyboard — $149.99\n\n💰 In-stock inventory value: $1,179.97",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "dict-comprehension",
        "term": "Dictionary Comprehension",
        "part_of_speech": "Programming Technique / Syntax Sugar",
        "pronunciation": "/dɪkt kɒmprɪˈhenʃən/",
        "category": "technique",
        "signature": "{key_expr: value_expr for item in iterable if condition}",
        "short_summary": "A concise syntax for building dictionaries by specifying key-value pairs derived from an iterable, with optional filtering.",
        "simple_definition": "Just like list comprehensions build lists, dict comprehensions build dictionaries in a single line. You specify a key and a value for each item in your data. It's perfect for transforming data — like converting a list of names into a lookup table.",
        "full_description": "Dictionary comprehensions provide a compact way to create dictionaries from iterables. They mirror the syntax of list comprehensions but produce key-value mappings instead of sequences.\n\n### Structure\n```python\n{key_expr: value_expr for variable in iterable if condition}\n```\n\nIntroduced alongside set comprehensions in **PEP 274** for Python 2.7 / 3.0.",
        "parameters": [],
        "returns": {"type": "dict", "description": "A new dictionary built from the key-value pairs produced by the expression."},
        "added_in_version": "2.7",
        "deprecated_in_version": None,
        "pep_reference": "PEP 274",
        "pep_url": "https://peps.python.org/pep-0274/",
        "gotchas": [
            "Duplicate keys: if the key expression produces the same key twice, the last value wins — earlier values are silently overwritten.",
            "Order is preserved in Python 3.7+ (insertion order is guaranteed).",
            "For large data transformations, consider if a regular loop with conditional logic is more readable."
        ],
        "cross_language": {
            "JavaScript": "Object.fromEntries(arr.map(x => [key, val]))",
            "Rust": "iter.map(|x| (key, val)).collect::<HashMap<_, _>>()",
            "Go": "Manual loop: m[key] = val"
        },
        "tags": ["technique", "syntax-sugar", "dictionaries", "idiomatic", "pep-274"],
        "senses": [],
        "version_timeline": [
            {"version": "2.7", "change_type": "pep", "title": "PEP 274 Dict Comprehensions", "description": "Dictionary comprehension syntax introduced for Python 2.7 and 3.0.", "pep": "PEP 274"}
        ],
        "examples": [
            {
                "title": "Real-world: Student Grade Lookup Table",
                "code": "# Converting exam results into a quick-lookup grade map\nstudents = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']\nscores = [92, 67, 85, 45, 78]\n\ndef letter_grade(score):\n    if score >= 90: return 'A'\n    if score >= 80: return 'B'\n    if score >= 70: return 'C'\n    if score >= 60: return 'D'\n    return 'F'\n\n# Build the report card\nreport = {name: {'score': score, 'grade': letter_grade(score)}\n          for name, score in zip(students, scores)}\n\nprint('📋 Report Card:')\nfor name, info in report.items():\n    status = '✓ Pass' if info['score'] >= 60 else '✗ Fail'\n    print(f\"  {name}: {info['score']} ({info['grade']}) — {status}\")\n\n# Quick filter: who needs help?\nstruggling = {name: info['score'] for name, info in report.items() if info['score'] < 70}\nprint(f\"\\n⚠ Students needing support: {struggling}\")",
                "expected_output": "📋 Report Card:",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "f-strings",
        "term": "f-strings (Formatted String Literals)",
        "part_of_speech": "Programming Technique / Syntax Feature",
        "pronunciation": "/ɛf strɪŋz/",
        "category": "technique",
        "signature": "f'text {expression}' / f'text {expr:format_spec}'",
        "short_summary": "String literals prefixed with `f` that embed Python expressions directly inside curly braces, evaluated at runtime.",
        "simple_definition": "f-strings let you put Python code right inside a string by wrapping it in curly braces `{}`. Instead of clunky concatenation like `'Hello ' + name + '!'`, you write `f'Hello {name}!'`. You can even do math, call functions, and format numbers directly inside the braces.",
        "full_description": "Formatted string literals (f-strings), introduced in **PEP 498** for Python 3.6, provide the most readable and performant way to embed expressions inside string literals.\n\n### Key Features\n- Embed any valid Python expression: `f'{2 + 2}'` → `'4'`\n- Format specifiers: `f'{price:.2f}'` → `'19.99'`\n- Self-documenting expressions (3.8+): `f'{x=}'` → `'x=42'`\n- Multiline with triple quotes: `f'''...'''`\n\n### Performance\nf-strings are faster than `.format()` and `%` formatting because the expression is compiled at parse time, not runtime.",
        "parameters": [],
        "returns": {"type": "str", "description": "A formatted string with all embedded expressions evaluated and converted to strings."},
        "added_in_version": "3.6",
        "deprecated_in_version": None,
        "pep_reference": "PEP 498 (Literal String Interpolation)",
        "pep_url": "https://peps.python.org/pep-0498/",
        "gotchas": [
            "Backslashes are not allowed directly inside the `{}` expression (use a variable instead).",
            "Self-documenting f-strings (`f'{x=}'`) were added in Python 3.8, not 3.6.",
            "Be careful with user-provided strings in f-strings — never use f-strings with untrusted input as templates (use `.format_map()` instead)."
        ],
        "cross_language": {
            "JavaScript": "Template literals: `Hello ${name}!`",
            "Rust": "format!(\"Hello {}!\", name) or println! macro",
            "Go": "fmt.Sprintf(\"Hello %s!\", name)",
            "Ruby": "String interpolation: \"Hello #{name}!\""
        },
        "tags": ["technique", "strings", "formatting", "idiomatic", "pep-498"],
        "senses": [],
        "version_timeline": [
            {"version": "3.6", "change_type": "pep", "title": "PEP 498 f-strings", "description": "Introduced f-string literal syntax for inline expression embedding.", "pep": "PEP 498"},
            {"version": "3.8", "change_type": "feature", "title": "Self-documenting Expressions", "description": "Added the `=` specifier: `f'{expr=}'` shows both the expression text and its value."},
            {"version": "3.12", "change_type": "feature", "title": "Relaxed Restrictions", "description": "PEP 701 removed many limitations, allowing backslashes, comments, and nested quotes inside f-string expressions."}
        ],
        "examples": [
            {
                "title": "Real-world: Invoice Generator",
                "code": "# Generating a formatted invoice\ncustomer = 'Acme Corp'\nitems = [\n    ('Widget A', 3, 12.50),\n    ('Gadget B', 1, 45.00),\n    ('Cable C', 5, 3.99),\n]\n\nprint(f'{'=' * 40}')\nprint(f'{\"INVOICE\":^40}')\nprint(f'{'=' * 40}')\nprint(f'Customer: {customer}')\nprint(f'{\"\":-<40}')\nprint(f'{\"Item\":<20} {\"Qty\":>5} {\"Price\":>6} {\"Total\":>7}')\nprint(f'{\"\":-<40}')\n\ngrand_total = 0\nfor name, qty, price in items:\n    total = qty * price\n    grand_total += total\n    print(f'{name:<20} {qty:>5} {price:>6.2f} {total:>7.2f}')\n\nprint(f'{\"\":-<40}')\nprint(f'{\"GRAND TOTAL\":>33} {grand_total:>7.2f}')",
                "expected_output": "========================================",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "decorator",
        "term": "Decorator (@)",
        "part_of_speech": "Programming Technique / Design Pattern",
        "pronunciation": "/ˈdɛkəreɪtər/",
        "category": "technique",
        "signature": "@decorator_name  /  def decorator(func): ...",
        "short_summary": "A function that wraps another function to extend or modify its behavior without changing its source code, using the `@` syntax.",
        "simple_definition": "A decorator is like gift wrapping for functions. The `@` symbol above a function definition says \"before this function runs, wrap it with extra behavior.\" Common uses: adding logging, checking permissions, measuring how long a function takes, or caching results. The original function stays unchanged — the decorator just adds a layer around it.",
        "full_description": "Decorators are a powerful Python pattern that allows you to modify or extend the behavior of functions or classes. The `@decorator` syntax is syntactic sugar for `func = decorator(func)`.\n\n### How It Works\n1. You write a wrapper function that takes a function as input\n2. Inside the wrapper, you can add code before/after calling the original function\n3. You return the wrapper\n4. Apply it with `@wrapper_name` above any function definition\n\n### Common Built-in Decorators\n- `@staticmethod`, `@classmethod`, `@property`\n- `@functools.lru_cache`, `@functools.wraps`\n- `@dataclasses.dataclass`",
        "parameters": [],
        "returns": {"type": "Callable", "description": "A new function that wraps the original with additional behavior."},
        "added_in_version": "2.4",
        "deprecated_in_version": None,
        "pep_reference": "PEP 318 (Decorators for Functions and Methods)",
        "pep_url": "https://peps.python.org/pep-0318/",
        "gotchas": [
            "Always use `@functools.wraps(func)` inside your decorator to preserve the original function's name, docstring, and metadata.",
            "Decorators run at import time, not at call time. The wrapping happens once when the module loads.",
            "Stacking multiple decorators applies them bottom-up: `@a @b def f()` means `f = a(b(f))`."
        ],
        "cross_language": {
            "JavaScript": "Higher-order functions / TypeScript decorators (@decorator)",
            "Rust": "Procedural macros (#[attribute])",
            "Java": "Annotations (@Override, @Deprecated) — metadata only, not behavioral",
            "Go": "No native equivalent; middleware pattern via function wrapping"
        },
        "tags": ["technique", "design-pattern", "functions", "metaprogramming", "pep-318"],
        "senses": [],
        "version_timeline": [
            {"version": "2.4", "change_type": "pep", "title": "PEP 318 Function Decorators", "description": "Introduced the @decorator syntax for functions and methods.", "pep": "PEP 318"},
            {"version": "3.0", "change_type": "pep", "title": "PEP 3129 Class Decorators", "description": "Extended decorator syntax to classes.", "pep": "PEP 3129"}
        ],
        "examples": [
            {
                "title": "Real-world: Performance Timer Decorator",
                "code": "import time\nimport functools\n\n# A decorator that measures how long a function takes\ndef timer(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        result = func(*args, **kwargs)\n        elapsed = time.time() - start\n        print(f'⏱ {func.__name__}() took {elapsed:.4f}s')\n        return result\n    return wrapper\n\n@timer\ndef process_data(n):\n    \"\"\"Simulate processing n records.\"\"\"\n    total = sum(i * i for i in range(n))\n    return total\n\n@timer\ndef generate_report(title):\n    \"\"\"Simulate report generation.\"\"\"\n    time.sleep(0.1)\n    return f'Report: {title}'\n\nresult1 = process_data(100_000)\nresult2 = generate_report('Q4 Sales')\nprint(f'\\nData result: {result1:,}')\nprint(f'Report: {result2}')",
                "expected_output": "⏱ process_data() took",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "context-manager",
        "term": "Context Manager (with statement)",
        "part_of_speech": "Programming Technique / Protocol",
        "pronunciation": "/ˈkɒntekst ˈmænɪdʒər/",
        "category": "technique",
        "signature": "with expression as variable:  /  class CM: __enter__, __exit__  /  @contextmanager",
        "short_summary": "A protocol (`__enter__`/`__exit__`) used with the `with` statement to guarantee resource setup and teardown, even if exceptions occur.",
        "simple_definition": "A context manager automatically handles setup and cleanup for you. The `with` statement says \"open this resource, let me use it, and make sure it gets properly closed when I'm done — even if something goes wrong.\" It's most commonly used for files, database connections, and locks.",
        "full_description": "Context managers implement the `__enter__` and `__exit__` protocol to guarantee resource management. The `with` statement ensures `__exit__` is always called, even if an exception occurs inside the block.\n\n### Three Ways to Create\n1. **Class-based:** Define `__enter__` and `__exit__` methods\n2. **Generator-based:** Use `@contextlib.contextmanager` with a `yield`\n3. **Built-in:** Many Python objects are already context managers (`open()`, `threading.Lock()`, `sqlite3.connect()`)",
        "parameters": [],
        "returns": None,
        "added_in_version": "2.5",
        "deprecated_in_version": None,
        "pep_reference": "PEP 343 (The 'with' Statement)",
        "pep_url": "https://peps.python.org/pep-0343/",
        "gotchas": [
            "If `__exit__` returns `True`, exceptions inside the `with` block are suppressed (swallowed). This is rarely desired.",
            "You can nest context managers: `with open('a') as f1, open('b') as f2:` (or use `contextlib.ExitStack`).",
            "The `as` clause captures the return value of `__enter__`, not the context manager itself."
        ],
        "cross_language": {
            "JavaScript": "No direct equivalent; try/finally or using disposable pattern (TC39 proposal)",
            "Rust": "RAII (Resource Acquisition Is Initialization) via Drop trait",
            "Go": "defer statement: `defer file.Close()`",
            "C#": "using statement: `using (var f = new StreamReader(...)) { ... }`",
            "Java": "try-with-resources: `try (var r = new Resource()) { ... }`"
        },
        "tags": ["technique", "resource-management", "protocol", "pep-343", "files"],
        "senses": [],
        "version_timeline": [
            {"version": "2.5", "change_type": "pep", "title": "PEP 343 The 'with' Statement", "description": "Introduced the with statement and context manager protocol.", "pep": "PEP 343"},
            {"version": "3.1", "change_type": "feature", "title": "Multiple Context Managers", "description": "Allowed multiple comma-separated context managers in a single with statement."},
            {"version": "3.10", "change_type": "feature", "title": "Parenthesized Context Managers", "description": "Allowed parentheses around multiple context managers for better formatting across lines."}
        ],
        "examples": [
            {
                "title": "Real-world: Safe Database Transaction Handler",
                "code": "from contextlib import contextmanager\n\n# Custom context manager for database-like transactions\n@contextmanager\ndef transaction(name):\n    print(f'🔄 BEGIN transaction: {name}')\n    try:\n        yield name  # Let the caller do their work\n        print(f'✓ COMMIT transaction: {name}')\n    except Exception as e:\n        print(f'✗ ROLLBACK transaction: {name} (Error: {e})')\n\n# Successful transaction\nwith transaction('add_user') as tx:\n    print(f'  Inserting user into {tx}...')\n    print(f'  Setting permissions...')\n\nprint()\n\n# Failed transaction (automatically rolled back)\nwith transaction('transfer_funds') as tx:\n    print(f'  Debiting account A...')\n    raise ValueError('Insufficient funds!')  # Oops!\n    print(f'  Crediting account B...')  # Never reached",
                "expected_output": "🔄 BEGIN transaction: add_user\n  Inserting user into add_user...\n  Setting permissions...\n✓ COMMIT transaction: add_user\n\n🔄 BEGIN transaction: transfer_funds\n  Debiting account A...\n✗ ROLLBACK transaction: transfer_funds (Error: Insufficient funds!)",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "lambda-expression",
        "term": "Lambda Expression",
        "part_of_speech": "Programming Technique / Expression",
        "pronunciation": "/ˈlæm.də/",
        "category": "technique",
        "signature": "lambda arguments: expression",
        "short_summary": "Creates a small anonymous (unnamed) function in a single expression, useful for short callbacks and sorting keys.",
        "simple_definition": "A `lambda` is a tiny throw-away function you can write in one line without giving it a name. It's perfect for simple operations like \"sort this list by the second item\" or \"multiply each number by 2\". If you need more than one line, use a regular `def` function instead.",
        "full_description": "Lambda expressions create anonymous functions — small, unnamed functions defined inline. They are limited to a single expression (no statements, no assignments, no multi-line logic).\n\n### When to Use\n- **Sorting keys:** `sorted(items, key=lambda x: x.price)`\n- **Callbacks:** `button.on_click(lambda: print('clicked'))`\n- **Functional programming:** `map(lambda x: x * 2, numbers)`\n\n### When NOT to Use\n- Multi-line logic → use `def`\n- Named for reuse → use `def`\n- Complex conditions → use `def`",
        "parameters": [],
        "returns": {"type": "function", "description": "An anonymous function object that evaluates the expression with the given arguments."},
        "added_in_version": "1.0",
        "deprecated_in_version": None,
        "pep_reference": "Python Language Reference",
        "pep_url": "https://docs.python.org/3/reference/expressions.html#lambda",
        "gotchas": [
            "Lambdas capture variables by reference, not by value! In loops, use default arguments: `lambda x, i=i: ...`",
            "Don't assign lambdas to variables (`fn = lambda x: x + 1`). PEP 8 says use `def fn(x):` instead.",
            "Lambdas can only contain a single expression — no `if/else` statements (but ternary `a if cond else b` works)."
        ],
        "cross_language": {
            "JavaScript": "Arrow functions: (x) => x + 1",
            "Rust": "Closures: |x| x + 1",
            "Go": "Anonymous functions: func(x int) int { return x + 1 }",
            "Java": "Lambda expressions: (x) -> x + 1"
        },
        "tags": ["technique", "functions", "functional-programming", "anonymous", "callbacks"],
        "senses": [],
        "version_timeline": [
            {"version": "1.0", "change_type": "feature", "title": "Lambda Expressions", "description": "Lambda syntax has been part of Python since its earliest versions, inspired by functional programming languages like Lisp."}
        ],
        "examples": [
            {
                "title": "Real-world: Smart Data Sorting",
                "code": "# Sorting employee records by different criteria\nemployees = [\n    {'name': 'Alice', 'dept': 'Engineering', 'salary': 95000},\n    {'name': 'Bob', 'dept': 'Marketing', 'salary': 72000},\n    {'name': 'Charlie', 'dept': 'Engineering', 'salary': 110000},\n    {'name': 'Diana', 'dept': 'Marketing', 'salary': 68000},\n    {'name': 'Eve', 'dept': 'Design', 'salary': 85000},\n]\n\n# Sort by salary (highest first)\nby_salary = sorted(employees, key=lambda e: e['salary'], reverse=True)\nprint('💰 By salary (highest first):')\nfor emp in by_salary[:3]:\n    print(f\"  {emp['name']}: ${emp['salary']:,}\")\n\n# Sort by department, then by name\nby_dept = sorted(employees, key=lambda e: (e['dept'], e['name']))\nprint('\\n🏢 By department:')\nfor emp in by_dept:\n    print(f\"  [{emp['dept']}] {emp['name']}\")\n\n# Quick filter with lambda + filter\nhigh_earners = list(filter(lambda e: e['salary'] > 80000, employees))\nprint(f'\\n🌟 High earners (>$80k): {[e[\"name\"] for e in high_earners]}')",
                "expected_output": "💰 By salary (highest first):",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "unpacking-assignment",
        "term": "Unpacking Assignment (Destructuring)",
        "part_of_speech": "Programming Technique / Syntax Feature",
        "pronunciation": "/ʌnˈpækɪŋ/",
        "category": "technique",
        "signature": "a, b, c = iterable  /  first, *rest = iterable  /  (a, (b, c)) = nested",
        "short_summary": "Assigns multiple variables simultaneously from an iterable's elements in a single statement, with support for starred (`*rest`) catch-all syntax.",
        "simple_definition": "Unpacking lets you split a list, tuple, or any iterable into individual variables in one line. Instead of writing `x = data[0]; y = data[1]`, you write `x, y = data`. The `*` star syntax catches \"the rest\" into a list — like saying \"give me the first two items, and put everything else in a separate pile.\"",
        "full_description": "Python's unpacking assignment (also called destructuring) extracts individual values from sequences and assigns them to variables. **Extended unpacking** (PEP 3132) introduced the `*target` syntax to capture remaining items.\n\n### Forms\n- **Basic:** `a, b = [1, 2]`\n- **Swap:** `a, b = b, a`\n- **Extended:** `first, *middle, last = range(5)`\n- **Nested:** `(a, (b, c)) = (1, (2, 3))`\n- **Loop unpacking:** `for key, value in dict.items():`",
        "parameters": [],
        "returns": None,
        "added_in_version": "1.0",
        "deprecated_in_version": None,
        "pep_reference": "PEP 3132 (Extended Iterable Unpacking)",
        "pep_url": "https://peps.python.org/pep-3132/",
        "gotchas": [
            "ValueError is raised if the number of variables doesn't match the iterable length (unless using *starred catch-all).",
            "You can only have ONE starred variable per unpacking expression.",
            "Swapping `a, b = b, a` works because the right side is fully evaluated before assignment."
        ],
        "cross_language": {
            "JavaScript": "Destructuring: const [a, b, ...rest] = arr; const {x, y} = obj;",
            "Rust": "let (a, b) = tuple; Pattern matching in match/let",
            "Go": "Multiple return: a, b := funcReturningTwo()",
            "Ruby": "Parallel assignment: a, b = [1, 2]"
        },
        "tags": ["technique", "syntax", "assignment", "idiomatic", "pep-3132"],
        "senses": [],
        "version_timeline": [
            {"version": "1.0", "change_type": "feature", "title": "Basic Tuple Unpacking", "description": "Parallel assignment `a, b = 1, 2` available since Python 1.0."},
            {"version": "3.0", "change_type": "pep", "title": "PEP 3132 Extended Iterable Unpacking", "description": "Added *starred catch-all syntax: `first, *rest = iterable`.", "pep": "PEP 3132"}
        ],
        "examples": [
            {
                "title": "Real-world: Parsing Structured Data",
                "code": "# Parsing CSV-like records with unpacking\nrecords = [\n    'Alice,30,Engineer,NYC',\n    'Bob,25,Designer,LA',\n    'Charlie,35,Manager,Chicago',\n]\n\nprint('👥 Employee Directory:')\nfor record in records:\n    name, age, role, city = record.split(',')\n    print(f'  {name} ({age}) — {role} in {city}')\n\n# Extended unpacking: header + data rows\ncsv_data = ['Name,Score,Grade', 'Alice,95,A', 'Bob,82,B', 'Charlie,78,C']\nheader, *rows = csv_data\nprint(f'\\n📊 Columns: {header}')\nprint(f'   Data rows: {len(rows)}')\n\n# Swapping variables (classic Python trick)\nx, y = 'hello', 'world'\nprint(f'\\nBefore swap: x={x}, y={y}')\nx, y = y, x\nprint(f'After swap:  x={x}, y={y}')",
                "expected_output": "👥 Employee Directory:",
                "is_interactive": True
            }
        ]
    },
    {
        "slug": "ternary-expression",
        "term": "Ternary / Conditional Expression",
        "part_of_speech": "Programming Technique / Expression",
        "pronunciation": "/ˈtɜːnəri/",
        "category": "technique",
        "signature": "value_if_true if condition else value_if_false",
        "short_summary": "A one-line expression that evaluates to one of two values based on a boolean condition — Python's inline if/else.",
        "simple_definition": "The ternary expression is Python's way of writing a quick if/else in a single line. Instead of writing 3 lines with `if:` and `else:`, you write `result = 'yes' if condition else 'no'`. Read it like English: \"give me THIS if THAT is true, otherwise give me THAT OTHER THING.\"",
        "full_description": "Python's conditional expression (often called the ternary operator) provides a compact way to choose between two values based on a condition. It was added in **PEP 308** after extensive community discussion.\n\n### Syntax\n```python\nresult = true_value if condition else false_value\n```\n\nThis is equivalent to:\n```python\nif condition:\n    result = true_value\nelse:\n    result = false_value\n```\n\n### Chaining\nYou can chain them: `a if c1 else b if c2 else c` but this quickly becomes unreadable.",
        "parameters": [],
        "returns": {"type": "Any", "description": "The value of the true branch if condition is truthy, otherwise the false branch."},
        "added_in_version": "2.5",
        "deprecated_in_version": None,
        "pep_reference": "PEP 308 (Conditional Expressions)",
        "pep_url": "https://peps.python.org/pep-0308/",
        "gotchas": [
            "Don't chain more than one ternary — it becomes unreadable. Use a regular if/elif/else.",
            "The syntax reads differently from C/JS ternary (`cond ? a : b`). Python's order is: `value_if_true if condition else value_if_false`.",
            "Both branches must be expressions (not statements). You can't use `return` or `raise` inside."
        ],
        "cross_language": {
            "JavaScript": "condition ? trueVal : falseVal",
            "Rust": "if condition { a } else { b } (expressions, not statements)",
            "Go": "No ternary operator; must use if/else block",
            "Java": "condition ? trueVal : falseVal"
        },
        "tags": ["technique", "expressions", "conditional", "syntax", "pep-308"],
        "senses": [],
        "version_timeline": [
            {"version": "2.5", "change_type": "pep", "title": "PEP 308 Conditional Expressions", "description": "Added the ternary conditional expression syntax after years of community debate.", "pep": "PEP 308"}
        ],
        "examples": [
            {
                "title": "Real-world: User-Friendly Data Display",
                "code": "# Formatting data for display with smart defaults\nusers = [\n    {'name': 'Alice', 'age': 30, 'bio': 'Python developer'},\n    {'name': 'Bob', 'age': None, 'bio': ''},\n    {'name': 'Charlie', 'age': 17, 'bio': 'Student'},\n    {'name': 'Diana', 'age': 65, 'bio': None},\n]\n\nprint('👤 User Profiles:')\nfor user in users:\n    age_display = f\"{user['age']} years old\" if user['age'] else 'Age not provided'\n    bio_display = user['bio'] if user['bio'] else 'No bio yet'\n    access = '✓ Full access' if (user['age'] or 0) >= 18 else '⚠ Minor account'\n    \n    print(f\"  {user['name']}: {age_display}\")\n    print(f\"    Bio: {bio_display}\")\n    print(f\"    Status: {access}\")\n    print()\n\n# Practical one-liner: pluralization\nfor count in [0, 1, 5]:\n    label = f\"{count} item{'s' if count != 1 else ''}\"\n    print(f'Cart: {label}')",
                "expected_output": "👤 User Profiles:",
                "is_interactive": True
            }
        ]
    },
]

def seed_database():
    init_db()
    conn = get_db()
    cursor = conn.cursor()

    for item in ENTRIES:
        cursor.execute("""
        INSERT OR REPLACE INTO entries (
            slug, term, part_of_speech, pronunciation, category, signature,
            short_summary, simple_definition, full_description, parameters, returns, added_in_version,
            deprecated_in_version, pep_reference, pep_url, gotchas, cross_language, tags,
            senses, version_timeline
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["slug"],
            item["term"],
            item["part_of_speech"],
            item.get("pronunciation"),
            item["category"],
            item.get("signature"),
            item["short_summary"],
            item.get("simple_definition"),
            item["full_description"],
            json.dumps(item.get("parameters", [])),
            json.dumps(item.get("returns")),
            item.get("added_in_version"),
            item.get("deprecated_in_version"),
            item.get("pep_reference"),
            item.get("pep_url"),
            json.dumps(item.get("gotchas", [])),
            json.dumps(item.get("cross_language", {})),
            json.dumps(item.get("tags", [])),
            json.dumps(item.get("senses", [])),
            json.dumps(item.get("version_timeline", []))
        ))

        # Clear existing code examples for this slug before inserting fresh
        cursor.execute("DELETE FROM code_examples WHERE entry_slug = ?", (item["slug"],))
        for ex in item.get("examples", []):
            cursor.execute("""
            INSERT INTO code_examples (entry_slug, title, code, expected_output, is_interactive)
            VALUES (?, ?, ?, ?, ?)
            """, (item["slug"], ex["title"], ex["code"], ex.get("expected_output"), ex.get("is_interactive", True)))

        # Update FTS table
        cursor.execute("DELETE FROM entries_fts WHERE slug = ?", (item["slug"],))
        cursor.execute("""
        INSERT INTO entries_fts (slug, term, short_summary, full_description, tags, category)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            item["slug"],
            item["term"],
            item["short_summary"],
            item["full_description"],
            " ".join(item.get("tags", [])),
            item["category"]
        ))

    conn.commit()
    conn.close()
    print(f"Successfully seeded {len(ENTRIES)} PyDict entries with simple definitions and real-world examples.")

if __name__ == "__main__":
    seed_database()
