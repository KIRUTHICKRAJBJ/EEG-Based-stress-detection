import streamlit as st
from main import stress_detection_app
import pyrebase

# --- Firebase Configuration ---
firebaseConfig = {
    "apiKey": "AIzaSyBI63zXcsfNdtz2pHOclOwF5xZad9jtdfo",
    "authDomain": "eeg-based-stress-detection.firebaseapp.com",
    "databaseURL": "https://eeg-based-stress-detection-default-rtdb.firebaseio.com/",
    "projectId": "eeg-based-stress-detection",
    "storageBucket": "eeg-based-stress-detection.appspot.com",
    "messagingSenderId": "560708215802",
    "appId": "1:560708215802:web:69feedb5843a7ce82dfa43",
    "measurementId": "G-N8EZBLP6XE"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth_fb = firebase.auth()

# --- Session State Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def add_custom_css():
    st.markdown("""
        <style>
        body {
            background-color: #f0f2f6;
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px;
            margin-top: 10px;
        }
        .stTextInput>div>div>input {
            padding: 10px;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

def login_signup_page():
    add_custom_css()
    st.markdown("<h1 style='text-align: center;'>🔐 EEG Stress Detection Login</h1>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 Login")
            username = st.text_input("Username", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            if st.button("Login"):
                try:
                    user = auth_fb.sign_in_with_email_and_password(username, password)
                    st.success("✅ Login Successful!")
                    st.session_state.logged_in = True
                    st.session_state.user_email = username  # Store email in session
                    st.session_state.page = "App"
                except Exception as e:
                    st.error("❌ Something went wrong. Please check your email and password.")
                    print(e)

        with col2:
            st.subheader("📝 Sign Up")
            new_username = st.text_input("New Email", key="new_username", placeholder="Enter your email")
            new_password = st.text_input("New Password", type="password", key="new_password", placeholder="Enter password")

            if st.button("Create Account"):
                try:
                    auth_fb.create_user_with_email_and_password(new_username, new_password)
                    st.success("✅ Account Created Successfully! Please login.")
                except Exception as e:
                    st.error("⚠️ Could not create account. Email might already exist or password is invalid.")
                    print(e)

def main_app():
    st.sidebar.subheader("Navigation")
    logout_button = st.sidebar.button("🚪 Logout")

    if logout_button:
        st.session_state.logged_in = False
        st.success("🟢 Logged Out Successfully!")

    if 'user_email' in st.session_state:
        stress_detection_app(st.session_state.user_email)
    else:
        st.error("User email not found in session. Please log in again.")

# --- Main ---
def main():
    if st.session_state.logged_in:
        main_app()
    else:
        login_signup_page()

if __name__ == "__main__":
    main()
