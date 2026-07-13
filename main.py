import streamlit as st
from app_model.db import get_connection
from app_model.schema import create_user_table, create_login_history_table
from app_model.users import login_user_terminal, register_user_terminal, get_user, is_valid_hash, check_login_attempt, PASSWORD_HASH, USERNAME, ROLE


def main():
    while True:
        print('1. To Register\n2. To Log in\n3. To Exit')
        choice = input(': > ')
        if choice == '1':
            register_user_terminal()
        elif choice == '2':
            print('Login successful!' if login_user_terminal() else 'Incorrect login.')
        elif choice == '3':
            print('Goodbye!'); break
        
# To run on terminal, uncomment the following lines:
# if __name__ == '__main__':
#     main() 

def login_page():
    st.title("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password  = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        conn = get_connection()
        try:
            user = get_user(conn, username)
        finally:
            conn.close()

        if not user:
            st.error("Incorrect username or password.")
            return
        
        if is_valid_hash(password, user[PASSWORD_HASH]):
            st.session_state.logged_in = True
            st.session_state.username  = user[USERNAME]
            st.session_state.role      = user[ROLE]
            st.switch_page("pages/1_Dashboard.py")    
            # Redirect on success
        else:
            st.error(" Incorrect username or password.")
        
    st.subheader("New to the platform? Please create an account to continue.")
    if st.button("Create an account"):
        st.switch_page("pages/2_Register.py")

def require_login():
    if st.session_state.logged_in != True:
        st.warning("Please log in to access this page.")

        if st.button("Go to Login Page"):
            st.switch_page("main.py")  # Redirect to login page
        st.stop()  # Stop further execution of the page if not logged in
    
# SQL DATABASE
conn = get_connection()
user_table = create_user_table(conn)
login_history_table = create_login_history_table(conn) 
conn.close()
    
# STREAMLIT
st.set_page_config(page_title='Home', page_icon=':home:', layout='wide')

st.title("Welcome to Cyber Incidents Viewing Platform")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

login_page()

