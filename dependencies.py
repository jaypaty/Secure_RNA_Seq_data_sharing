import streamlit as st
import streamlit_authenticator as stauth
import datetime
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Load the service account key
if not firebase_admin._apps:
    cred = credentials.Certificate("./your-firebase-adminsdk-xyz123-xzy123.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def insert_user(email, username, password):
    """
    Inserts Users into Firestore with hashed passwords
    """
    try:
        date_joined = str(datetime.datetime.now())

        # Hash the password before inserting into Firestore
        hashed_password = stauth.Hasher([password]).generate()[0]  # Only use the first generated hash

        return db.collection('users').add({
            'email': email,
            'username': username,
            'password': hashed_password,  # Store the hashed password
            'date_joined': date_joined
        })
        st.success("Account created successfully!")
    except Exception as e:
        st.error(f"Error creating user: {e}")

# the line below tests successful insertion of given user in our firebase DB
# insert_user("test@gmail.com", "2te2est", "11112222")

# Function to fetch users from Firestore
def fetch_users():
    users_ref = db.collection('users')
    users = [doc.to_dict() for doc in users_ref.stream()]
    return users

# # following line tests the fetch user function from our cloud DB
# # print(fetch_users())# Streamlit Form for Sign Up

def sign_up():
    st.subheader("Sign Up")
    with st.form(key='signup_form', clear_on_submit=True):
        email = st.text_input('Email', placeholder='Enter your email')
        username = st.text_input('Username', placeholder='Enter your username')
        password = st.text_input('Password', placeholder='Enter your password', type='password')
        confirm_password = st.text_input('Confirm Password', placeholder='Re-enter your password', type='password')
        submit_button = st.form_submit_button(label='Sign Up')

        if submit_button:
            if password == confirm_password:
                insert_user(email, username, password)
            else:
                st.warning("Passwords do not match")
