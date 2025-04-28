# firebase_config.py

import firebase_admin
from firebase_admin import credentials, firestore
import requests

# --- Firebase Admin SDK Initialization (For Firestore Database) ---

# Initialize Firebase Admin SDK only if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")  # your downloaded service account key
    firebase_admin.initialize_app(cred)

# Firestore Database Client
db = firestore.client()

# --- Firebase Authentication via REST API (for signup/login) ---

# Web API Key from Firebase Project Settings -> General -> Web API Key
API_KEY = "AIzaSyBI63zXcsfNdtz2pHOclOwF5xZad9jtdfo"  # 🔥 Replace with your Web API key here

# Firebase Authentication Endpoints
FIREBASE_AUTH_SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
FIREBASE_AUTH_SIGNIN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"

def signup_user(email, password):
    """Sign up a new user to Firebase Authentication"""
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(FIREBASE_AUTH_SIGNUP_URL, data=payload)
    return response.json()

def login_user(email, password):
    """Login an existing user to Firebase Authentication"""
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(FIREBASE_AUTH_SIGNIN_URL, data=payload)
    return response.json()
