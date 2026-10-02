"""
PyDict — Comprehensive Python Exception & Error Catalog
Provides detailed plain-English conceptual breakdowns, realistic real-world code examples,
common gotchas, and inheritance hierarchy for all Python built-in exceptions.
"""

EXCEPTION_CATALOG = {
    "IndexError": {
        "simple_definition": "`IndexError` occurs when trying to access an item from a list, tuple, or sequence at a position that does not exist (outside the valid range of indices). In Python, indices are 0-based, so a list with 3 elements has valid indices 0, 1, and 2.",
        "title": "Real-world: Safely Reading Command-Line Arguments & User Selections",
        "code": """# Real-world: Reading command-line arguments or pagination selections safely
items = ["dashboard", "settings", "profile"]

# Attempting to access an index out of bounds
try:
    selected = items[5]  # Index 5 does not exist!
except IndexError as err:
    print(f"IndexError caught: {err}")
    selected = items[0]  # Safe fallback to first item

print(f"Active view: {selected}")

# Tip: List slices NEVER raise IndexError — they gracefully return empty lists:
print("Safe slice beyond bounds:", items[10:20])  # Output: []""",
        "gotchas": [
            "Remember Python is 0-indexed: the 3rd item is at index 2, not 3.",
            "Negative indices count backwards from the end (-1 is the last item), but values past -len(seq) will still raise IndexError.",
            "List slicing `lst[start:end]` never raises IndexError; it simply truncates or returns an empty list."
        ],
        "inheritance": "LookupError -> Exception -> BaseException"
    },

    "KeyError": {
        "simple_definition": "`KeyError` occurs when you attempt to retrieve a value from a dictionary using a key that does not exist in that dictionary. You can avoid it by using `dict.get(key, default)` or `if key in dict:`.",
        "title": "Real-world: Safe Dictionary Lookup in Web API Responses",
        "code": """# Real-world: Parsing user payload from an external API
user_payload = {
    "user_id": 4821,
    "username": "alex99",
    "email": "alex@example.com"
}

# 1. Using try/except for mandatory fields
try:
    account_type = user_payload["account_type"]
except KeyError:
    account_type = "standard"  # Default fallback
    print("KeyError: 'account_type' was omitted, defaulted to 'standard'.")

# 2. Idiomatic alternative: dict.get() with fallback
role = user_payload.get("role", "member")
print(f"User: {user_payload['username']} | Role: {role} | Type: {account_type}")""",
        "gotchas": [
            "Use `data.get(key, default)` when a missing key has a reasonable default value.",
            "Use `collections.defaultdict` if you frequently append or increment keys in a dictionary.",
            "`KeyError` is a subclass of `LookupError`, sharing hierarchy with `IndexError`."
        ],
        "inheritance": "LookupError -> Exception -> BaseException"
    },

    "ValueError": {
        "simple_definition": "`ValueError` occurs when a function or operation receives an argument that has the correct data type, but an inappropriate or invalid value (such as passing a non-numeric string `'hello'` to `int()`).",
        "title": "Real-world: Validating User Form Inputs & Conversion",
        "code": """# Real-world: Parsing raw form inputs into typed numbers
form_inputs = ["25", "100", "invalid_number", "42"]

valid_ages = []
for raw in form_inputs:
    try:
        age = int(raw)
        if 0 <= age <= 120:
            valid_ages.append(age)
        else:
            print(f"Out-of-range value rejected: {age}")
    except ValueError as err:
        print(f"ValueError: Could not convert '{raw}' to integer.")

print("Successfully validated ages:", valid_ages)""",
        "gotchas": [
            "`ValueError` means the TYPE is acceptable (e.g. string), but the VALUE is unacceptable (e.g. cannot be parsed).",
            "Unpacking a tuple or list with the wrong number of variables (`a, b = [1, 2, 3]`) also raises ValueError.",
            "Math domain errors like `math.sqrt(-1)` raise ValueError."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "TypeError": {
        "simple_definition": "`TypeError` occurs when an operation or function is applied to an object of an inappropriate type (such as concatenating a string and an integer, or passing the wrong number of positional arguments to a function).",
        "title": "Real-world: Handling Mixed-Type Calculations Safely",
        "code": """# Real-world: Processing invoice line items with mixed data types
def calculate_subtotal(unit_price, quantity):
    try:
        # In dynamic apps, inputs may accidentally arrive as strings
        return unit_price * quantity
    except TypeError:
        # Gracefully cast to float and int
        return float(unit_price) * int(quantity)

print("Numeric calculation:", calculate_subtotal(19.99, 3))
print("String calculation:", calculate_subtotal("19.99", "3"))

# Note: Calling an uncallable object also raises TypeError:
not_a_func = 42
try:
    not_a_func()
except TypeError as err:
    print(f"TypeError caught: {err}")""",
        "gotchas": [
            "Trying to use mutable objects (like lists or dicts) as dictionary keys or set elements raises `TypeError: unhashable type`.",
            "Adding a string and integer (`'Age: ' + 25`) raises TypeError; use f-strings `f'Age: {25}'` instead.",
            "Passing an unexpected number of arguments to a function raises TypeError."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "AttributeError": {
        "simple_definition": "`AttributeError` occurs when you attempt to access an attribute or call a method that does not exist on an object. A very common cause is receiving `None` from a function and trying to call a method on it (`'NoneType' object has no attribute ...`).",
        "title": "Real-world: Safe Attribute Access & Null-Object Checks",
        "code": """# Real-world: Accessing optional profile data safely
class UserProfile:
    def __init__(self, username, email=None):
        self.username = username
        self.email = email

user = UserProfile("jordan_dev")

# 1. Defensive handling of missing attributes
try:
    print("User bio:", user.bio)
except AttributeError:
    print("AttributeError: 'bio' attribute does not exist on UserProfile.")

# 2. Idiomatic prevention using getattr() with default
bio = getattr(user, "bio", "No bio provided.")
print(f"User: {user.username} | Bio: {bio}")

# 3. Guarding against NoneType attribute errors
def get_user_email(profile):
    if profile.email is not None:
        return profile.email.lower()
    return "no-reply@domain.com"

print("Email:", get_user_email(user))""",
        "gotchas": [
            "`'NoneType' object has no attribute '...'` almost always means a function returned `None` instead of the expected object.",
            "Check for typos in method or property names (e.g. `append` vs `apend`).",
            "Use `hasattr(obj, 'attr')` or `getattr(obj, 'attr', default)` to inspect dynamic objects."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "ZeroDivisionError": {
        "simple_definition": "`ZeroDivisionError` occurs when the second argument of a division (`/`, `//`) or modulo (`%`) operation is zero. In mathematics, division by zero is undefined.",
        "title": "Real-world: Safe Metric & Conversion Rate Calculation",
        "code": """# Real-world: Calculating conversion rate and average order value safely
total_revenue = 4500.00
completed_orders = 0  # Brand new store with no orders yet

try:
    avg_order_value = total_revenue / completed_orders
except ZeroDivisionError:
    avg_order_value = 0.0
    print("ZeroDivisionError: No completed orders recorded. Defaulted to $0.00.")

print(f"Average Order Value: ${avg_order_value:.2f}")

# Clean inline alternative using a ternary condition:
total_users = 100
active_users = 0
ratio = (active_users / total_users) if total_users > 0 else 0.0
print(f"Active user ratio: {ratio:.1%}")""",
        "gotchas": [
            "Modulo by zero `x % 0` also raises ZeroDivisionError.",
            "Floating point values like `0.0` still trigger ZeroDivisionError.",
            "`ZeroDivisionError` is a subclass of `ArithmeticError`."
        ],
        "inheritance": "ArithmeticError -> Exception -> BaseException"
    },

    "FileNotFoundError": {
        "simple_definition": "`FileNotFoundError` occurs when attempting to read, rename, or delete a file or directory that does not exist at the designated path.",
        "title": "Real-world: Graceful File Loading with Pathlib Fallbacks",
        "code": """from pathlib import Path
import json

# Real-world: Reading application preferences with safe fallback
config_path = Path("user_settings.json")

try:
    with config_path.open("r", encoding="utf-8") as f:
        settings = json.load(f)
except FileNotFoundError:
    # Use default settings if the file hasn't been created yet
    settings = {"theme": "system", "auto_save": True, "font_size": 14}
    print("FileNotFoundError: 'user_settings.json' missing. Loaded defaults.")

print("Active settings:", settings)

# Idiomatic check using pathlib before reading
if config_path.exists():
    print("Config file exists on disk.")
else:
    print("Config file does not exist on disk.")""",
        "gotchas": [
            "Relative paths depend on current working directory (`os.getcwd()`), which may differ from the script location.",
            "Always use `pathlib.Path` for cross-platform forward/backward slash compatibility.",
            "`FileNotFoundError` is a subclass of `OSError` (errno 2: ENOENT)."
        ],
        "inheritance": "OSError -> Exception -> BaseException"
    },

    "FileExistsError": {
        "simple_definition": "`FileExistsError` occurs when trying to create a file or directory that already exists, especially with functions that require an exclusive non-existing target like `os.mkdir()` or file opening mode `'x'`.",
        "title": "Real-world: Safe Directory Creation with exist_ok",
        "code": """from pathlib import Path
import os

# Real-world: Ensuring an export directory exists without crashing
export_dir = Path("exports/2026/reports")

# The clean modern Python 3 way:
export_dir.mkdir(parents=True, exist_ok=True)
print(f"Directory ready: {export_dir}")

# Using exclusive creation mode 'x' which raises FileExistsError if file exists:
target_file = export_dir / "summary.txt"
target_file.write_text("Initial report data")

try:
    with open(target_file, "x") as f:
        f.write("New data")
except FileExistsError:
    print(f"FileExistsError: '{target_file}' already exists! Avoiding overwrite.")""",
        "gotchas": [
            "Use `pathlib.Path.mkdir(parents=True, exist_ok=True)` to prevent FileExistsError when creating folders.",
            "Opening a file with mode `'x'` (exclusive creation) explicitly guards against accidentally overwriting existing files."
        ],
        "inheritance": "OSError -> Exception -> BaseException"
    },

    "PermissionError": {
        "simple_definition": "`PermissionError` occurs when attempting an operation without the required operating system privileges (such as writing to a read-only directory or modifying a file locked by another process).",
        "title": "Real-world: Handling Restricted File Access Gracefully",
        "code": """import os
from pathlib import Path

# Real-world: Attempting to write logs to a protected location
log_path = Path("/etc/app_log.txt")  # Typically requires root / admin rights

try:
    with open(log_path, "w") as f:
        f.write("System startup log")
except PermissionError as err:
    print(f"PermissionError: Access denied to '{log_path}'.")
    # Graceful fallback to user home directory
    fallback_path = Path.home() / "app_log.txt"
    fallback_path.write_text("System startup log (user fallback)")
    print(f"Saved log to fallback location: {fallback_path}")""",
        "gotchas": [
            "Commonly raised when trying to write to `/`, `/etc`, or `C:\\Program Files` without administrative privileges.",
            "On Windows, opening a file already exclusively locked by another process triggers PermissionError.",
            "`PermissionError` is a subclass of `OSError`."
        ],
        "inheritance": "OSError -> Exception -> BaseException"
    },

    "NameError": {
        "simple_definition": "`NameError` occurs when Python tries to evaluate a variable, function, or module name that has not been defined in the current local, global, or built-in scope. Usually caused by typos or missing imports.",
        "title": "Real-world: Guarding Against Undefined Variables & Optional Libraries",
        "code": """# Real-world: Handling optional configuration or dynamic imports
try:
    # Attempting to use a setting that may not have been declared
    current_status = deployment_env
except NameError:
    deployment_env = "development"
    print("NameError: 'deployment_env' was not defined. Setting to 'development'.")

# Checking if a variable exists in the global scope:
if "DEBUG_MODE" not in globals():
    DEBUG_MODE = False

print(f"Environment: {deployment_env} | Debug: {DEBUG_MODE}")""",
        "gotchas": [
            "Most NameErrors are simple typos in variable or function names (e.g. `prnt` instead of `print`).",
            "Referencing a variable before its assignment statement in the file triggers NameError.",
            "If the variable is inside a function and assigned later, Python raises `UnboundLocalError` (a subclass of NameError)."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "UnboundLocalError": {
        "simple_definition": "`UnboundLocalError` is a subclass of `NameError` that occurs when you reference a local variable inside a function before assigning a value to it. This happens because Python marks any variable assigned anywhere in a function as local.",
        "title": "Real-world: Modifying Counter Variables Inside Functions",
        "code": """# Real-world: Incrementing an external counter correctly
retry_count = 0

def bad_increment():
    try:
        # Python sees retry_count = ... below, so it treats it as LOCAL!
        # Reading it before assignment raises UnboundLocalError:
        retry_count += 1
    except UnboundLocalError as err:
        print(f"UnboundLocalError caught: {err}")

bad_increment()

# Correct way 1: Use 'global' keyword if mutating module-level variable
def good_increment():
    global retry_count
    retry_count += 1
    return retry_count

print("Clean increment:", good_increment())""",
        "gotchas": [
            "If a function contains `x = ...` anywhere in its body, `x` is local for the ENTIRE function scope.",
            "Use `global x` for module variables or `nonlocal x` for outer closures.",
            "Passing state as arguments and returning updated values is usually cleaner than using `global`."
        ],
        "inheritance": "NameError -> Exception -> BaseException"
    },

    "ImportError": {
        "simple_definition": "`ImportError` occurs when an `import` statement fails to import a module or a specific symbol from a module. Commonly caused by circular imports, missing packages, or renamed functions.",
        "title": "Real-world: Safe Fallback for Optional Accelerators",
        "code": """# Real-world: Graceful fallback to standard json if rapidjson is not installed
try:
    import ujson as fast_json
    print("Loaded high-performance ujson accelerator.")
except ImportError:
    import json as fast_json
    print("ImportError: ujson not installed, fell back to standard json.")

data = {"status": "ok", "latency_ms": 12}
print("Serialized payload:", fast_json.dumps(data))""",
        "gotchas": [
            "Circular imports (`a.py` imports `b.py` which imports `a.py`) are a frequent cause of unexpected ImportErrors.",
            "In Python 3.6+, missing top-level modules raise `ModuleNotFoundError`, which inherits from `ImportError`."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "ModuleNotFoundError": {
        "simple_definition": "`ModuleNotFoundError` is a subclass of `ImportError` raised when Python cannot locate the module file or package specified in an `import` statement within `sys.path`.",
        "title": "Real-world: Feature-Detection for Optional Dependencies",
        "code": """# Real-world: Optional pandas integration in a lightweight data utility
def load_dataset(file_path):
    try:
        import pandas as pd
        print("Using Pandas for high-speed DataFrame loading.")
        return pd.read_csv(file_path)
    except ModuleNotFoundError:
        import csv
        print("ModuleNotFoundError: Pandas not available. Using built-in csv module.")
        with open(file_path, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))""",
        "gotchas": [
            "Always verify your virtual environment (`venv`) is activated when running scripts.",
            "Ensure the module name matches the PyPI import name (e.g. `pip install pyyaml` -> `import yaml`)."
        ],
        "inheritance": "ImportError -> Exception -> BaseException"
    },

    "StopIteration": {
        "simple_definition": "`StopIteration` is raised by the built-in `next()` function to signal that an iterator has no further items. Python's `for` loops catch this exception automatically behind the scenes to terminate iteration.",
        "title": "Real-world: Consuming Generators & Manual Iterator Stepping",
        "code": """# Real-world: Manually consuming items from an iterator with next()
def number_stream():
    yield 10
    yield 20

stream = number_stream()

print("First item:", next(stream))
print("Second item:", next(stream))

# 1. Catching StopIteration explicitly
try:
    print(next(stream))
except StopIteration:
    print("StopIteration: The stream has ended.")

# 2. Idiomatic alternative: next() with a default value prevents the exception
item = next(stream, "END_OF_STREAM")
print("Safe next with default:", item)""",
        "gotchas": [
            "`for` loops automatically handle and suppress `StopIteration`.",
            "Calling `next(iterator, default)` allows providing a fallback without `try/except`.",
            "In Python 3.7+ (PEP 479), raising `StopIteration` inside a generator transforms into `RuntimeError`."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "RecursionError": {
        "simple_definition": "`RecursionError` occurs when a recursive function exceeds Python's maximum call stack depth (default is usually 1,000 frames). It prevents infinite recursion from crashing the host process with a C stack overflow.",
        "title": "Real-world: Recursive Tree Traversal with Depth Guards",
        "code": """# Real-world: Safe recursive navigation with depth guard
def traverse_org_chart(node, depth=0, max_depth=50):
    if depth > max_depth:
        raise RecursionError(f"Maximum organizational depth of {max_depth} exceeded!")
    
    print(f"{'  ' * depth}├── {node['name']}")
    for child in node.get("reports", []):
        traverse_org_chart(child, depth + 1, max_depth)

org = {
    "name": "CEO",
    "reports": [
        {"name": "VP Engineering", "reports": [{"name": "Lead Architect"}]},
        {"name": "VP Product"}
    ]
}

traverse_org_chart(org)""",
        "gotchas": [
            "Almost always caused by forgetting the base case in a recursive function.",
            "Check current limit with `import sys; sys.getrecursionlimit()` (default 1000).",
            "For deep trees or graphs, prefer an iterative loop with a stack or queue over recursion."
        ],
        "inheritance": "RuntimeError -> Exception -> BaseException"
    },

    "OverflowError": {
        "simple_definition": "`OverflowError` occurs when an arithmetic operation produces a numeric result that is too large to be represented by the underlying numeric type (such as floating-point numbers or math module functions).",
        "title": "Real-world: Guarding Exponential Math & Floating-Point Calculations",
        "code": """import math

# Real-world: Calculating compound interest or exponential growth
rates = [0.05, 0.5, 1000.0]

for r in rates:
    try:
        growth = math.exp(r)
        print(f"e^{r} = {growth:.4e}")
    except OverflowError as err:
        print(f"OverflowError: Value e^{r} exceeds 64-bit floating point capacity!")

# Note: Python standard integers have arbitrary precision and NEVER raise OverflowError!
huge_int = 10 ** 100
print(f"Huge int (10^100) length in digits: {len(str(huge_int))}")""",
        "gotchas": [
            "Python `int` has unlimited precision in Python 3 and will NOT raise OverflowError.",
            "`float` uses IEEE 754 double precision (up to ~1.79e+308), so values beyond that trigger OverflowError.",
            "`OverflowError` inherits from `ArithmeticError`."
        ],
        "inheritance": "ArithmeticError -> Exception -> BaseException"
    },

    "AssertionError": {
        "simple_definition": "`AssertionError` is raised when an `assert condition, message` statement evaluates to False. It is primarily used for debugging, internal consistency checks, and unit tests.",
        "title": "Real-world: Defending Data Invariants in Financial Transactions",
        "code": """# Real-world: Validating internal invariants before committing a ledger transaction
def transfer_funds(from_balance, to_balance, amount):
    assert amount > 0, "Transfer amount must be strictly positive."
    assert from_balance >= amount, f"Insufficient funds: {from_balance} < {amount}"
    
    new_from = from_balance - amount
    new_to = to_balance + amount
    
    # Invariant: Total system money must remain conserved
    assert (new_from + new_to) == (from_balance + to_balance), "Balance conservation invariant violated!"
    return new_from, new_to

try:
    transfer_funds(50, 200, 100)  # Attempting to transfer more than available
except AssertionError as err:
    print(f"AssertionError caught: {err}")""",
        "gotchas": [
            "Do NOT use `assert` for user input validation in production because running Python with `-O` (optimize) disables all asserts!",
            "Use standard `if not condition: raise ValueError(...)` for production business logic validation.",
            "Avoid writing `assert(condition, message)` with parentheses — in Python, that evaluates a non-empty tuple as True!"
        ],
        "inheritance": "Exception -> BaseException"
    },

    "NotImplementedError": {
        "simple_definition": "`NotImplementedError` is raised in abstract base classes, interface methods, or plugin contracts to signal that a derived child class is required to override and provide the implementation.",
        "title": "Real-world: Defining Extensible Payment Gateway Interfaces",
        "code": """# Real-world: Abstract payment provider interface
class PaymentGateway:
    def process_charge(self, amount_cents: int, token: str) -> bool:
        raise NotImplementedError("Subclasses of PaymentGateway must implement 'process_charge()'.")

class StripeGateway(PaymentGateway):
    def process_charge(self, amount_cents: int, token: str) -> bool:
        print(f"Charged ${amount_cents / 100:.2f} via Stripe token '{token}'.")
        return True

# Unimplemented gateway raises error clearly
dummy = PaymentGateway()
try:
    dummy.process_charge(5000, "tok_123")
except NotImplementedError as err:
    print(f"NotImplementedError caught: {err}")

# Subclassed gateway succeeds
stripe = StripeGateway()
stripe.process_charge(2500, "tok_stripe_abc")""",
        "gotchas": [
            "Do not confuse `NotImplementedError` (an exception class) with `NotImplemented` (a singleton object returned by dunder methods like `__eq__`).",
            "Consider using Python's `abc.ABC` and `@abc.abstractmethod` for formal abstract base classes."
        ],
        "inheritance": "RuntimeError -> Exception -> BaseException"
    },

    "RuntimeError": {
        "simple_definition": "`RuntimeError` is a general exception raised when an error is detected that doesn't fall into any other specific category. A famous example is modifying a dictionary or collection while iterating over it.",
        "title": "Real-world: Safe Collection Mutation During Iteration",
        "code": """# Real-world: Removing expired sessions from an active session store
active_sessions = {
    "sess_1": {"user": "alice", "expired": False},
    "sess_2": {"user": "bob", "expired": True},
    "sess_3": {"user": "carol", "expired": True}
}

# Modifying active_sessions directly during iteration raises RuntimeError:
try:
    for session_id, data in active_sessions.items():
        if data["expired"]:
            del active_sessions[session_id]
except RuntimeError as err:
    print(f"RuntimeError caught: {err}")

# Safe solution: Iterate over a snapshot list of keys:
for session_id in list(active_sessions.keys()):
    if active_sessions[session_id]["expired"]:
        del active_sessions[session_id]

print("Remaining active sessions:", list(active_sessions.keys()))""",
        "gotchas": [
            "`RuntimeError: dictionary changed size during iteration` is solved by wrapping keys in `list(dict.keys())`.",
            "Acts as the base class for `RecursionError` and `NotImplementedError`."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "TimeoutError": {
        "simple_definition": "`TimeoutError` occurs when an operation, such as an HTTP request, database query, or network socket read, exceeds its configured time limit without completing.",
        "title": "Real-world: Calling Remote APIs with Connection Timeouts",
        "code": """import socket

# Real-world: Setting a defensive socket timeout
def ping_service(host, port, timeout_sec=1.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout_sec)
    try:
        s.connect((host, port))
        print(f"Successfully reached {host}:{port}")
    except (TimeoutError, socket.timeout):
        print(f"TimeoutError: {host}:{port} did not respond within {timeout_sec}s.")
    finally:
        s.close()

# Attempt connection to non-routable address to demonstrate timeout
ping_service("10.255.255.1", 80, timeout_sec=0.5)""",
        "gotchas": [
            "In Python 3.10+, `socket.timeout` was made an alias of built-in `TimeoutError`.",
            "Always specify explicit timeouts in production network calls (`requests.get(url, timeout=5)`)."
        ],
        "inheritance": "OSError -> Exception -> BaseException"
    },

    "ConnectionError": {
        "simple_definition": "`ConnectionError` is the base class for network connection issues, including connection refused, connection reset, or broken pipes.",
        "title": "Real-world: Network Retry Logic with Exponential Backoff",
        "code": """# Real-world: Retrying connection to a database or message queue
def attempt_connection(max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            # Simulated network failure
            raise ConnectionError("Connection refused by database proxy.")
        except ConnectionError as err:
            print(f"Attempt {attempt}/{max_retries} failed: {err}")
            if attempt == max_retries:
                print("Max retries exhausted. Alerting on-call engineer.")

attempt_connection()""",
        "gotchas": [
            "`ConnectionError` is a subclass of `OSError`.",
            "Subclasses include `ConnectionRefusedError`, `ConnectionResetError`, `ConnectionAbortedError`, and `BrokenPipeError`."
        ],
        "inheritance": "OSError -> Exception -> BaseException"
    },

    "ConnectionRefusedError": {
        "simple_definition": "`ConnectionRefusedError` is a subclass of `ConnectionError` raised when a network connection attempt is rejected by the target host (usually because no server is listening on the requested port).",
        "title": "Real-world: Detecting Offline Microservices Safely",
        "code": """import socket

# Real-world: Health-checking a local microservice port
def check_service_health(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", port))
        print(f"Service on port {port} is healthy and running.")
    except ConnectionRefusedError:
        print(f"ConnectionRefusedError: Nothing is listening on port {port}. Service is offline.")
    finally:
        s.close()

check_service_health(65432)  # Typically closed port""",
        "gotchas": [
            "Corresponds to operating system errno 111 (ECONNREFUSED).",
            "Indicates the network route is valid, but the target port is closed or firewalled."
        ],
        "inheritance": "ConnectionError -> OSError -> Exception -> BaseException"
    },

    "EOFError": {
        "simple_definition": "`EOFError` (End Of File Error) occurs when built-in functions like `input()` or deserializers like `pickle.load()` hit the end of a file or stream without reading any expected data.",
        "title": "Real-world: Safe Interactive Terminal Input Loop",
        "code": """# Real-world: Reading commands from an interactive console loop
def console_loop():
    print("Welcome to CLI! (Press Ctrl+D or Ctrl+Z to exit)")
    commands = ["status", "deploy", "exit"]
    
    for cmd in commands:
        try:
            # Simulating input reading
            if cmd == "exit":
                raise EOFError("User sent EOF (Ctrl+D)")
            print(f"Executing: {cmd}")
        except EOFError:
            print("\\nEOFError caught: Gracefully shutting down CLI session.")
            break

console_loop()""",
        "gotchas": [
            "Pressing Ctrl+D (Unix) or Ctrl+Z then Enter (Windows) during `input()` triggers EOFError.",
            "Reading from an empty pipe in CLI tools triggers EOFError."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "KeyboardInterrupt": {
        "simple_definition": "`KeyboardInterrupt` occurs when the user presses the interrupt key (typically Ctrl+C or Delete) in the terminal to stop execution. Crucially, it inherits directly from `BaseException`, not `Exception`, so `except Exception:` will not accidentally swallow it.",
        "title": "Real-world: Graceful Service Shutdown on Ctrl+C",
        "code": """import time

# Real-world: Worker loop with graceful cleanup on Ctrl+C
def background_worker():
    print("Worker started. Simulating task execution...")
    try:
        # Simulate worker cycle
        for step in range(3):
            time.sleep(0.01)
        # Simulate Ctrl+C
        raise KeyboardInterrupt()
    except KeyboardInterrupt:
        print("\\nKeyboardInterrupt detected!")
        print("Cleaning up open file handles and releasing database locks...")
        print("Worker stopped safely.")

background_worker()""",
        "gotchas": [
            "Never use `except:` (bare except) or `except BaseException: pass` — that traps KeyboardInterrupt and makes scripts impossible to stop with Ctrl+C!",
            "Always catch specific exceptions (`except Exception:`) so KeyboardInterrupt propagates cleanly."
        ],
        "inheritance": "BaseException"
    },

    "MemoryError": {
        "simple_definition": "`MemoryError` occurs when an operation runs out of available memory (RAM). When this happens, Python fails to allocate the requested buffer or object.",
        "title": "Real-world: Chunked File Processing to Prevent Memory Exhaustion",
        "code": """# Real-world: Processing large log files in chunks rather than loading all into RAM
def process_large_file_safely(file_lines):
    # BAD: line_list = file.read().splitlines()  <-- Can trigger MemoryError on multi-GB files!
    
    # GOOD: Stream chunk-by-chunk using a generator
    processed_count = 0
    for line in file_lines:
        processed_count += 1
    return processed_count

lines_generator = (f"Log line {i}" for i in range(1000))
print("Processed lines:", process_large_file_safely(lines_generator))""",
        "gotchas": [
            "Use generators `(x for x in ...)` instead of list comprehensions `[x for x in ...]` for massive datasets.",
            "Use `pd.read_csv(..., chunksize=10000)` or standard `for line in f:` to stream files."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "SystemExit": {
        "simple_definition": "`SystemExit` is raised by `sys.exit()` to terminate the Python interpreter. Like `KeyboardInterrupt`, it inherits from `BaseException` so that cleanup handlers (`finally` blocks) run, but normal application code does not accidentally trap it.",
        "title": "Real-world: Exiting CLI Tools with Status Codes",
        "code": """import sys

# Real-world: CLI utility validation and exit codes
def run_cli_validation(config_loaded):
    try:
        if not config_loaded:
            print("Fatal: Configuration failed to load.", file=sys.stderr)
            # Exit code 1 indicates failure to shell
            sys.exit(1)
    except SystemExit as err:
        print(f"SystemExit intercepted: Code {err.code}. Running cleanup...")

run_cli_validation(False)""",
        "gotchas": [
            "`sys.exit(0)` means successful exit; any non-zero integer (like 1 or 2) indicates an error.",
            "`finally` blocks are still executed when `SystemExit` is raised.",
            "Inherits directly from `BaseException`."
        ],
        "inheritance": "BaseException"
    },

    "SyntaxError": {
        "simple_definition": "`SyntaxError` occurs when Python's parser encounters source code that violates Python grammatical rules (such as missing colons, unmatched parentheses, or reserved keywords used as variable names).",
        "title": "Real-world: Safely Compiling & Validating User-Submitted Code",
        "code": """# Real-world: Validating user formula syntax before dynamic execution
user_expressions = [
    "2 + 2",
    "total * 1.05",
    "def (bad syntax here"
]

for expr in user_expressions:
    try:
        compile(expr, "<string>", "eval")
        print(f"Syntax OK: {expr}")
    except SyntaxError as err:
        print(f"SyntaxError in '{expr}': {err.msg} at line {err.lineno}")""",
        "gotchas": [
            "SyntaxError occurs during the compilation/parsing phase before the code even begins executing.",
            "Common causes: missing colon `:` after `if`/`for`/`def`, unclosed quotes, or unmatched parentheses `)`."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "IndentationError": {
        "simple_definition": "`IndentationError` is a subclass of `SyntaxError` that occurs when code blocks are not indented uniformly or correctly according to Python's whitespace indentation rules.",
        "title": "Real-world: Understanding Indentation Structure",
        "code": """# Python relies on strict, consistent indentation to define code blocks
# Example of correct 4-space indentation:
def calculate_tax(income):
    if income > 50000:
        rate = 0.20
    else:
        rate = 0.10
    return income * rate

print("Tax on $60,000:", calculate_tax(60000))""",
        "gotchas": [
            "PEP 8 recommends 4 spaces per indentation level.",
            "Mixing tabs and spaces in the same file raises `TabError` (a subclass of `IndentationError`)."
        ],
        "inheritance": "SyntaxError -> Exception -> BaseException"
    },

    "TabError": {
        "simple_definition": "`TabError` is a subclass of `IndentationError` raised when a code block contains an inconsistent mixture of tabs and spaces for indentation.",
        "title": "Real-world: Enforcing Consistent Spaces in Codebases",
        "code": """# Real-world: Python strictly forbids mixing tabs and spaces in the same block
# Configure your code editor to 'Insert Spaces' instead of Tab characters
print("All lines in this file consistently use 4 spaces for indentation.")""",
        "gotchas": [
            "Configure your IDE (VS Code, PyCharm) to automatically convert Tabs to 4 spaces.",
            "Run linters like `flake8` or formatters like `black` / `ruff` to clean up indentation automatically."
        ],
        "inheritance": "IndentationError -> SyntaxError -> Exception -> BaseException"
    },

    "UnicodeDecodeError": {
        "simple_definition": "`UnicodeDecodeError` occurs when attempting to decode a sequence of raw bytes into a Python string using a text encoding (like UTF-8) that does not recognize those byte values.",
        "title": "Real-world: Reading Legacy Encoded Files Safely",
        "code": """# Real-world: Reading files with potential non-UTF-8 characters
raw_bytes = b"Hello, world! Special: \xe9 \xff"

# 1. Specifying errors='replace' to prevent crashing on invalid bytes
decoded_safe = raw_bytes.decode("utf-8", errors="replace")
print("Safe decoded with replacement char ():", decoded_safe)

# 2. Specifying errors='ignore' to omit malformed bytes
decoded_clean = raw_bytes.decode("utf-8", errors="ignore")
print("Decoded with ignored bytes:", decoded_clean)""",
        "gotchas": [
            "Always specify `encoding='utf-8'` explicitly when opening files (`open(..., encoding='utf-8')`).",
            "Use `errors='replace'` or `errors='ignore'` when reading unknown or legacy external data."
        ],
        "inheritance": "UnicodeError -> ValueError -> Exception -> BaseException"
    },

    "UnicodeEncodeError": {
        "simple_definition": "`UnicodeEncodeError` occurs when attempting to encode a Python string containing Unicode characters into a restricted byte encoding (such as ASCII) that cannot represent those characters.",
        "title": "Real-world: Exporting Unicode Text to Restrictive Encodings",
        "code": """# Real-world: Exporting text with emoji or international accents to ASCII systems
message = "Order total: 50€ 🐍"

try:
    # ASCII only supports characters 0-127
    ascii_bytes = message.encode("ascii")
except UnicodeEncodeError as err:
    print(f"UnicodeEncodeError caught: {err.reason}")
    # Handle with XML character references or replacement
    ascii_safe = message.encode("ascii", errors="xmlcharrefreplace").decode("ascii")
    print("Safe ASCII fallback:", ascii_safe)""",
        "gotchas": [
            "Default to UTF-8 for all modern storage and network transfer.",
            "When interfacing with legacy ASCII printers or terminals, use `errors='namereplace'` or `'replace'`."
        ],
        "inheritance": "UnicodeError -> ValueError -> Exception -> BaseException"
    },

    "ExceptionGroup": {
        "simple_definition": "`ExceptionGroup` was introduced in Python 3.11 (PEP 654) to bundle and raise multiple independent exceptions simultaneously. It is predominantly used with asyncio task groups and parallel thread executions.",
        "title": "Real-world: Handling Multiple Parallel Task Failures with except*",
        "code": """# Real-world: Simulating multiple concurrent task failures
# (Available in Python 3.11+)
eg = ExceptionGroup("Background jobs failed", [
    ValueError("Invalid job payload"),
    FileNotFoundError("Missing asset file"),
    ValueError("Missing API key")
])

# Inspecting grouped exceptions
print(f"Exception group: {eg.message}")
print(f"Contained exceptions ({len(eg.exceptions)}):")
for exc in eg.exceptions:
    print(f" - {type(exc).__name__}: {exc}")""",
        "gotchas": [
            "Handled using the `except*` (except-star) syntax in Python 3.11+.",
            "Useful in `asyncio.TaskGroup` where multiple coroutines can fail concurrently."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "LookupError": {
        "simple_definition": "`LookupError` is the base class for exceptions raised when a key or index used on a mapping or sequence is invalid. Its direct subclasses are `IndexError` and `KeyError`.",
        "title": "Real-world: Universal Lookup Handler for Dicts and Lists",
        "code": """# Real-world: Generic lookup helper that handles both lists and dicts
def safe_lookup(container, key_or_index, default=None):
    try:
        return container[key_or_index]
    except LookupError:  # Catches BOTH IndexError AND KeyError!
        return default

my_list = ["apple", "banana"]
my_dict = {"name": "Charlie"}

print("List safe index 5:", safe_lookup(my_list, 5, "default_fruit"))
print("Dict safe key 'age':", safe_lookup(my_dict, "age", 25))""",
        "gotchas": [
            "Catching `LookupError` is an elegant way to handle missing keys in dicts and missing indices in lists with a single except clause."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "ArithmeticError": {
        "simple_definition": "`ArithmeticError` is the base class for all built-in exceptions that are raised for various arithmetic errors. Its subclasses are `ZeroDivisionError`, `OverflowError`, and `FloatingPointError`.",
        "title": "Real-world: Catching Any Mathematical Fault in Calculations",
        "code": """import math

# Real-world: Robust mathematical evaluator catching any math failure
def safe_calculate(func, *args):
    try:
        return func(*args)
    except ArithmeticError as err:  # Catches ZeroDivisionError and OverflowError!
        print(f"Arithmetic fault: {type(err).__name__} -> {err}")
        return None

print("Valid div:", safe_calculate(lambda a, b: a / b, 10, 2))
print("Zero div:", safe_calculate(lambda a, b: a / b, 10, 0))
print("Overflow:", safe_calculate(lambda x: math.exp(x), 1000.0))""",
        "gotchas": [
            "Use `except ArithmeticError:` when evaluating dynamic formulas to catch both division by zero and exponential overflow together."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "OSError": {
        "simple_definition": "`OSError` is the base exception class for system-related errors, such as file not found, permission denied, disk full, and socket connection errors. It provides access to the underlying OS `errno` code.",
        "title": "Real-world: Catching Low-Level Operating System Failures",
        "code": """import os

# Real-world: Attempting low-level OS operations
try:
    # Attempting to query non-existent path
    os.stat("non_existent_system_file.dat")
except OSError as err:
    print(f"OSError caught: {err}")
    print(f"Error Number (errno): {err.errno}")
    print(f"Error Message: {err.strerror}")""",
        "gotchas": [
            "In Python 3.3+, `IOError` and `EnvironmentError` became aliases of `OSError`.",
            "`FileNotFoundError`, `PermissionError`, `ConnectionError`, `TimeoutError` all inherit from `OSError`."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "BufferError": {
        "simple_definition": "`BufferError` is raised when a buffer-related operation cannot be performed, such as attempting to modify a bytearray while an active `memoryview` is referencing it.",
        "title": "Real-world: Safe High-Performance Memory Buffer Views",
        "code": """# Real-world: Working with zero-copy byte buffers
raw_data = bytearray(b"IMAGE_PAYLOAD_CHUNK")
view = memoryview(raw_data)

try:
    # Trying to resize the bytearray while view is open raises BufferError:
    raw_data.extend(b"_EXTRA")
except BufferError as err:
    print(f"BufferError caught: {err}")
    # Properly release memoryview before resizing
    view.release()
    raw_data.extend(b"_EXTRA")
    print("Buffer successfully resized after releasing view:", bytes(raw_data))""",
        "gotchas": [
            "Always call `.release()` on `memoryview` objects when finished with underlying buffer data."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "ReferenceError": {
        "simple_definition": "`ReferenceError` is raised when a weak reference proxy object (`weakref.proxy`) is used to access an attribute of the referent after it has already been garbage collected.",
        "title": "Real-world: Weak Reference Caching to Prevent Circular Memory Leaks",
        "code": """import weakref

class HeavyResource:
    def __init__(self, name):
        self.name = name

obj = HeavyResource("DatabasePool")
# Create a weak proxy
proxy = weakref.proxy(obj)
print("Proxy access while alive:", proxy.name)

# Delete referent
del obj

try:
    print("Access after garbage collection:", proxy.name)
except ReferenceError as err:
    print(f"ReferenceError caught: {err}")""",
        "gotchas": [
            "Use standard `weakref.ref(obj)` which returns `None` when collected, rather than `weakref.proxy(obj)` which raises ReferenceError."
        ],
        "inheritance": "Exception -> BaseException"
    },

    "GeneratorExit": {
        "simple_definition": "`GeneratorExit` is raised inside a generator when the generator's `close()` method is called. It inherits directly from `BaseException` to ensure generators terminate cleanly.",
        "title": "Real-world: Cleaning Up Generator Resources with close()",
        "code": """# Real-world: Resource-tracking generator that closes cleanly
def resource_stream():
    print("Opening database cursor...")
    try:
        while True:
            yield "data_batch"
    except GeneratorExit:
        print("GeneratorExit: Closing database cursor safely.")

gen = resource_stream()
print("Received:", next(gen))
# Explicitly closing generator triggers GeneratorExit
gen.close()""",
        "gotchas": [
            "Do NOT yield any more values inside `except GeneratorExit:`, otherwise Python raises a `RuntimeError`."
        ],
        "inheritance": "BaseException"
    },

    "BaseException": {
        "simple_definition": "`BaseException` is the common base class of ALL built-in Python exceptions. It is designed to be subclassed only by system-exiting exceptions (`SystemExit`, `KeyboardInterrupt`, `GeneratorExit`) and `Exception`.",
        "title": "Real-world: Correct Exception Hierarchy & Catching Best Practices",
        "code": """# Real-world best practice:
# ALWAYS catch 'Exception', NOT 'BaseException', to avoid blocking Ctrl+C:
try:
    # Application logic
    total = 100 / 2
except Exception as err:
    # Catches normal runtime errors
    print("Application error:", err)
except BaseException:
    # Lets system exits and Ctrl+C pass cleanly or logs fatal termination
    print("Fatal shutdown signal received.")
    raise""",
        "gotchas": [
            "Never use `except BaseException: pass` because it makes the program impossible to kill via Ctrl+C or `sys.exit()`.",
            "All custom user exceptions must inherit from `Exception`, never directly from `BaseException`."
        ],
        "inheritance": "object"
    },

    "Exception": {
        "simple_definition": "`Exception` is the base class for all non-system-exiting exceptions. All user-defined and standard library exceptions should inherit from this class.",
        "title": "Real-world: Creating Custom Application Exceptions",
        "code": """# Real-world: Defining a domain-specific custom exception
class InsufficientFundsError(Exception):
    \"\"\"Raised when an account balance is inadequate for a withdrawal.\"\"\"
    def __init__(self, balance, amount):
        super().__init__(f"Attempted to withdraw ${amount:.2f} with only ${balance:.2f} available.")
        self.balance = balance
        self.amount = amount

try:
    raise InsufficientFundsError(14.50, 50.00)
except InsufficientFundsError as err:
    print(f"Domain error caught: {err}")
    print(f"Current balance: ${err.balance:.2f}")""",
        "gotchas": [
            "Always inherit from `Exception` when creating custom application error classes.",
            "Catching `except Exception as e:` will catch virtually all normal runtime errors while preserving Ctrl+C."
        ],
        "inheritance": "BaseException"
    },

    "BrokenPipeError": {
        "simple_definition": "`BrokenPipeError` occurs when trying to write data to a pipe, socket, or process output stream where the reading process has already terminated or closed its end.",
        "title": "Real-world: Graceful Handling of CLI Pager (head/grep) Closures",
        "code": """import sys

# Real-world: Outputting data to a pipe like "python script.py | head -n 5"
try:
    for i in range(100):
        # If receiver closes early, print() triggers BrokenPipeError
        if i >= 5:
            raise BrokenPipeError("Broken pipe: downstream reader closed.")
        print(f"Streaming data line {i}")
except BrokenPipeError:
    # Python convention: redirect stderr and exit cleanly with code 0
    sys.stderr.close()
    print("Downstream consumer exited early. Clean exit.")""",
        "gotchas": [
            "Very common in Unix command line pipelines when piping output into utilities like `head` or `grep -q`.",
            "Subclass of `ConnectionError` and `OSError` (errno 32: EPIPE)."
        ],
        "inheritance": "ConnectionError -> OSError -> Exception -> BaseException"
    },
    "ConnectionResetError": {
        "simple_definition": "`ConnectionResetError` occurs when an existing network connection is abruptly closed or forcibly reset by the remote peer (e.g. server crash or TCP RST packet).",
        "title": "Real-world: Handling Sudden Peer Disconnections",
        "code": """import socket

# Real-world: Handling sudden reset from an upstream WebSocket or HTTP server
try:
    raise ConnectionResetError("Connection forcibly closed by the remote host.")
except ConnectionResetError as err:
    print(f"ConnectionResetError caught: {err}")
    print("Action: Attempting automatic reconnect with backoff...")""",
        "gotchas": [
            "Corresponds to operating system errno 104 (ECONNRESET) on Linux, WSAECONNRESET on Windows.",
            "Often indicates server restarts, timeouts, or NAT router table expiration."
        ],
        "inheritance": "ConnectionError -> OSError -> Exception -> BaseException"
    },
    "ConnectionAbortedError": {
        "simple_definition": "`ConnectionAbortedError` occurs when a network connection that was established or in progress is terminated locally by the operating system or application network layer.",
        "title": "Real-world: Handling Local Connection Abortions",
        "code": """# Real-world: Detecting local connection abortions
try:
    raise ConnectionAbortedError("Software caused connection abort.")
except ConnectionAbortedError as err:
    print(f"ConnectionAbortedError caught: {err}")""",
        "gotchas": [
            "Corresponds to operating system errno 103 (ECONNABORTED).",
            "Happens when the local host aborts the socket before data transfer finishes."
        ],
        "inheritance": "ConnectionError -> OSError -> Exception -> BaseException"
    },
    "IsADirectoryError": {
        "simple_definition": "`IsADirectoryError` occurs when a file-specific operation (like `open(path, \"r\")`) is attempted on a path that is actually a directory.",
        "title": "Real-world: Validating File Paths vs Directories",
        "code": """from pathlib import Path

# Real-world: Checking path type before reading
path = Path(".")  # Current folder

try:
    if path.is_dir():
        print(f"\"{path}\" is a directory, not a regular file.")
    else:
        with open(path, "r") as f:
            content = f.read()
except IsADirectoryError:
    print(f"IsADirectoryError: Cannot read \"{path}\" as a text file.")""",
        "gotchas": [
            "Use `path.is_file()` or `path.is_dir()` with `pathlib.Path` to verify path types before opening.",
            "Corresponds to errno 21 (EISDIR)."
        ],
        "inheritance": "OSError -> Exception -> BaseException"
    },
    "NotADirectoryError": {
        "simple_definition": "`NotADirectoryError` occurs when a directory-specific operation (like `os.listdir()`) is requested on a path that is a regular file rather than a directory.",
        "title": "Real-world: Guarding Directory Listings",
        "code": """import os
from pathlib import Path

file_path = Path("sample.txt")
file_path.write_text("Hello")

try:
    os.listdir(file_path)
except NotADirectoryError as err:
    print(f"NotADirectoryError: \"{file_path}\" is a file, not a directory.")""",
        "gotchas": [
            "Always check `Path(p).is_dir()` before calling directory operations like `iterdir()` or `os.listdir()`.",
            "Corresponds to errno 20 (ENOTDIR)."
        ],
        "inheritance": "OSError -> Exception -> BaseException"
    },
    "InterruptedError": {
        "simple_definition": "`InterruptedError` occurs when a system call is interrupted by an incoming operating system signal (errno 4: EINTR). In Python 3.5+ (PEP 475), interrupted system calls are automatically retried by the interpreter.",
        "title": "Real-world: Interrupted System Call Awareness",
        "code": """# Python 3.5+ automatically restarts system calls interrupted by signals (PEP 475)
try:
    # Modern Python handles EINTR under the hood
    pass
except InterruptedError:
    print("System call was interrupted by a signal.")""",
        "gotchas": [
            "Since PEP 475, Python automatically retries system calls that fail with EINTR, so this error is rarely seen in modern Python."
        ],
        "inheritance": "OSError -> Exception -> BaseException"
    },
    "ProcessLookupError": {
        "simple_definition": "`ProcessLookupError` occurs when an operation is performed on a process ID (PID) that does not exist or has already terminated.",
        "title": "Real-world: Checking If Background Process Is Still Alive",
        "code": """import os

# Real-world: Checking if a PID is alive using signal 0
pid_to_check = 999999

try:
    # Signal 0 performs error checking without actually killing the process
    os.kill(pid_to_check, 0)
    print(f"Process {pid_to_check} is running.")
except ProcessLookupError:
    print(f"ProcessLookupError: Process {pid_to_check} does not exist.")""",
        "gotchas": [
            "Use `os.kill(pid, 0)` inside try/except to test if a PID is alive.",
            "Corresponds to errno 3 (ESRCH)."
        ],
        "inheritance": "OSError -> Exception -> BaseException"
    },
    "BlockingIOError": {
        "simple_definition": "`BlockingIOError` occurs when an operation on a non-blocking object (such as a non-blocking socket) would block the calling thread.",
        "title": "Real-world: Working with Non-Blocking Asynchronous Sockets",
        "code": """import socket

# Real-world: Setting up non-blocking socket reads
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(False)

try:
    # Reading immediately when no data is ready raises BlockingIOError
    data = s.recv(1024)
except BlockingIOError:
    print("BlockingIOError: No data available right now, socket would block.")
    print("Waiting for I/O readiness via select / asyncio...")
finally:
    s.close()""",
        "gotchas": [
            "This is normal behavior for non-blocking I/O; frameworks like `asyncio` or `selectors` wait until data is ready before reading.",
            "Corresponds to errno EAGAIN, EALREADY, EWOULDBLOCK, and EINPROGRESS."
        ],
        "inheritance": "OSError -> Exception -> BaseException"
    },
    "ChildProcessError": {
        "simple_definition": "`ChildProcessError` occurs when an operation on a child process fails, such as calling `os.waitpid()` on a process that is not a child of the current process.",
        "title": "Real-world: Monitoring Subprocesses with Safe Waits",
        "code": """import os

try:
    # Attempting to wait on arbitrary PID
    os.waitpid(999999, 0)
except ChildProcessError:
    print("ChildProcessError: PID is not a child of the current process.")""",
        "gotchas": [
            "Use the high-level `subprocess` module (`subprocess.run`, `subprocess.Popen`) instead of raw `os.fork` and `os.waitpid`.",
            "Corresponds to errno 10 (ECHILD)."
        ],
        "inheritance": "OSError -> Exception -> BaseException"
    },
    "EnvironmentError": {
        "simple_definition": "`EnvironmentError` is the historical base class for exceptions occurring outside the Python system (like file or OS errors). In modern Python 3, it is an exact alias of `OSError`.",
        "title": "Real-world: Legacy EnvironmentError Alias",
        "code": """# EnvironmentError is identical to OSError in Python 3
print("Is EnvironmentError the same as OSError?", EnvironmentError is OSError)

try:
    open("missing_file.xyz", "r")
except EnvironmentError as err:
    print("Caught via legacy EnvironmentError alias:", err)""",
        "gotchas": [
            "In Python 3.3+, `EnvironmentError` and `IOError` were merged into `OSError`. Use `OSError` in all new code."
        ],
        "inheritance": "OSError (alias)"
    },
    "IOError": {
        "simple_definition": "`IOError` (Input/Output Error) is the historical exception raised when an I/O operation (such as file reading or writing) fails. In Python 3.3+, it was merged into and is an alias for `OSError`.",
        "title": "Real-world: Catching Input/Output Failures",
        "code": """# IOError is an alias for OSError in Python 3
print("Is IOError the same as OSError?", IOError is OSError)

try:
    with open("non_existent_document.txt", "r") as f:
        data = f.read()
except IOError as err:
    print(f"IOError caught: {err}")""",
        "gotchas": [
            "Use `OSError` in modern Python 3 code for forward compatibility."
        ],
        "inheritance": "OSError (alias)"
    },
    "UnicodeError": {
        "simple_definition": "`UnicodeError` is the base class for exceptions that occur when encoding or decoding Unicode strings. It inherits from `ValueError`.",
        "title": "Real-world: Catching Any Unicode Encoding or Decoding Problem",
        "code": """# Real-world: Generic Unicode handler catching both encode and decode issues
def safe_transcode(byte_data, from_enc="utf-8", to_enc="ascii"):
    try:
        text = byte_data.decode(from_enc)
        return text.encode(to_enc)
    except UnicodeError as err:  # Catches UnicodeDecodeError AND UnicodeEncodeError!
        print(f"Unicode error: {err}")
        return None

print("Result:", safe_transcode(b"Hello \xff"))""",
        "gotchas": [
            "`UnicodeError` subclasses: `UnicodeDecodeError`, `UnicodeEncodeError`, and `UnicodeTranslateError`."
        ],
        "inheritance": "ValueError -> Exception -> BaseException"
    },
    "UnicodeTranslateError": {
        "simple_definition": "`UnicodeTranslateError` occurs during string translation (`str.translate()`) when a character cannot be mapped in the translation table.",
        "title": "Real-world: Safe Character Translation with str.translate",
        "code": """# Real-world: Sanitizing text with custom character translation tables
trans_map = str.maketrans({"<": "&lt;", ">": "&gt;", "&": "&amp;"})
safe_html = "User input: <b>Hello & welcome</b>".translate(trans_map)
print("Sanitized HTML:", safe_html)""",
        "gotchas": [
            "Inherits from `UnicodeError`."
        ],
        "inheritance": "UnicodeError -> ValueError -> Exception -> BaseException"
    },
    "FloatingPointError": {
        "simple_definition": "`FloatingPointError` is raised when a floating-point operation fails. In standard Python builds, floating-point IEEE 754 exceptions produce `inf` or `nan` instead of raising this error unless explicitly configured via the `fpectl` module.",
        "title": "Real-world: Detecting NaN and Infinity in Float Calculations",
        "code": """import math

# In standard Python, floating overflow creates inf rather than FloatingPointError:
val = 1e300 * 1e300
print("Extreme float result:", val)
print("Is infinite?", math.isinf(val))

# Detecting invalid numbers safely with math.isnan and math.isinf
if math.isinf(val) or math.isnan(val):
    print("Calculation produced non-finite number, adjusting...")""",
        "gotchas": [
            "Standard Python rarely raises `FloatingPointError` because IEEE 754 non-trapping arithmetic is standard.",
            "Subclass of `ArithmeticError`."
        ],
        "inheritance": "ArithmeticError -> Exception -> BaseException"
    },
    "SystemError": {
        "simple_definition": "`SystemError` occurs when the Python interpreter finds an internal inconsistency or fatal logic error, usually caused by a buggy C extension module or internal CPython failure.",
        "title": "Real-world: Diagnosing Internal C Extension Inconsistencies",
        "code": """# SystemError indicates an internal interpreter fault, usually from a C extension
print("SystemError should never occur in pure, valid Python code.")
print("If you encounter it, check C-extensions, Cython, or report a bug to CPython.")""",
        "gotchas": [
            "If seen, it is almost certainly a bug in a C extension (e.g. returning NULL without setting an exception).",
            "Inherits directly from `Exception`."
        ],
        "inheritance": "Exception -> BaseException"
    },
    "StopAsyncIteration": {
        "simple_definition": "`StopAsyncIteration` is the asynchronous counterpart to `StopIteration`. It must be raised by the `__anext__()` method of an asynchronous iterator to signal the end of an async sequence in `async for` loops.",
        "title": "Real-world: Building Custom Asynchronous Streams",
        "code": """import asyncio

# Real-world: Async generator simulating real-time metric stream
class MetricStream:
    def __init__(self, limit=3):
        self.count = 0
        self.limit = limit

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.count >= self.limit:
            raise StopAsyncIteration  # Signals end of async loop!
        self.count += 1
        await asyncio.sleep(0.01)
        return f"Metric batch #{self.count}"

async def run():
    async for item in MetricStream(3):
        print("Received:", item)

asyncio.run(run())""",
        "gotchas": [
            "Used exclusively with asynchronous iterators (`async for`) and `anext()`.",
            "Inherits from `Exception`."
        ],
        "inheritance": "Exception -> BaseException"
    },
    "BaseExceptionGroup": {
        "simple_definition": "`BaseExceptionGroup` was introduced in Python 3.11 (PEP 654) as the base class for exception groups that can contain `BaseException` instances (such as `KeyboardInterrupt`).",
        "title": "Real-world: Grouping System-Level Exceptions in Concurrency",
        "code": """# Python 3.11+ BaseExceptionGroup holds both regular Exceptions and BaseExceptions
beg = BaseExceptionGroup("System tasks terminated", [
    KeyboardInterrupt(),
    ValueError("Invalid parameter")
])

print(f"Group: {beg.message}")
print(f"Exceptions count: {len(beg.exceptions)}")""",
        "gotchas": [
            "Inherits directly from `BaseException` (not `Exception`).",
            "`ExceptionGroup` inherits from both `BaseExceptionGroup` and `Exception`."
        ],
        "inheritance": "BaseException"
    },
    "Warning": {
        "simple_definition": "`Warning` is the base class for all warning categories in Python. Unlike exceptions, warnings inform developers about conditions (like deprecations) without halting execution.",
        "title": "Real-world: Emitting and Filtering Python Warnings",
        "code": """import warnings

# Real-world: Emitting a warning for deprecated API usage
def old_calculate(x):
    warnings.warn(
        "old_calculate() is deprecated and will be removed in v3.0. Use new_calculate() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return x * 2

old_calculate(5)
print("Execution continued uninterrupted despite warning.")""",
        "gotchas": [
            "Warnings do not stop program execution unless converted to errors via `warnings.filterwarnings('error')`.",
            "Inherits from `Exception`."
        ],
        "inheritance": "Exception -> BaseException"
    },
    "UserWarning": {
        "simple_definition": "`UserWarning` is the standard warning category for warnings triggered by user application code (as opposed to Python language or library deprecations).",
        "title": "Real-world: Informing Users of Non-Fatal Sub-Optimal Conditions",
        "code": """import warnings

def import_csv_data(filepath, max_rows=10000):
    if max_rows > 5000:
        warnings.warn("Large import size may take several seconds.", UserWarning)
    print(f"Importing up to {max_rows} rows from {filepath}...")

import_csv_data("sales.csv", max_rows=8000)""",
        "gotchas": [
            "Default category for `warnings.warn()` when no category argument is passed."
        ],
        "inheritance": "Warning -> Exception -> BaseException"
    },
    "DeprecationWarning": {
        "simple_definition": "`DeprecationWarning` indicates that a feature, function, or parameter is deprecated and will be removed in a future version. Filtered by default in production Python to keep logs clean for end users.",
        "title": "Real-world: Deprecating Legacy Functions Safely",
        "code": """import warnings

def fetch_data_legacy(endpoint):
    warnings.warn(
        "fetch_data_legacy() is deprecated; migrate to api_client.get().",
        DeprecationWarning,
        stacklevel=2
    )
    return {"status": 200}

fetch_data_legacy("/users")""",
        "gotchas": [
            "Ignored by default in `__main__` modules in Python 3.7+ unless explicitly enabled with `-Wd`."
        ],
        "inheritance": "Warning -> Exception -> BaseException"
    },
    "PendingDeprecationWarning": {
        "simple_definition": "`PendingDeprecationWarning` indicates that a feature will be deprecated in the future, but is not yet formally deprecated in the current release.",
        "title": "Real-world: Advance Notice for Long-Term Deprecations",
        "code": """import warnings

warnings.warn("This feature will enter formal deprecation in Python 3.15.", PendingDeprecationWarning)
print("Pending deprecation emitted.")""",
        "gotchas": [
            "Always ignored by default in standard Python execution."
        ],
        "inheritance": "Warning -> Exception -> BaseException"
    },
    "SyntaxWarning": {
        "simple_definition": "`SyntaxWarning` indicates dubious or suspicious syntax in source code, such as using `is` to compare literals (`x is 1000`) instead of `==`.",
        "title": "Real-world: Identifying Suspicious Syntax Usage",
        "code": """import warnings

# Dubious syntax like 'x is 5' triggers SyntaxWarning in modern Python:
warnings.warn("Using 'is' with a literal produces SyntaxWarning. Use '==' instead.", SyntaxWarning)""",
        "gotchas": [
            "In Python 3.8+, comparisons like `x is 1000` or `s is 'literal'` emit a SyntaxWarning."
        ],
        "inheritance": "Warning -> Exception -> BaseException"
    },
    "RuntimeWarning": {
        "simple_definition": "`RuntimeWarning` indicates dubious runtime behavior that is not a fatal error, such as forgetting to await an asynchronous coroutine.",
        "title": "Real-world: Catching Unawaited Coroutines & Dubious Runtime State",
        "code": """import warnings

warnings.warn("Coroutine 'fetch_feed()' was never awaited!", RuntimeWarning)
print("RuntimeWarning emitted.")""",
        "gotchas": [
            "Famously emitted when an async function is called without `await`."
        ],
        "inheritance": "Warning -> Exception -> BaseException"
    },
    "FutureWarning": {
        "simple_definition": "`FutureWarning` warns developers about semantics that will change in future versions, targeted specifically at users of libraries rather than framework developers.",
        "title": "Real-world: Notifying Library Users of Semantic Changes",
        "code": """import warnings

warnings.warn("In version 2.0, default sorting order will change from asc to desc.", FutureWarning)
print("FutureWarning emitted.")""",
        "gotchas": [
            "Unlike `DeprecationWarning`, `FutureWarning` is shown by default to ensure end-users notice breaking API shifts."
        ],
        "inheritance": "Warning -> Exception -> BaseException"
    },
    "ImportWarning": {
        "simple_definition": "`ImportWarning` indicates potential issues during package or module importing.",
        "title": "Real-world: Emitting Import Resolution Warnings",
        "code": """import warnings

warnings.warn("Module import fell back to legacy compatibility path.", ImportWarning)""",
        "gotchas": [
            "Ignored by default."
        ],
        "inheritance": "Warning -> Exception -> BaseException"
    },
    "UnicodeWarning": {
        "simple_definition": "`UnicodeWarning` warns about subtle Unicode-related issues, such as converting byte strings to Unicode using non-standard or ambiguous conventions.",
        "title": "Real-world: Warning on Ambiguous Unicode Conversion",
        "code": """import warnings

warnings.warn("Ambiguous string conversion without explicit encoding parameter.", UnicodeWarning)""",
        "gotchas": [
            "Subclass of `Warning`."
        ],
        "inheritance": "Warning -> Exception -> BaseException"
    },
    "BytesWarning": {
        "simple_definition": "`BytesWarning` warns about dubious operations mixing `bytes` and `str` (such as comparing a bytes object with a string), emitted when Python is run with `-b` or `-bb` flag.",
        "title": "Real-world: Guarding Against Accidental Bytes/String Mixing",
        "code": """import warnings

# In Python 3, b'data' == 'data' evaluates to False silently unless -b flag is set
b_data = b"token_123"
s_data = "token_123"

if b_data != s_data:
    print("Note: In Python 3, bytes and strings are NEVER equal (b'abc' != 'abc').")
    warnings.warn("Comparing bytes and str without decoding.", BytesWarning)""",
        "gotchas": [
            "Run Python with `python -b` to see BytesWarnings, or `python -bb` to turn them into errors."
        ],
        "inheritance": "Warning -> Exception -> BaseException"
    },
    "EncodingWarning": {
        "simple_definition": "`EncodingWarning` was added in Python 3.10 (PEP 597) to warn when `open()` or `TextIOWrapper` is called without an explicit `encoding` argument, relying on platform-dependent defaults.",
        "title": "Real-world: Writing Platform-Independent File Handling (PEP 597)",
        "code": """import warnings

# PEP 597: Always specify encoding=\"utf-8\" to avoid EncodingWarning on Windows
warnings.warn("open() called without explicit encoding argument.", EncodingWarning)
print("Best practice: Always use open(filename, 'r', encoding='utf-8')")""",
        "gotchas": [
            "Enable PEP 597 warnings with `PYTHONWARNDEFAULTENCODING=1` or `python -X warn_default_encoding`."
        ],
        "inheritance": "Warning -> Exception -> BaseException"
    },
    "ResourceWarning": {
        "simple_definition": "`ResourceWarning` warns about unclosed or unreleased system resources, such as open file handles, database connections, or network sockets that were garbage collected without being closed.",
        "title": "Real-world: Preventing Leaked File Handles with Context Managers",
        "code": """import warnings

# Bad practice: f = open(\"data.txt\") without f.close() triggers ResourceWarning!
# Good practice: Always use 'with' statement context managers:
with open("test_resource.txt", "w", encoding="utf-8") as f:
    f.write("Resource automatically closed when exiting block.")

print("Resource safely closed with context manager.")""",
        "gotchas": [
            "Always use `with open(...)` or `with contextlib.closing(...)` to guarantee resources are finalized.",
            "Enabled automatically when running tests with pytest or Python in debug mode."
        ],
        "inheritance": "Warning -> Exception -> BaseException"
    }

}
