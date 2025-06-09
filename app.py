from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import requests
import re
import json
import os
from datetime import datetime

app = Flask(__name__, static_folder='.')
CORS(app)

# eBay API credentials (replace with your actual credentials)
EBAY_APP_ID = "Satyapuj-uplyftta-SBX-0470f8933-19768344"
EBAY_SANDBOX_URL = "https://svcs.sandbox.ebay.com/services/search/FindingService/v1"
# Replace with your OAuth token (generate from eBay Developer Portal)
EBAY_OAUTH_TOKEN = "v^1.1#i^1#r^0#I^3#f^0#p^3#t^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"  # Replace with your Sandbox OAuth token

  # Replace with your Sandbox OAuth token

# SQLite Database Setup
def init_db():
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions
                 (session_id TEXT PRIMARY KEY, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS preferences
                 (user_id INTEGER, category TEXT, FOREIGN KEY(user_id) REFERENCES users(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS purchases
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, item_id TEXT, item_title TEXT, price REAL, purchase_date TEXT,
                 FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

init_db()

# Serve index.html
@app.route('/')
def serve_index():
    try:
        print("Serving index.html")
        return send_from_directory('.', 'index.html')
    except Exception as e:
        print(f"Error serving index.html: {e}")
        return jsonify({'error': 'Failed to load frontend'}), 500

# Helper Functions
def get_user_id(session_id):
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute("SELECT user_id FROM sessions WHERE session_id = ?", (session_id,))
    result = c.fetchone()
    conn.close()
    print(f"Session ID {session_id} mapped to user_id: {result[0] if result else 'None'}")  # Debug log
    return result[0] if result else None

def get_user_preferences(user_id):
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute("SELECT category FROM preferences WHERE user_id = ?", (user_id,))
    result = c.fetchall()
    conn.close()
    return [row[0] for row in result]

def save_user_preference(user_id, category):
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO preferences (user_id, category) VALUES (?, ?)", (user_id, category))
    conn.commit()
    conn.close()

def save_purchase(user_id, item_id, item_title, price):
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    purchase_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO purchases (user_id, item_id, item_title, price, purchase_date) VALUES (?, ?, ?, ?, ?)",
              (user_id, item_id, item_title, price, purchase_date))
    conn.commit()
    # Debug: Verify the purchase was saved
    c.execute("SELECT * FROM purchases WHERE user_id = ? AND item_id = ?", (user_id, item_id))
    saved_purchase = c.fetchone()
    print(f"Saved purchase for user_id {user_id}: {saved_purchase}")
    conn.close()

def get_user_purchases(user_id):
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute("SELECT item_id, item_title, price, purchase_date FROM purchases WHERE user_id = ?", (user_id,))
    result = c.fetchall()
    conn.close()
    purchases = [{"item_id": row[0], "title": row[1], "price": row[2], "purchase_date": row[3]} for row in result]
    print(f"Retrieved purchases for user_id {user_id}: {purchases}")  # Debug log
    return purchases

# eBay API Helper Functions
def search_ebay_products(query, category=None, max_price=None):
    headers = {
        "Authorization": f"Bearer {EBAY_OAUTH_TOKEN}",
        "X-EBAY-API-SITEID": "0",  # 0 for US
        "Content-Type": "application/json"
    }
    params = {
        "OPERATION-NAME": "findItemsByKeywords",
        "SERVICE-VERSION": "1.0.0",
        "SECURITY-APPNAME": EBAY_APP_ID,
        "RESPONSE-DATA-FORMAT": "JSON",
        "REST-PAYLOAD": "",
        "keywords": query,
        "paginationInput.entriesPerPage": 3
    }
    if category:
        params["categoryId"] = category

    try:
        response = requests.get(EBAY_SANDBOX_URL, headers=headers, params=params)
        if response.status_code != 200:
            print(f"eBay API error: HTTP {response.status_code} - {response.text}")
            return []
        data = response.json()
        print(f"eBay API raw response: {json.dumps(data, indent=2)}")  # Log raw response for debugging
        items = data.get("findItemsByKeywordsResponse", [{}])[0].get("searchResult", [{}])[0].get("item", [])
        products = []
        for item in items:
            image_url = item.get("galleryURL", [""])[0]
            if not image_url:  # Fallback if image URL is empty
                image_url = "https://via.placeholder.com/150?text=Image+Not+Available"
            product = {
                "id": item.get("itemId", [""])[0],
                "name": item.get("title", [""])[0],
                "price": float(item.get("sellingStatus", [{}])[0].get("currentPrice", [{}])[0].get("value", "0")),
                "image": image_url
            }
            print(f"Product image URL: {product['image']}")  # Debug log for image URL
            products.append(product)
        # Fallback price if $0 (Sandbox issue)
        for product in products:
            if product["price"] == 0:
                product["price"] = 999.99  # Fallback price
        # Filter by max_price if specified
        if max_price is not None:
            products = [p for p in products if p["price"] <= max_price]
        return products
    except Exception as e:
        print(f"eBay API error: {e}")
        return []

# Intent Detection
def detect_intent(message):
    message = message.lower().strip()
    # Check for price-based query (e.g., "laptops under $1000")
    price_match = re.search(r"under \$(\d+)", message)
    if price_match:
        max_price = float(price_match.group(1))
        query = message[:message.find("under $")].strip()  # Extract query before "under $X"
        return "price_search", query, max_price

    if "show my orders" in message:
        return "show_orders"
    if message.startswith("buy "):
        return "buy", message[4:].strip()
    if "cheapest" in message:
        return "cheapest", message.replace("cheapest", "").strip()
    if "electronics" in message or "jewelery" in message or "clothing" in message:
        return "category_search", message
    return "general_search", message

# API Endpoints
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return jsonify({"message": "Signup successful"}), 200
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    if user:
        session_id = os.urandom(16).hex()
        c.execute("INSERT INTO sessions (session_id, user_id) VALUES (?, ?)", (session_id, user[0]))
        conn.commit()
        conn.close()
        return jsonify({"user": {"id": user[0], "username": username}, "session_id": session_id}), 200
    conn.close()
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/signout', methods=['POST'])
def signout():
    data = request.get_json()
    session_id = data.get('session_id')
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Signed out successfully"}), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message')
    session_id = data.get('session_id')
    user_id = data.get('user_id')

    if not user_id or not session_id:
        return jsonify({"error": "Not authenticated"}), 401

    # Verify user_id matches session_id
    actual_user_id = get_user_id(session_id)
    if actual_user_id != int(user_id):
        print(f"User ID mismatch: session_id {session_id} expected user_id {actual_user_id}, got {user_id}")
        return jsonify({"error": "Invalid session"}), 401

    intent, *args = detect_intent(message)

    if intent == "show_orders":
        orders = get_user_purchases(user_id)
        if not orders:
            return jsonify({"reply": "You haven't made any purchases yet."}), 200
        return jsonify({"reply": "Here are your orders:", "orders": orders}), 200

    if intent == "buy":
        item_name = args[0]
        products = search_ebay_products(item_name)
        if not products:
            return jsonify({"reply": f"Sorry, I couldn't find {item_name}."}), 200
        product = products[0]  # Simulate buying the first match
        save_purchase(user_id, product["id"], product["name"], product["price"])
        return jsonify({"reply": f"You've successfully purchased {product['name']} for ${product['price']}!" }), 200

    if intent == "cheapest":
        query = args[0]
        products = search_ebay_products(query)
        if not products:
            return jsonify({"reply": f"No products found for {query}."}), 200
        cheapest = min(products, key=lambda x: x["price"])
        return jsonify({"reply": f"The cheapest {query} is {cheapest['name']} for ${cheapest['price']}.", "products": [cheapest]}), 200

    if intent == "category_search":
        category = "electronics" if "electronics" in message else "jewelery" if "jewelery" in message else "clothing"
        save_user_preference(user_id, category)
        products = search_ebay_products(category)
        if not products:
            return jsonify({"reply": f"Sorry, I couldn't find any {category} items."}), 200
        return jsonify({
            "reply": f"Looks like you're interested in {category}! Here are some options:",
            "products": products,
            "recommendation": f"Since you like {category}, you might also enjoy similar items."
        }), 200

    if intent == "price_search":
        query, max_price = args
        products = search_ebay_products(query, max_price=max_price)
        if not products:
            return jsonify({"reply": f"Sorry, I couldn't find any {query} under ${max_price}."}), 200
        return jsonify({
            "reply": f"Here are some {query} under ${max_price}:",
            "products": products
        }), 200

    # General search
    products = search_ebay_products(message)
    if not products:
        return jsonify({"reply": f"Sorry, I couldn't find anything for '{message}'."}), 200
    preferences = get_user_preferences(user_id)
    recommendation = f"Based on your interest in {preferences[0] if preferences else 'various categories'}, you might like these." if preferences else None
    return jsonify({
        "reply": f"Here are some results for '{message}':",
        "products": products,
        "recommendation": recommendation
    }), 200

if __name__ == '__main__':
    app.run(debug=True)