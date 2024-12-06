import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd

import yaml
from yaml.loader import SafeLoader
from hasaki_recommendation_ui import main_content

@st.cache_data
def load_list_users():
    print("Loading users...")

    old_users = pd.read_csv('data/old_users_login.csv')
    new_users = pd.read_csv('data/new_users_login.csv')

    old_users_examples = []
    new_users_examples = []

    old_users = old_users[:20]

    users_dict = {
        "usernames": {}
    }

    for _, row in old_users.iterrows():
        users_dict["usernames"][row["username"]] = {
            "email": row["email"],
            "failed_login_attempts": 0,
            "first_name": row["ten_khach_hang"],
            "last_name": "",
            "logged_in": False,
            "password": row["password"],
            "roles": ["viewer"]
        }

        old_users_examples.append(f"- username: {row['username']} - password: {row['password']}")

    for _, row in new_users.iterrows():
        users_dict["usernames"][row["username"]] = {
            "email": row["email"],
            "failed_login_attempts": 0,
            "first_name": row["ten_khach_hang"],
            "last_name": "",
            "logged_in": False,
            "password": row["password"],
            "roles": ["viewer"]
        }

        new_users_examples.append(f"- username: {row['username']} - password: {row['password']}")

    st.session_state["old_users_examples"] = old_users_examples
    st.session_state["new_users_examples"] = new_users_examples

    return users_dict

def get_authenticator():
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Load user data and set credentials
    config['credentials'] = load_list_users()

    # Initialize authenticator
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    return authenticator

def login():
    if "authenticator" not in st.session_state:
        print("Loading login data...")
        st.session_state.authenticator = get_authenticator()
    
    authenticator = st.session_state.authenticator

    try:
        authenticator.login()
    except Exception as e:
        st.error(e)

    if st.session_state['authentication_status']:
        authenticator.logout()
        if st.session_state["name"]:
            st.write(f'## Welcome back *{st.session_state["name"].strip()}*')
        main_content()
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')

        if "old_users_examples" not in st.session_state:
            load_list_users()
        
        st.write("### Ví dụ tài khoản cũ:")
        for example in st.session_state.old_users_examples[:5]:
            st.write(example)
        
        st.write("### Ví dụ tài khoản mới:")
        for example in st.session_state.new_users_examples:
            st.write(example)