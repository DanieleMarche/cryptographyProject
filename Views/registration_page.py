from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import bcrypt
import jwt
import hmac
import hashlib
import base64
import os

app = Flask(__name__)

# Supabase config
SUPABASE_URL = "https://ldbsmswgtwtkxduqmoip.supabase.co/rest/v1/User"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxkYnNtc3dndHd0a3hkdXFtb2lwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjk2MDI5ODEsImV4cCI6MjA0NTE3ODk4MX0.7GndoQP5VHZx1dAfMwcLMlmJjwUcEsFMsuZLv77mG0k"
JWT_SECRET = "BVtIFgbuvhiNIWNNcJ73eSNwG5cP+eBO9vXyCJqvo8H8XQ/B795DpA2qQqvjAopde1j8oQZOXKVTiHgqwnIZUg=="

headers = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


# HMAC Function to verify message authenticity
def generate_hmac(message, key):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()


# User Registration Route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Hashing password with bcrypt
    hashed_password = generate_password_hash(password, method='bcrypt')

    # Prepare data to store in Supabase
    user_data = {
        "username": username,
        "password": hashed_password
    }

    # Save user in Supabase
    response = requests.post(SUPABASE_URL, headers=headers, json=user_data)

    if response.status_code == 201:
        return jsonify({"message": "User registered successfully!"}), 201
    else:
        return jsonify({"error": "Error registering user"}), 400


# User Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Fetch user from Supabase
    response = requests.get(SUPABASE_URL + f"?username=eq.{username}", headers=headers)
    user = response.json()

    if user and check_password_hash(user[0]['password'], password):
        # Generate JWT token
        token = jwt.encode({"username": username}, JWT_SECRET, algorithm='HS256')
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


# Transaction route with HMAC protection
@app.route('/transaction', methods=['POST'])
def transaction():
    data = request.get_json()
    message = data['message']
    key = os.getenv('HMAC_KEY', 'default_hmac_key')

    # Generate HMAC for the message
    hmac_signature = generate_hmac(message, key)

    return jsonify({"message": message, "hmac": hmac_signature})


if __name__ == "__main__":
    app.run(debug=True)

