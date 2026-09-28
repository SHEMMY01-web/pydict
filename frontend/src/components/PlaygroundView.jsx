import React, { useState, useEffect } from 'react';
import { 
  Play, RotateCcw, Copy, Check, Terminal, Loader2, 
  Sparkles, BookOpen, Trash2, ArrowUpRight, Cpu
} from 'lucide-react';
import { runPythonCode, getPyodide } from '../services/pyodide';

const TEMPLATES = [
  {
    id: 'list-comprehension',
    name: 'List & Dict Comprehensions',
    entrySlug: 'list-comprehension',
    description: 'Transforming, mapping, and filtering collections concisely.',
    code: `# List & Dictionary Comprehensions in Python
# 1. Filter even numbers and square them
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_squares = [x**2 for x in numbers if x % 2 == 0]
print("Even squares:", even_squares)

# 2. Dictionary comprehension: mapping words to lengths
words = ["python", "wiktionary", "comprehension", "lexicon", "syntax"]
word_lengths = {word: len(word) for word in words}
print("Word lengths dictionary:", word_lengths)

# 3. Nested comprehension: flatten a 2D matrix
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [val for row in matrix for val in row]
print("Flattened matrix:", flattened)
`
  },
  {
    id: 'walrus-operator',
    name: 'Walrus Operator (:=)',
    entrySlug: 'walrus-operator',
    description: 'Assignment expressions to evaluate and assign in one step.',
    code: `# Walrus Operator (:=) - Introduced in Python 3.8 (PEP 572)
# Avoid redundant calculations in conditions and loops

data = "PyKtionary: The definitive Python lexicon"

# Assign and test in a single expression
if (n := len(data)) > 20:
    print(f"String is long ({n} characters): '{data[:15]}...'")

# Simulating stream / chunk processing
import random
def get_sensor_data():
    return random.choice([10, 42, 88, 99, 0, 55])

# Read until 0 is encountered, logging every reading
print("\\nReading sensor values with walrus operator:")
step = 1
while (value := get_sensor_data()) != 0:
    print(f"  Step {step}: reading = {value}")
    step += 1
    if step > 5:
        break
print("Finished stream processing.")
`
  },
  {
    id: 'pattern-matching',
    name: 'Structural Pattern Matching',
    entrySlug: 'pattern-matching',
    description: 'Match/case statement for complex data destructuring (Python 3.10+).',
    code: `# Structural Pattern Matching (match / case) - Python 3.10 (PEP 634)

def parse_command(command):
    match command:
        case ("quit" | "exit"):
            return "Terminating application session..."
        case ("lookup", word):
            return f"Opening dictionary entry for: '{word}'"
        case ("search", query, int(limit)):
            return f"Searching for '{query}' (limit: {limit} results)"
        case {"action": "filter", "category": cat}:
            return f"Applying category filter: {cat}"
        case _:
            return f"Unknown command syntax: {command}"

commands = [
    ("lookup", "generator"),
    ("search", "dunder", 10),
    {"action": "filter", "category": "technique"},
    ("quit",),
    ("invalid", "args", "extra")
]

for cmd in commands:
    print(f"CMD {cmd} -> {parse_command(cmd)}")
`
  },
  {
    id: 'decorators',
    name: 'Custom Decorators (@wraps)',
    entrySlug: 'decorators',
    description: 'Higher-order function wrappers with argument passing & timing.',
    code: `# Custom Decorator with functools.wraps
import time
from functools import wraps

def benchmark(func):
    """Decorator that measures and reports the execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration_ms = (time.perf_counter() - start) * 1000
        print(f"[BENCHMARK] {func.__name__}() took {duration_ms:.3f} ms")
        return result
    return wrapper

@benchmark
def compute_fibonacci_primes(limit=25):
    """Generate Fibonacci numbers and identify primes."""
    def is_prime(n):
        return n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))
    
    a, b = 0, 1
    primes = []
    for _ in range(limit):
        if is_prime(a):
            primes.append(a)
        a, b = b, a + b
    return primes

primes = compute_fibonacci_primes(25)
print(f"Fibonacci primes found: {primes}")
print(f"Function metadata preserved: doc='{compute_fibonacci_primes.__doc__}'")
`
  },
  {
    id: 'generators',
    name: 'Generators & Lazy Evaluation',
    entrySlug: 'generator',
    description: 'Memory-efficient data pipelines using yield and generator expressions.',
    code: `# Generator Functions and Lazy Pipelines
import sys

def fibonacci_stream(limit=10):
    """Infinite or capped lazy sequence generator using yield."""
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

# 1. Inspect generator object (constant memory footprint)
gen = fibonacci_stream(10)
print(f"Generator object: {gen} (Size: {sys.getsizeof(gen)} bytes)")

# 2. Iterate using next() and loop
print("\\nFirst 3 items via next():")
print(" ", next(gen))
print(" ", next(gen))
print(" ", next(gen))

print("\\nRemaining items:")
for num in gen:
    print(" ", num)

# 3. Generator expression vs List comprehension memory
list_comp = [x * 2 for x in range(10000)]
gen_expr = (x * 2 for x in range(10000))
print(f"\\nMemory comparison (10,000 items):")
print(f"  List comprehension: {sys.getsizeof(list_comp)} bytes")
print(f"  Generator expression: {sys.getsizeof(gen_expr)} bytes")
`
  },
  {
    id: 'context-managers',
    name: 'Custom Context Managers',
    entrySlug: 'context-manager',
    description: 'Deterministic resource setup & teardown using the with statement.',
    code: `# Custom Context Manager using class protocol (__enter__ & __exit__)
class DatabaseTransaction:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"[TRANSACTION BEGIN] '{self.name}' opened. Acquiring row locks...")
        return self

    def query(self, sql):
        print(f"  Executing: {sql}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"[TRANSACTION ROLLBACK] Error occurred ({exc_val}). Rolling back changes!")
            return False  # Propagate exception
        print(f"[TRANSACTION COMMIT] '{self.name}' successfully committed.")
        return True

# Successful transaction
print("--- Test 1: Successful Transaction ---")
with DatabaseTransaction("UpdateLexicon") as tx:
    tx.query("UPDATE entries SET sense_count = 3 WHERE slug = 'zip'")
    tx.query("INSERT INTO audit_log (action) VALUES ('update')")

print("\\nAll resources cleaned up safely.")
`
  },
  {
    id: 'dataclasses',
    name: 'Modern Dataclasses',
    entrySlug: 'dataclass',
    description: 'Type-annotated data containers with auto-generated special methods.',
    code: `# Modern Dataclasses (PEP 557) - Python 3.7+
from dataclasses import dataclass, field
from typing import List

@dataclass(order=True)
class LexiconEntry:
    # Sort index enables direct comparisons
    sort_index: int = field(init=False, repr=False)
    term: str
    category: str
    views: int = 0
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        # Determine sorting priority by view count
        self.sort_index = self.views

# Create entries
entry1 = LexiconEntry(term="walrus operator", category="technique", views=1450, tags=["syntax", "pep-572"])
entry2 = LexiconEntry(term="list comprehension", category="technique", views=3820, tags=["syntax", "loops"])

print("Entry 1:", entry1)
print("Entry 2:", entry2)
print("Is entry2 more viewed than entry1?", entry2 > entry1)
`
  },
  {
    id: 'eafp',
    name: 'EAFP vs LBYL Idiom',
    entrySlug: 'eafp',
    description: 'Easier to Ask for Forgiveness than Permission (Pythonic error handling).',
    code: `# EAFP (Easier to Ask for Forgiveness than Permission)
# Pythonic idiom: assume keys/attributes exist and catch exceptions cleanly

user_profile = {
    "username": "guido_van_rossum",
    "role": "BDFL Emeritus",
    "stats": {"contributions": 9999}
}

# LBYL style (Look Before You Leap) - C/Java style
print("--- LBYL Style ---")
if "stats" in user_profile and isinstance(user_profile["stats"], dict) and "contributions" in user_profile["stats"]:
    print("Contributions:", user_profile["stats"]["contributions"])
else:
    print("Contributions not found")

# EAFP style (Easier to Ask for Forgiveness than Permission) - Idiomatic Python
print("\\n--- Pythonic EAFP Style ---")
try:
    print("Contributions:", user_profile["stats"]["contributions"])
except (KeyError, TypeError) as e:
    print(f"Defaulting: stats unavailable ({e})")

# Safe attribute dispatch with EAFP
class Duck:
    def quack(self):
        print("Quack! (I am a Python duck)")

def make_it_quack(creature):
    try:
        creature.quack()
    except AttributeError:
        print("Object cannot quack; not a duck.")

make_it_quack(Duck())
make_it_quack("just a string")
`
  },
  {
    id: 'scratchpad',
    name: 'Blank Python Scratchpad',
    entrySlug: null,
    description: 'Write, prototype, and execute arbitrary Python code directly in your browser.',
    code: `# PyKtionary Interactive Python Scratchpad
# Powered by client-side WebAssembly (Pyodide Python 3.11)
# Write any Python code below and press 'Run Code' or Ctrl+Enter

import math

def calculate_primes(limit=50):
    primes = []
    for num in range(2, limit + 1):
        if all(num % i != 0 for i in range(2, int(math.isqrt(num)) + 1)):
            primes.append(num)
    return primes

print("PyKtionary WASM Python Environment")
print("Primes up to 50:", calculate_primes(50))
`
  }
];

export default function PlaygroundView({ onSelectEntry }) {
  const [selectedTemplate, setSelectedTemplate] = useState(TEMPLATES[0]);
  const [code, setCode] = useState(TEMPLATES[0].code);
  const [output, setOutput] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [statusMessage, setStatusMessage] = useState(null);
  const [isCopied, setIsCopied] = useState(false);
  const [executionTime, setExecutionTime] = useState(null);
  const [pyodideReady, setPyodideReady] = useState(false);

  // Pre-warm Pyodide in background
  useEffect(() => {
    getPyodide()
      .then(() => setPyodideReady(true))
      .catch((err) => console.warn('Pyodide preload error:', err));
  }, []);

  const handleSelectTemplate = (template) => {
    setSelectedTemplate(template);
    setCode(template.code);
    setOutput('');
    setStatusMessage(null);
    setExecutionTime(null);
  };

  const handleRun = async () => {
    setIsRunning(true);
    setStatusMessage('Executing in Pyodide WASM...');
    try {
      const res = await runPythonCode(code);
      setExecutionTime(res.durationMs);

      if (res.success) {
        let finalOut = res.output;
        if (res.stderr) {
          finalOut += `\n[stderr]:\n${res.stderr}`;
        }
        setOutput(finalOut);
        setStatusMessage(`Finished in ${res.durationMs}ms`);
      } else {
        setOutput(`Traceback (most recent call last):\n${res.error}`);
        setStatusMessage(`Error (${res.durationMs}ms)`);
      }
    } catch (err) {
      setOutput(`Execution failed: ${err.message}`);
      setStatusMessage('Failed');
    } finally {
      setIsRunning(false);
    }
  };

  const handleReset = () => {
    setCode(selectedTemplate.code);
    setOutput('');
    setStatusMessage(null);
    setExecutionTime(null);
  };

  const handleClearOutput = () => {
    setOutput('');
    setStatusMessage(null);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  // Keyboard shortcut Ctrl+Enter to execute
  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      handleRun();
    }
  };

  return (
    <div className="playground-view-container">
      {/* Playground Page Header */}
      <div className="playground-page-header">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Terminal size={22} color="var(--py-blue)" />
            <h1 style={{ fontSize: '1.6rem', fontFamily: 'var(--font-serif)', fontWeight: 700 }}>
              Python Interactive Playground
            </h1>
            <span className="wiki-pill" style={{ fontSize: '0.75rem', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              <Cpu size={12} />
              {pyodideReady ? 'Pyodide WASM Active' : 'Loading Runtime...'}
            </span>
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '4px' }}>
            Live in-browser Python execution environment. Select a curated technique template or prototype your own code.
          </p>
        </div>

        {selectedTemplate.entrySlug && onSelectEntry && (
          <button
            className="wiki-action-btn"
            onClick={() => onSelectEntry(selectedTemplate.entrySlug)}
            title="Read complete Wiktionary article for this concept"
            style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
          >
            <BookOpen size={14} />
            <span>Read '{selectedTemplate.name}' in Lexicon</span>
            <ArrowUpRight size={13} style={{ opacity: 0.7 }} />
          </button>
        )}
      </div>

      {/* Main Grid: Template Selector (Left) & Editor/Console (Right) */}
      <div className="playground-grid">
        {/* Left Column: Technique Templates */}
        <div className="playground-sidebar">
          <div className="playground-sidebar-header">
            <span>Technique Templates</span>
          </div>
          <div className="playground-template-list">
            {TEMPLATES.map((tmpl) => {
              const isSelected = tmpl.id === selectedTemplate.id;
              return (
                <button
                  key={tmpl.id}
                  className={`playground-template-item ${isSelected ? 'active' : ''}`}
                  onClick={() => handleSelectTemplate(tmpl)}
                >
                  <div className="template-item-name">{tmpl.name}</div>
                  <div className="template-item-desc">{tmpl.description}</div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Column: Code Editor + Execution Console */}
        <div className="playground-main">
          {/* Top Editor Toolbar */}
          <div className="playground-toolbar">
            <div className="toolbar-info">
              <span className="toolbar-active-title">{selectedTemplate.name}</span>
              <span className="toolbar-kbd-hint">Ctrl+Enter to run</span>
            </div>

            <div className="toolbar-actions">
              <button
                className="wiki-action-btn"
                onClick={handleCopy}
                title="Copy code to clipboard"
                style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', padding: '4px 8px' }}
              >
                {isCopied ? <Check size={13} color="#10B981" /> : <Copy size={13} />}
                <span>{isCopied ? 'Copied' : 'Copy'}</span>
              </button>

              <button
                className="wiki-action-btn"
                onClick={handleReset}
                title="Reset snippet to original"
                style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', padding: '4px 8px' }}
              >
                <RotateCcw size={13} />
                <span>Reset</span>
              </button>

              <button
                className="run-code-btn"
                onClick={handleRun}
                disabled={isRunning}
                style={{ padding: '6px 14px', fontSize: '0.85rem' }}
              >
                {isRunning ? (
                  <>
                    <Loader2 size={14} className="animate-spin" />
                    <span>Executing...</span>
                  </>
                ) : (
                  <>
                    <Play size={14} fill="currentColor" />
                    <span>Run Snippet</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Interactive Code Editor Textarea */}
          <div className="playground-editor-wrap">
            <textarea
              className="playground-editor-textarea"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              onKeyDown={handleKeyDown}
              spellCheck="false"
              placeholder="Type your Python code here..."
            />
          </div>

          {/* Execution Output Console */}
          <div className="playground-console">
            <div className="console-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span className="console-title">Terminal Output (stdout / stderr)</span>
                {executionTime !== null && (
                  <span className="console-time-badge">{executionTime} ms</span>
                )}
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                {statusMessage && (
                  <span style={{ fontSize: '0.75rem', color: isRunning ? 'var(--py-blue)' : '#a7f3d0' }}>
                    {statusMessage}
                  </span>
                )}
                {output && (
                  <button
                    className="icon-btn"
                    onClick={handleClearOutput}
                    title="Clear console output"
                    style={{ color: '#94a3b8', width: '24px', height: '24px' }}
                  >
                    <Trash2 size={13} />
                  </button>
                )}
              </div>
            </div>

            <pre className="console-body">
              {output || (
                <span style={{ color: '#64748b', fontStyle: 'italic' }}>
                  Click "Run Snippet" (or press Ctrl+Enter) to execute the code in your browser's WebAssembly Python runtime.
                </span>
              )}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
