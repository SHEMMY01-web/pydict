"""
Rich real-world examples and plain-English simple definitions for Python built-ins,
keywords, and standard library components.
"""

# Plain-English definitions and realistic code examples for built-in functions & types
BUILTIN_CATALOG = {
    "sum": {
        "simple_definition": "`sum()` adds up all numbers in a collection (like a list or tuple). You can also provide an optional starting number, which the sum will build on top of.",
        "title": "Real-world: Shopping Cart Total with Base Fee",
        "code": """# Real-world: Calculating shopping cart total with base shipping
cart_items = [19.99, 35.50, 4.25, 12.00]
shipping_fee = 5.00

# sum() starts with shipping fee and adds all item prices
total = sum(cart_items, shipping_fee)
print(f"Cart items: {cart_items}")
print(f"Total with shipping (${shipping_fee}): ${total:.2f}")

# Quick syntax demo:
numbers = [10, 20, 30, 40]
print('Sum:', sum(numbers, 5)) # starts with 5"""
    },
    "len": {
        "simple_definition": "`len()` counts how many items are inside an object — whether it's the number of characters in a string, items in a list, or keys in a dictionary.",
        "title": "Real-world: Form Field Validation & Message Length",
        "code": """# Real-world: Validating password and SMS length requirements
password = "superSecurePassword123"
sms_message = "Your one-time verification code is 849201. Do not share this."

print(f"Password characters: {len(password)}")
if len(password) >= 12:
    print("✓ Password meets security requirements")

print(f"SMS length: {len(sms_message)} / 160 characters")
if len(sms_message) <= 160:
    print("✓ Fits in a single SMS message segment")"""
    },
    "map": {
        "simple_definition": "`map()` applies a specific function to every item in a list or sequence, returning an iterator of the results without needing a manual loop.",
        "title": "Real-world: Sanitizing and Formatting Raw Input Data",
        "code": """# Real-world: Cleaning up user input tags and email domains
raw_tags = ["  python ", " fastAPI  ", "Web-Dev  ", "  ai "]

# Strip whitespace and normalize to lowercase across all items
cleaned_tags = list(map(lambda t: t.strip().lower(), raw_tags))
print("Raw tags:    ", raw_tags)
print("Cleaned tags:", cleaned_tags)

# Formatting prices to 2 decimal places
raw_prices = [12.5, 9.999, 4.0, 100.123]
formatted = list(map(lambda p: f"${p:.2f}", raw_prices))
print("Formatted:   ", formatted)"""
    },
    "filter": {
        "simple_definition": "`filter()` checks every item in a collection against a condition function, keeping only the items where the condition returns True.",
        "title": "Real-world: Finding Active Users & High-Value Orders",
        "code": """# Real-world: Filtering database records for active accounts
users = [
    {"username": "alice", "active": True, "balance": 150.00},
    {"username": "bob", "active": False, "balance": 0.00},
    {"username": "charlie", "active": True, "balance": 450.50},
    {"username": "diana", "active": False, "balance": 25.00}
]

# Keep only active users
active_users = list(filter(lambda u: u["active"], users))
print("Active users:", [u["username"] for u in active_users])

# Filter orders exceeding $100 threshold
high_balance = list(filter(lambda u: u["balance"] > 100, active_users))
print("High balance VIPs:", [u["username"] for u in high_balance])"""
    },
    "zip": {
        "simple_definition": "`zip()` pairs up corresponding elements from multiple lists like a zipper, grouping item 0 with item 0, item 1 with item 1, and so on.",
        "title": "Real-world: Merging Header Names with Row Values",
        "code": """# Real-world: Combining CSV column headers with row data into a dictionary
headers = ["id", "product", "price", "stock"]
row_data = [101, "Mechanical Keyboard", 89.99, 42]

# Turn paired tuples directly into a record dictionary
product_record = dict(zip(headers, row_data))
print("Constructed Record:")
for key, value in product_record.items():
    print(f"  {key}: {value}")"""
    },
    "enumerate": {
        "simple_definition": "`enumerate()` loops over a sequence while keeping a running counter, giving you both the index number and the item simultaneously.",
        "title": "Real-world: Numbered Ranking and Task Prioritization",
        "code": """# Real-world: Printing a numbered leaderboard with custom start index
top_players = ["CyberSamurai", "Pythonista", "ByteMaster", "AlgoQueen"]

print("🏆 Leaderboard:")
for rank, player in enumerate(top_players, start=1):
    medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
    print(f"  {medal} {player}")"""
    },
    "sorted": {
        "simple_definition": "`sorted()` returns a brand new sorted list from any iterable without changing the original list. You can customize the sorting logic with `key` and `reverse`.",
        "title": "Real-world: Multi-Criteria Product Catalog Sorting",
        "code": """# Real-world: Sorting e-commerce inventory by price or ratings
products = [
    {"name": "USB-C Hub", "price": 34.99, "rating": 4.5},
    {"name": "Wireless Mouse", "price": 19.99, "rating": 4.8},
    {"name": "4K Monitor", "price": 299.99, "rating": 4.7},
    {"name": "Laptop Stand", "price": 24.50, "rating": 4.2}
]

# Sort by rating (highest first)
by_rating = sorted(products, key=lambda p: p["rating"], reverse=True)
print("Top rated products:")
for p in by_rating:
    print(f"  ⭐ {p['rating']} - {p['name']} (${p['price']})")"""
    },
    "range": {
        "simple_definition": "`range()` generates a sequence of numbers on demand without storing them all in memory, commonly used to control how many times a loop runs.",
        "title": "Real-world: Pagination & Batch Processing Intervals",
        "code": """# Real-world: Slicing records into pagination chunks
total_items = 45
page_size = 10

print("Generating page batch ranges:")
for page_num, start_idx in enumerate(range(0, total_items, page_size), start=1):
    end_idx = min(start_idx + page_size, total_items)
    print(f"  Page {page_num}: Items {start_idx} to {end_idx - 1} (Total: {end_idx - start_idx})")"""
    },
    "min": {
        "simple_definition": "`min()` finds and returns the smallest item in a collection, or the lowest value based on a custom comparison key.",
        "title": "Real-world: Finding the Best Deal or Lowest Server Latency",
        "code": """# Real-world: Choosing the fastest server endpoint
servers = [
    {"region": "us-east", "ping_ms": 42},
    {"region": "eu-central", "ping_ms": 115},
    {"region": "us-west", "ping_ms": 18},
    {"region": "ap-southeast", "ping_ms": 180}
]

best_server = min(servers, key=lambda s: s["ping_ms"])
print(f"Fastest Server: {best_server['region']} ({best_server['ping_ms']}ms)")"""
    },
    "max": {
        "simple_definition": "`max()` finds and returns the largest item in a collection, or the highest value based on a custom comparison key.",
        "title": "Real-world: Identifying Top Performer in Sales",
        "code": """# Real-world: Detecting highest sale of the quarter
sales = [
    {"rep": "Sarah", "amount": 14200},
    {"rep": "David", "amount": 23500},
    {"rep": "Elena", "amount": 19800}
]

top_sale = max(sales, key=lambda s: s["amount"])
print(f"Top Representative: {top_sale['rep']} with ${top_sale['amount']:,}")"""
    },
    "round": {
        "simple_definition": "`round()` rounds a floating-point number to a specified number of decimal places (defaulting to the nearest whole integer).",
        "title": "Real-world: Currency & Tax Computation",
        "code": """# Real-world: Calculating sales tax with standard financial rounding
subtotal = 149.95
tax_rate = 0.0825

tax = round(subtotal * tax_rate, 2)
total = round(subtotal + tax, 2)

print(f"Subtotal: ${subtotal:.2f}")
print(f"Tax:      ${tax:.2f}")
print(f"Total:    ${total:.2f}")"""
    },
    "isinstance": {
        "simple_definition": "`isinstance()` checks whether a variable belongs to a particular type or class (including any subclasses). It's the recommended way to check types in Python.",
        "title": "Real-world: Safe Configuration Parser & Polymorphic Handling",
        "code": """# Real-world: Handling polymorphic API payloads safely
def parse_setting(key, value):
    if isinstance(value, bool):
        return f"Flag [{key}] is {'ENABLED' if value else 'DISABLED'}"
    elif isinstance(value, (int, float)):
        return f"Metric [{key}] = {value * 1.1:.2f} (scaled)"
    elif isinstance(value, list):
        return f"List [{key}] contains {len(value)} items"
    return f"Value [{key}] = {value}"

print(parse_setting("debug", True))
print(parse_setting("timeout", 30))
print(parse_setting("hosts", ["srv1", "srv2", "srv3"]))"""
    },
    "all": {
        "simple_definition": "`all()` checks if every single item in an iterable is True. If even one item is False (or falsy), it returns False.",
        "title": "Real-world: Pre-flight Checklist & Health Checks",
        "code": """# Real-world: Ensuring all microservices pass health checks before deployment
service_health = {
    "database": True,
    "redis_cache": True,
    "auth_service": True,
    "payment_gateway": True
}

all_healthy = all(service_health.values())
print(f"All services operational? {all_healthy}")

if all_healthy:
    print("🚀 Deployment approved: all checks green!")
else:
    print("⚠️ Deployment aborted: one or more checks failed.")"""
    },
    "any": {
        "simple_definition": "`any()` checks if at least one item in an iterable is True. It returns True as soon as it finds the first truthy value.",
        "title": "Real-world: Permission Verification & Threat Detection",
        "code": """# Real-world: Checking if a user has any required admin roles
user_roles = ["editor", "subscriber"]
admin_roles = ["admin", "superadmin", "owner"]

has_admin_access = any(role in admin_roles for role in user_roles)
print(f"User roles: {user_roles}")
print(f"Access granted: {has_admin_access}")"""
    },
    "abs": {
        "simple_definition": "`abs()` returns the absolute (positive) magnitude of a number, stripping away any minus sign.",
        "title": "Real-world: Measuring Sensor Deviation & Tolerance Checks",
        "code": """# Real-world: Checking if a temperature reading is within acceptable tolerance
target_temp = 72.0
actual_reading = 74.3
tolerance = 2.5

difference = abs(actual_reading - target_temp)
print(f"Target: {target_temp}° | Actual: {actual_reading}° | Deviation: {difference:.1f}°")

if difference <= tolerance:
    print("✓ Temperature is within safe operating range")
else:
    print("⚠️ Temperature alert: deviation exceeded tolerance!")"""
    },
    "any": {
        "simple_definition": "`any()` returns True if at least one element in an iterable evaluates to True; otherwise False.",
        "title": "Real-world: Security Privilege Verification",
        "code": """# Real-world: Checking if user has at least one administrative flag
user_flags = ["can_view", "can_comment", "can_edit"]
admin_flags = ["can_delete", "is_superuser", "can_ban"]

has_elevated = any(flag in admin_flags for flag in user_flags)
print(f"Has elevated privilege? {has_elevated}")"""
    },
    "open": {
        "simple_definition": "`open()` opens a file from disk and returns a file object so you can read, write, or append text or binary data.",
        "title": "Real-world: Writing and Reading Configuration Files Safely",
        "code": """# Real-world: Writing and reading application settings with context manager
import tempfile

with tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8") as f:
    f.write("DEBUG=True\\nPORT=8000\\nAPP_NAME=PyKtionary")
    filepath = f.name

# Read it back safely
with open(filepath, mode="r", encoding="utf-8") as f:
    config = dict(line.strip().split("=") for line in f if "=" in line)

print("Parsed config:", config)"""
    },
    "print": {
        "simple_definition": "`print()` outputs text and values to the console screen. You can customize separators (`sep`), line endings (`end`), and formatting.",
        "title": "Real-world: CLI Progress and Status Reporting",
        "code": """# Real-world: Formatting console status outputs with custom separators
server_ip = "192.168.1.100"
port = 8080
status = "ONLINE"

# Using sep and end to format terminal output
print("Server", server_ip, port, sep=" : ")
print("Status:", status, end=" 🟢\\n")"""
    },
    "dict": {
        "simple_definition": "`dict` creates a key-value store (dictionary), allowing you to look up, add, update, and delete information by unique keys in O(1) time.",
        "title": "Real-world: Constructing User Sessions and State",
        "code": """# Real-world: Managing a user session cache
session = dict(user_id=402, role="admin", ip="127.0.0.1", authenticated=True)

# Fast lookups with fallback
theme = session.get("theme", "dark-mode")
print(f"Session for user {session['user_id']} ({session['role']})")
print(f"Active Theme: {theme}")"""
    },
    "list": {
        "simple_definition": "`list` creates an ordered, mutable sequence of items. You can add, remove, slice, and sort elements freely.",
        "title": "Real-world: Order Queue Processing",
        "code": """# Real-world: Managing an e-commerce order processing queue
orders = list(["ORD-001", "ORD-002", "ORD-003"])
orders.append("ORD-004")  # New order arrives

processed = orders.pop(0) # Process first in queue
print(f"Processed order: {processed}")
print(f"Remaining in queue: {orders}")"""
    },
    "set": {
        "simple_definition": "`set` creates an unordered collection of unique elements, automatically eliminating duplicate entries and offering fast membership testing.",
        "title": "Real-world: Deduplicating Visitor Emails & Set Operations",
        "code": """# Real-world: Eliminating duplicate newsletter signups
raw_subscribers = ["ada@dev.org", "bob@test.com", "ada@dev.org", "clara@code.io"]
unique_subscribers = set(raw_subscribers)

print(f"Raw submissions: {len(raw_subscribers)}")
print(f"Unique subscribers ({len(unique_subscribers)}): {unique_subscribers}")

# Checking overlap between free and paid tier
free_tier = {"user1", "user2", "user3"}
paid_tier = {"user3", "user4"}
upgraded = free_tier.intersection(paid_tier)
print("Users in both tiers:", upgraded)"""
    },
    "tuple": {
        "simple_definition": "`tuple` creates an immutable (unchangeable) ordered sequence, perfect for fixed collections like coordinates, database records, and dictionary keys.",
        "title": "Real-world: Geographic Coordinates & Immutable Records",
        "code": """# Real-world: Storing immutable GPS location coordinates
gps_point = (37.7749, -122.4194)  # (Latitude, Longitude)

lat, lon = gps_point  # Unpack directly
print(f"San Francisco GPS -> Lat: {lat}, Lon: {lon}")

# Tuples can safely be used as dictionary keys because they are immutable
route_distances = {
    ("NYC", "BOS"): 215,
    ("SFO", "LAX"): 382
}
print(f"Distance SFO to LAX: {route_distances[('SFO', 'LAX')]} miles")"""
    },
    "int": {
        "simple_definition": "`int()` converts a string or number into a whole integer (no decimals). It can also parse different number bases like binary or hexadecimal.",
        "title": "Real-world: Parsing Web Query Params and Ports",
        "code": """# Real-world: Safely parsing port numbers from environment strings
raw_port = "  8080 "
port = int(raw_port.strip())

# Parsing hexadecimal color codes to integers
hex_color = "0xFF"
rgb_value = int(hex_color, 16)

print(f"Application Port: {port}")
print(f"Hex {hex_color} as integer: {rgb_value}")"""
    },
    "float": {
        "simple_definition": "`float()` converts a number or string into a decimal floating-point number.",
        "title": "Real-world: Parsing Metric Sensor Readings",
        "code": """# Real-world: Converting sensor string data into numerical values
sensor_input = "23.85"
temperature = float(sensor_input)
converted_fahrenheit = (temperature * 9/5) + 32

print(f"Sensor Reading: {temperature}°C ({converted_fahrenheit:.2f}°F)")"""
    },
    "str": {
        "simple_definition": "`str()` converts any Python object into its human-readable text (string) representation.",
        "title": "Real-world: Serializing Objects for Audit Logging",
        "code": """# Real-world: Formatting status codes and timestamps for logs
error_code = 404
timestamp = 1695900000

log_entry = "ERROR [" + str(error_code) + "] at timestamp: " + str(timestamp)
print("System Log:", log_entry)"""
    },
    "bool": {
        "simple_definition": "`bool()` checks whether a value is considered True or False by Python's truth-testing rules (falsy values include 0, empty strings, empty lists, and None).",
        "title": "Real-world: Checking Empty Collections and Flags",
        "code": """# Real-world: Validating if input fields or baskets are populated
cart = []
has_items = bool(cart)
print(f"Shopping cart has items? {has_items}")

user_input = "Alice"
has_name = bool(user_input.strip())
print(f"User provided valid name? {has_name}")"""
    },
    "reversed": {
        "simple_definition": "`reversed()` returns an iterator that traverses a sequence backwards without creating an expensive in-memory copy.",
        "title": "Real-world: Displaying Most Recent Events First",
        "code": """# Real-world: Showing log events from latest to oldest
events = ["10:00 Boot", "10:05 User Login", "10:15 File Upload", "10:20 Logout"]

print("Recent Activity (Newest First):")
for event in reversed(events):
    print(f"  • {event}")"""
    },
    "getattr": {
        "simple_definition": "`getattr()` gets the value of an object's attribute dynamically by name (as a string), with an optional default if it doesn't exist.",
        "title": "Real-world: Dynamic Plugin Dispatch and Feature Flags",
        "code": """# Real-world: Dynamically invoking command handlers
class APIController:
    def get_users(self):
        return ["Alice", "Bob"]
    def get_health(self):
        return {"status": "ok"}

controller = APIController()
endpoint = "get_health"

# Dynamically lookup and execute the method
handler = getattr(controller, endpoint, None)
if handler:
    print(f"Result of {endpoint}:", handler())
else:
    print("Endpoint not found!")"""
    },
    "hasattr": {
        "simple_definition": "`hasattr()` checks whether an object possesses a specific attribute or method, returning True or False.",
        "title": "Real-world: Duck-Typing Feature Verification",
        "code": """# Real-world: Checking if an object supports serialization or closing
class FileStream:
    def close(self):
        print("Closing stream...")

stream = FileStream()
if hasattr(stream, "close"):
    print("Object supports close protocol — closing safely.")
    stream.close()"""
    },
    "setattr": {
        "simple_definition": "`setattr()` sets the value of a named attribute on an object dynamically using a string name.",
        "title": "Real-world: Hydrating Model Instances from Dictionaries",
        "code": """# Real-world: Populating an object from database row key-values
class UserModel:
    pass

user = UserModel()
db_row = {"username": "victor_dev", "role": "admin", "points": 350}

for key, val in db_row.items():
    setattr(user, key, val)

print(f"User {user.username} has role '{user.role}' and {user.points} points.")"""
    },
    "iter": {
        "simple_definition": "`iter()` returns an iterator object from any iterable, enabling manual step-by-step element retrieval via `next()`.",
        "title": "Real-world: Reading Fixed-Size Chunks Until Sentinel",
        "code": """# Real-world: Step-by-step traversal with iter() and next()
tokens = iter(["Bearer", "eyJhbGciOi...", "2024-09"])

token_type = next(tokens)
token_val = next(tokens)
print(f"Type: {token_type} | Token: {token_val[:12]}...")"""
    },
    "next": {
        "simple_definition": "`next()` fetches the very next item from an iterator. You can provide a default value to return when the iterator is exhausted instead of raising StopIteration.",
        "title": "Real-world: Finding First Matching Item with Default Fallback",
        "code": """# Real-world: Finding the first server meeting criteria with a safe fallback
servers = [
    {"name": "srv-1", "load": 95},
    {"name": "srv-2", "load": 30},
    {"name": "srv-3", "load": 15}
]

# Find the first server with load < 50
available = next((s for s in servers if s["load"] < 50), None)
if available:
    print(f"Allocated to: {available['name']} (Load: {available['load']}%)")
else:
    print("All servers busy!")"""
    }
}

# Plain-English definitions and realistic code examples for Python Keywords
KEYWORD_CATALOG = {
    "def": {
        "simple_definition": "`def` is the keyword used to define a new function or method. It bundles a block of reusable code under a name so you can call it whenever needed.",
        "title": "Real-world: Calculating Discounts and Total Prices",
        "code": """# Real-world: Calculating the final price after a promotional discount
def calculate_discount(price, discount_percent=10):
    \"\"\"Calculates discount savings and returns the final price.\"\"\"
    savings = price * (discount_percent / 100)
    final_price = round(price - savings, 2)
    return final_price

regular_price = 120.00
sale_price = calculate_discount(regular_price, discount_percent=15)
print(f"Regular: ${regular_price} -> Sale Price: ${sale_price}")"""
    },
    "class": {
        "simple_definition": "`class` creates a blueprint for creating custom objects. Inside a class, you define properties (attributes) and actions (methods) that belong to those objects.",
        "title": "Real-world: User Account Management Model",
        "code": """# Real-world: Modeling a User Account with states and behaviors
class UserAccount:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.is_active = True

    def deactivate(self):
        self.is_active = False
        print(f"Account for '{self.username}' is now deactivated.")

# Instantiate and interact with the user object
user = UserAccount("alice_dev", "alice@example.com")
print(f"Created user: {user.username} ({user.email}) - Active: {user.is_active}")
user.deactivate()"""
    },
    "return": {
        "simple_definition": "`return` exits a function immediately and sends a result back to the code that called it. If you don't return anything, Python returns `None` by default.",
        "title": "Real-world: Authenticating User Credentials",
        "code": """# Real-world: Validating credentials and returning status and data
def verify_login(username, password):
    if not username or not password:
        return False, "Missing credentials"
    if username == "admin" and password == "secret123":
        return True, "Access granted"
    return False, "Invalid username or password"

success, message = verify_login("admin", "secret123")
print(f"Login result: {message} (Success: {success})")"""
    },
    "if": {
        "simple_definition": "`if` runs a block of code only when a condition is True. You can chain it with `elif` (else if) and `else` for alternative branches.",
        "title": "Real-world: Free Shipping Eligibility Check",
        "code": """# Real-world: Determining shipping rates based on cart value and membership
cart_total = 75.50
is_vip = True

if cart_total >= 100.0 or is_vip:
    shipping = 0.00
    print(f"Cart: ${cart_total} -> Free Shipping Qualified! ($0.00)")
elif cart_total >= 50.0:
    shipping = 4.99
    print(f"Cart: ${cart_total} -> Discounted Shipping: ${shipping}")
else:
    shipping = 9.99
    print(f"Cart: ${cart_total} -> Standard Shipping: ${shipping}")"""
    },
    "for": {
        "simple_definition": "`for` loops through each item in a sequence (like a list, string, or range), executing the block of code once for each item.",
        "title": "Real-world: Processing Bank Transactions",
        "code": """# Real-world: Filtering and summing positive deposits
transactions = [120.0, -45.0, 300.0, -15.5, 80.0]
total_deposits = 0.0

print("Transaction Audit:")
for amount in transactions:
    if amount > 0:
        total_deposits += amount
        print(f"  • Deposit: +${amount:.2f}")
    else:
        print(f"  • Withdrawal: -${abs(amount):.2f}")

print(f"Total Deposited: ${total_deposits:.2f}")"""
    },
    "while": {
        "simple_definition": "`while` keeps repeating a block of code over and over as long as its condition remains True. It stops as soon as the condition turns False.",
        "title": "Real-world: API Connection Retry Loop with Backoff",
        "code": """# Real-world: Retrying a network request up to 3 times
attempts = 0
max_retries = 3
connected = False

while not connected and attempts < max_retries:
    attempts += 1
    print(f"Attempt {attempts}/{max_retries}: Connecting to database...")
    # Simulating connection succeeding on attempt 2
    if attempts == 2:
        connected = True
        print("✓ Connected successfully!")

if not connected:
    print("❌ Failed to connect after max retries.")"""
    },
    "try": {
        "simple_definition": "`try` wraps code that might cause an error so you can catch the error gracefully with `except` instead of letting your program crash.",
        "title": "Real-world: Parsing User Input Without Crashing",
        "code": """# Real-world: Parsing integers from dirty external data
inputs = ["42", "100", "invalid_num", "99"]
clean_numbers = []

for item in inputs:
    try:
        val = int(item)
        clean_numbers.append(val)
        print(f"✓ Parsed number: {val}")
    except ValueError:
        print(f"⚠️ Skipping invalid data: '{item}'")

print(f"Successfully collected numbers: {clean_numbers}")"""
    },
    "with": {
        "simple_definition": "`with` manages resources (like files, database locks, or network connections) automatically, ensuring they are cleanly closed even if an error occurs.",
        "title": "Real-world: Safe File Handling with Automatic Cleanup",
        "code": """# Real-world: Writing and reading a temporary log safely
import tempfile

with tempfile.NamedTemporaryFile(mode="w+", delete=True) as tmp:
    tmp.write("2024-09-28 INFO: Application booted successfully\\n")
    tmp.seek(0)
    contents = tmp.read()
    print("Temporary log output:")
    print(contents.strip())
# File automatically closed and deleted upon leaving the with block"""
    },
    "lambda": {
        "simple_definition": "`lambda` creates a compact, anonymous (unnamed) one-line function on the fly. It's often used as an argument to functions like `sorted()`, `map()`, or `filter()`.",
        "title": "Real-world: Sorting Products by Multiple Keys",
        "code": """# Real-world: Sorting employees by department, then salary
employees = [
    {"name": "Alice", "dept": "Engineering", "salary": 95000},
    {"name": "Bob", "dept": "Marketing", "salary": 72000},
    {"name": "Charlie", "dept": "Engineering", "salary": 110000}
]

# Sort by salary ascending using lambda
by_salary = sorted(employees, key=lambda e: e["salary"])
for emp in by_salary:
    print(f"${emp['salary']:,} - {emp['name']} ({emp['dept']})")"""
    },
    "pass": {
        "simple_definition": "`pass` does absolutely nothing. It is a placeholder used when Python syntax requires a code block (like in an empty function or loop) but you aren't ready to write the code yet.",
        "title": "Real-world: Scaffolded API Service Interface",
        "code": """# Real-world: Creating an abstract payment provider template
class PaymentProvider:
    def process_credit_card(self, card_number, amount):
        pass  # TODO: Integrate Stripe SDK here

    def process_crypto(self, wallet_address, amount):
        pass  # TODO: Integrate Coinbase Commerce here

print("PaymentProvider interface declared without syntax errors.")"""
    },
    "raise": {
        "simple_definition": "`raise` deliberately triggers an error (exception) in your program, signaling that something unexpected or invalid happened.",
        "title": "Real-world: Enforcing Business Validation Rules",
        "code": """# Real-world: Rejecting negative account balances
def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("Withdrawal amount must be strictly positive.")
    if amount > balance:
        raise ValueError(f"Insufficient funds: Balance is ${balance}, requested ${amount}.")
    return balance - amount

try:
    current_balance = 50.00
    print("Attempting to withdraw $100...")
    withdraw(current_balance, 100.00)
except ValueError as err:
    print(f"Transaction Rejected: {err}")"""
    },
    "assert": {
        "simple_definition": "`assert` tests an expression as a sanity check. If the expression evaluates to False, Python immediately halts and raises an `AssertionError`.",
        "title": "Real-world: Internal State & Input Invariant Checks",
        "code": """# Real-world: Validating that discount ratios never exceed 100%
def apply_promo(subtotal, discount_ratio):
    assert 0.0 <= discount_ratio <= 1.0, f"Invalid discount ratio: {discount_ratio}"
    return round(subtotal * (1 - discount_ratio), 2)

final = apply_promo(100.0, 0.20)
print(f"$100 with 20% promo: ${final}")"""
    },
    "global": {
        "simple_definition": "`global` tells Python that a variable inside a function refers to the top-level (module-wide) variable, allowing you to modify it instead of creating a local copy.",
        "title": "Real-world: Global Application Request Counter",
        "code": """# Real-world: Incrementing an application-wide request counter
request_count = 0

def record_api_call(route):
    global request_count
    request_count += 1
    print(f"Request #{request_count}: Accessed {route}")

record_api_call("/api/users")
record_api_call("/api/checkout")
print(f"Total server hits: {request_count}")"""
    },
    "nonlocal": {
        "simple_definition": "`nonlocal` tells Python that a variable inside a nested function refers to a variable in the outer enclosing function (not global, but not local either).",
        "title": "Real-world: Stateful ID Generator Closure",
        "code": """# Real-world: Creating a ticket sequence generator closure
def make_ticket_generator(prefix="TICKET"):
    next_id = 1000
    def generate():
        nonlocal next_id
        current = f"{prefix}-{next_id}"
        next_id += 1
        return current
    return generate

ticket_issuer = make_ticket_generator("SUPPORT")
print("Issued:", ticket_issuer())
print("Issued:", ticket_issuer())
print("Issued:", ticket_issuer())"""
    }
}

# Plain-English definitions and realistic code examples for common built-in Exceptions
EXCEPTION_CATALOG = {
    "KeyError": {
        "simple_definition": "`KeyError` happens when you try to look up a key in a dictionary that doesn't exist. You can prevent it with `dict.get(key, default)` or catch it with `try/except`.",
        "title": "Real-world: Safe Dictionary Lookup with Fallback",
        "code": """# Real-world: Handling missing keys in an API response
user_data = {"id": 101, "name": "Sarah"}

try:
    role = user_data["role"]
except KeyError:
    role = "guest"  # Safe fallback
    print("KeyError caught: 'role' key was missing, defaulted to 'guest'.")

print(f"User: {user_data['name']} | Role: {role}")"""
    },
    "ValueError": {
        "simple_definition": "`ValueError` happens when a function receives an argument that has the right type, but an inappropriate or invalid value (like trying to convert `'abc'` to an `int`).",
        "title": "Real-world: Validating User Form Inputs",
        "code": """# Real-world: Catching invalid numerical input from a web form
raw_input = "not_a_number"

try:
    age = int(raw_input)
except ValueError as err:
    print(f"ValueError: Could not convert '{raw_input}' to integer.")
    age = 18  # Default minimum age

print(f"Proceeding with age: {age}")"""
    },
    "TypeError": {
        "simple_definition": "`TypeError` happens when an operation or function is applied to an object of an inappropriate type (like trying to add a number and a string).",
        "title": "Real-world: Catching Incompatible Data Types",
        "code": """# Real-world: Safely adding price and quantity across string/number types
def compute_line_total(price, quantity):
    try:
        return price * quantity
    except TypeError:
        # Convert strings if needed
        return float(price) * int(quantity)

print("Total 1:", compute_line_total(19.99, 2))
print("Total 2:", compute_line_total("19.99", "3"))"""
    },
    "IndexError": {
        "simple_definition": "`IndexError` happens when you try to access an item from a list or sequence at an index number that is out of range (like grabbing item 10 from a 3-item list).",
        "title": "Real-world: Safely Reading Command-Line Arguments",
        "code": """# Real-world: Safely getting an element from a list with bounds check
commands = ["start", "--verbose"]

try:
    mode = commands[2]
except IndexError:
    mode = "--normal"  # Default fallback
    print("IndexError: Missing third argument, defaulted to '--normal'.")

print("Run mode:", mode)"""
    },
    "ZeroDivisionError": {
        "simple_definition": "`ZeroDivisionError` happens when you attempt to divide a number by zero or perform a modulo (`%`) by zero, which is mathematically undefined.",
        "title": "Real-world: Calculating Click-Through Rates (CTR)",
        "code": """# Real-world: Safely calculating conversion rates when visits are zero
clicks = 15
impressions = 0

try:
    ctr = (clicks / impressions) * 100
except ZeroDivisionError:
    ctr = 0.0
    print("ZeroDivisionError: No impressions recorded yet, CTR is 0.0%")

print(f"Conversion rate: {ctr:.1f}%")"""
    },
    "FileNotFoundError": {
        "simple_definition": "`FileNotFoundError` happens when you try to open or delete a file that does not exist at the specified path.",
        "title": "Real-world: Loading Optional Config File with Default",
        "code": """# Real-world: Gracefully falling back when a config file is absent
import json

try:
    with open("app_settings.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    config = {"theme": "dark", "version": "1.0.0"}
    print("FileNotFoundError: app_settings.json not found. Using default config.")

print("Loaded config:", config)"""
    }
}
