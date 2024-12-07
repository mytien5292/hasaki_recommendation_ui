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

    return users_dict

@st.cache_data
def load_examples_users():
    old_users = pd.read_csv('data/old_users_login.csv')
    new_users = pd.read_csv('data/new_users_login.csv')

    old_users_examples = []
    new_users_examples = []

    for _, row in old_users.iterrows():
        old_users_examples.append(f"- username: {row['username']} - password: {row['password']}")

    for _, row in new_users.iterrows():
        new_users_examples.append(f"- username: {row['username']} - password: {row['password']}")

    return old_users_examples, new_users_examples

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
            #st.write(f'## Xin chào bạn *{st.session_state["name"].strip()}*')
            st.markdown(
    f"<h5>Xin chào <em>{st.session_state['name'].strip()}, chào mừng bạn đến thế giới làm đẹp cùng Hasaki!</em></h5>",
    unsafe_allow_html=True,
)
        main_content()
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')

        old_users_examples, new_users_examples = load_examples_users()
        
        st.write("### Ví dụ tài khoản cũ:")
        for example in old_users_examples[:5]:
            st.write(example)
        
        st.write("### Ví dụ tài khoản mới:")
        for example in new_users_examples[:5]:
            st.write(example)