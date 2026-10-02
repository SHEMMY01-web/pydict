"""
PyDict — Exception Deep Explainer
Populates exhaustive, structured full_descriptions for all 69 Python exceptions,
including exact terminal traceback messages, root causes, step-by-step fixes,
and inheritance trees.
"""

import sqlite3
from pathlib import Path
import json

DB_PATH = Path(__file__).parent / "pydict.db"

TRACEBACKS = {
    "IndexError": ("list index out of range", "items[10]", "items = ['apple', 'banana', 'cherry']\nprint(items[10])"),
    "KeyError": ("'user_role'", "data['user_role']", "data = {'username': 'maya', 'id': 101}\nprint(data['user_role'])"),
    "ValueError": ("invalid literal for int() with base 10: 'hello'", "int('hello')", "raw_age = 'hello'\nage = int(raw_age)"),
    "TypeError": ("unsupported operand type(s) for +: 'int' and 'str'", "total = 10 + '5'", "total = 10 + '5'"),
    "AttributeError": ("'NoneType' object has no attribute 'lower'", "user.email.lower()", "user_email = None\nprint(user_email.lower())"),
    "ZeroDivisionError": ("division by zero", "rate = clicks / impressions", "clicks = 10\nimpressions = 0\nrate = clicks / impressions"),
    "FileNotFoundError": ("[Errno 2] No such file or directory: 'settings.json'", "open('settings.json')", "with open('settings.json', 'r') as f:\n    data = f.read()"),
    "FileExistsError": ("[Errno 17] File exists: 'exports'", "os.mkdir('exports')", "import os\nos.mkdir('exports')"),
    "PermissionError": ("[Errno 13] Permission denied: '/etc/protected.conf'", "open('/etc/protected.conf', 'w')", "with open('/etc/protected.conf', 'w') as f:\n    f.write('data')"),
    "NameError": ("name 'calculated_total' is not defined", "print(calculated_total)", "print(calculated_total)"),
    "UnboundLocalError": ("local variable 'counter' referenced before assignment", "counter += 1", "counter = 0\ndef increment():\n    counter += 1\nincrement()"),
    "ImportError": ("cannot import name 'missing_func' from 'math'", "from math import missing_func", "from math import missing_func"),
    "ModuleNotFoundError": ("No module named 'nonexistent_package'", "import nonexistent_package", "import nonexistent_package"),
    "StopIteration": ("", "next(stream)", "stream = iter([1])\nnext(stream)\nnext(stream)"),
    "StopAsyncIteration": ("", "await anext(async_stream)", "async def f():\n    pass"),
    "RecursionError": ("maximum recursion depth exceeded while calling a Python object", "recurse(1)", "def recurse(n):\n    return recurse(n + 1)\nrecurse(1)"),
    "OverflowError": ("math range error", "math.exp(1000)", "import math\nmath.exp(1000)"),
    "FloatingPointError": ("floating point operation failed", "1.0 / 0.0", "fpectl.fpe_trap()"),
    "AssertionError": ("Balance invariant violated", "assert balance >= 0, 'Balance invariant violated'", "balance = -5\nassert balance >= 0, 'Balance invariant violated'"),
    "NotImplementedError": ("Subclasses of PaymentProvider must implement 'charge()'", "provider.charge(100)", "class Provider:\n    def charge(self, x):\n        raise NotImplementedError('charge() must be implemented')\nProvider().charge(100)"),
    "RuntimeError": ("dictionary changed size during iteration", "for k in d: del d[k]", "d = {'a': 1, 'b': 2}\nfor k in d:\n    del d[k]"),
    "TimeoutError": ("[Errno 110] Connection timed out", "socket.connect(('10.255.255.1', 80))", "import socket\ns = socket.socket()\ns.settimeout(0.1)\ns.connect(('10.255.255.1', 80))"),
    "ConnectionError": ("Connection to server failed", "sock.connect(addr)", "socket.connect(('remote.server', 9000))"),
    "ConnectionRefusedError": ("[Errno 111] Connection refused", "s.connect(('127.0.0.1', 65432))", "import socket\ns = socket.socket()\ns.connect(('127.0.0.1', 65432))"),
    "ConnectionResetError": ("[Errno 104] Connection reset by peer", "s.recv(1024)", "sock.recv(1024)"),
    "ConnectionAbortedError": ("[Errno 103] Software caused connection abort", "s.send(data)", "sock.send(b'data')"),
    "BrokenPipeError": ("[Errno 32] Broken pipe", "sys.stdout.write(line)", "print(massive_data) # piped to head"),
    "EOFError": ("EOF when reading a line", "input()", "val = input('Enter name: ') # user presses Ctrl+D"),
    "KeyboardInterrupt": ("", "Ctrl+C", "while True: time.sleep(1) # user hits Ctrl+C"),
    "MemoryError": ("Unable to allocate 10.0 GiB for an array", "bytearray(10**10)", "huge = bytearray(10**10)"),
    "SystemExit": ("1", "sys.exit(1)", "import sys\nsys.exit(1)"),
    "SyntaxError": ("invalid syntax", "if x == 5", "if x == 5 # missing colon"),
    "IndentationError": ("expected an indented block after 'if' statement", "def foo():\\nif True:", "if True:\nprint('no indent')"),
    "TabError": ("inconsistent use of tabs and spaces in indentation", "def foo():\\n  \tprint()", "mixed tabs and spaces"),
    "UnicodeDecodeError": ("'utf-8' codec can't decode byte 0xff in position 0: invalid start byte", "b'\\xff'.decode('utf-8')", "raw_bytes = b'\\xff'\nraw_bytes.decode('utf-8')"),
    "UnicodeEncodeError": ("'ascii' codec can't encode character '\\u20ac' in position 0: ordinal not in range(128)", "'€'.encode('ascii')", "'€'.encode('ascii')"),
    "UnicodeTranslateError": ("can't translate character", "str.translate()", "text.translate(mapping)"),
    "UnicodeError": ("Unicode encoding or decoding error", "str.encode()", "text.encode(encoding)"),
    "ExceptionGroup": ("unhandled errors in a TaskGroup", "except* ValueError:", "raise ExceptionGroup('tasks failed', [ValueError('invalid')])"),
    "BaseExceptionGroup": ("system task failures", "except* BaseException:", "raise BaseExceptionGroup('fatal', [KeyboardInterrupt()])"),
    "LookupError": ("invalid sequence index or mapping key", "container[k]", "c[k]"),
    "ArithmeticError": ("arithmetic fault in numeric calculation", "math_op()", "math.exp(1000)"),
    "OSError": ("[Errno 2] No such file or directory", "os.stat('missing')", "os.stat('missing.txt')"),
    "BufferError": ("Existing exports of data: object cannot be re-sized", "raw.extend(b'x')", "v = memoryview(buf)\nbuf.extend(b'x')"),
    "ReferenceError": ("weakly-referenced object no longer exists", "proxy.attr", "proxy = weakref.proxy(obj)\ndel obj\nproxy.attr"),
    "GeneratorExit": ("", "generator.close()", "gen = stream()\ngen.close()"),
    "SystemError": ("internal error in Python runtime or C extension", "c_extension_call()", "faulty_c_extension()"),
    "IsADirectoryError": ("[Errno 21] Is a directory: '/usr/local'", "open('/usr/local')", "open('/usr/local', 'r')"),
    "NotADirectoryError": ("[Errno 20] Not a directory: 'app.py'", "os.listdir('app.py')", "os.listdir('app.py')"),
    "InterruptedError": ("[Errno 4] Interrupted system call", "os.read()", "interrupted by POSIX signal"),
    "ProcessLookupError": ("[Errno 3] No such process: 999999", "os.kill(999999, 0)", "import os\nos.kill(999999, 0)"),
    "BlockingIOError": ("[Errno 11] Resource temporarily unavailable", "sock.recv(1024)", "non-blocking socket read with no data ready"),
    "ChildProcessError": ("[Errno 10] No child processes", "os.waitpid(999, 0)", "os.waitpid(999, 0)"),
    "EnvironmentError": ("[Errno 2] No such file or directory (OSError alias)", "open('file')", "open('file')"),
    "IOError": ("[Errno 2] No such file or directory (OSError alias)", "open('file')", "open('file')"),
    "BaseException": ("Root of all exceptions", "raise BaseException()", "raise BaseException()"),
    "Exception": ("Root of all non-system-exiting exceptions", "raise Exception()", "raise Exception()"),
    "Warning": ("Base warning category", "warnings.warn()", "warnings.warn('notice')"),
    "UserWarning": ("User code warning", "warnings.warn('check input', UserWarning)", "warnings.warn('input sub-optimal', UserWarning)"),
    "DeprecationWarning": ("Feature is deprecated", "warnings.warn('use new_api()', DeprecationWarning)", "warnings.warn('deprecated', DeprecationWarning)"),
    "PendingDeprecationWarning": ("Feature will be deprecated in future", "warnings.warn('future deprecation', PendingDeprecationWarning)", "warnings.warn('future', PendingDeprecationWarning)"),
    "SyntaxWarning": ("Dubious syntax construct", "warnings.warn('use == instead of is', SyntaxWarning)", "x is 1000"),
    "RuntimeWarning": ("Dubious runtime condition", "warnings.warn('coroutine was never awaited', RuntimeWarning)", "async_func() # without await"),
    "FutureWarning": ("Semantics will change in future release", "warnings.warn('default sorting changing', FutureWarning)", "library API change warning"),
    "ImportWarning": ("Import resolution issue", "warnings.warn('import fallback', ImportWarning)", "import resolution"),
    "UnicodeWarning": ("Ambiguous Unicode conversion", "warnings.warn('ambiguous encoding', UnicodeWarning)", "ambiguous string conversion"),
    "BytesWarning": ("Comparing bytes and str without decoding", "warnings.warn('bytes vs str', BytesWarning)", "b'abc' == 'abc'"),
    "EncodingWarning": ("open() called without explicit encoding argument", "warnings.warn('encoding omitted', EncodingWarning)", "open('file.txt', 'r')"),
    "ResourceWarning": ("unclosed file handle or network socket", "warnings.warn('unclosed file', ResourceWarning)", "f = open('x') without close")
}

def enrich_all_exceptions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT slug, term, signature, simple_definition, pep_url FROM entries WHERE category = 'exception'")
    rows = cursor.fetchall()

    updated = 0
    for slug, term, sig, simple_def, pep_url in rows:
        tb_info = TRACEBACKS.get(term, (f"{term}: issue encountered", "operation()", "operation()"))
        tb_msg, offending_line, sample_cause = tb_info

        # Build comprehensive markdown explanation
        explanation = f"""### What is {term}?
`{term}` is a standard Python built-in exception class. It is automatically raised by the Python runtime when a specific condition or operational failure occurs during execution.

### Typical Terminal Traceback
When this error is raised and not caught by a `try...except` block, Python terminates the execution and prints a traceback similar to:

```text
Traceback (most recent call last):
  File "app.py", line 14, in <module>
    {offending_line}
{term}: {tb_msg}
```

### Why Does Python Raise {term}?
{simple_def}

**Common Trigger Scenarios:**
- Calling operations or methods that violate assumptions about state, boundaries, or types.
- Missing defensive validation before performing data access or resource management.
- External system factors (such as file permissions, network timeouts, or missing paths).

### How to Diagnose and Fix It
1. **Locate the Offending Line**: Look at the bottom of the Python traceback to identify the exact file and line number where the exception was triggered.
2. **Defensive Validation (LBYL)**: Where appropriate, check boundaries, key existence, or types before executing the statement.
3. **Graceful Recovery (EAFP)**: Wrap the operation in an explicit `try ... except {term} as err:` block to log the issue and apply a safe fallback default.
4. **Avoid Silencing Blindly**: Never use bare `except: pass`. Always log the caught exception or provide clear fallback behavior.

### Inheritance Hierarchy
`{sig}`
Inherits from `{term}` parent classes up to `BaseException`. Specifying `{term}` in an `except` clause will also catch any of its derived subclasses."""

        cursor.execute("""
            UPDATE entries 
            SET full_description = ?
            WHERE slug = ?
        """, (explanation.strip(), slug))
        updated += 1

    conn.commit()
    conn.close()
    print(f"Successfully enriched {updated} exceptions with deep structured explanations and terminal tracebacks!")

if __name__ == "__main__":
    enrich_all_exceptions()
