import streamlit as st
from app_model.db import get_connection
from app_model.schema import create_user_table
from app_model.users import delete_user, login_user_terminal, register_user_terminal, get_user, is_valid_hash, add_user, generate_hash



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
        name = st.text_input("Username")
        psw  = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        conn = get_connection()
        try:
            user = get_user(conn, name)
        except Exception as e:
            st.error(f"Error retrieving user: {e}")
        finally:
            conn.close()

        if user and is_valid_hash(psw, user[2]):
            st.session_state.logged_in = True
            st.session_state.username  = user[1]
            st.session_state.role      = user[3]
            st.switch_page("pages/1_Dashboard.py")    
            # Redirect on success
        else:
            st.error(" Incorrect username or password.")


def register_page():
    st.title("Create Account")

    with st.form("register_form"):
        name  = st.text_input("Choose a username")
        psw   = st.text_input("Choose a password", type="password")
        st.warning("Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
        psw2  = st.text_input("Confirm password",  type="password")
        submitted = st.form_submit_button("Register")
    
    letters_only = ""
    for char in name:
        if char.isalpha():
            letters_only += char
    

    if submitted:
        if not name or not psw:
            st.error("All fields are required.")
            return
        if name == "admin":
            st.error("This username is reserved. Please choose another.")
            return
        if psw != psw2:
            st.error("Passwords do not match.")
            return
        if len(psw) < 8:
            st.error("Password must be at least 8 characters long.")
            return
        if not any(c.isupper() for c in psw):
            st.error("Password must contain at least one uppercase letter.")
            return
        if not any(c.islower() for c in psw):
            st.error("Password must contain at least one lowercase letter.")
            return
        if not any(c.isdigit() for c in psw):
            st.error("Password must contain at least one number.")
            return
        if not any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in psw):
            st.error("Password must contain at least one special character.")
            return
        if name.lower() in psw.lower():
            st.error("Password cannot contain your username.")
            return
        if letters_only.lower() in psw.lower():
            st.error("Password cannot be similar to username.")
            return
        if "password" in psw.lower():
            st.error("Password cannot contain the word 'password'.")
            return
        

        conn = get_connection()
        try:
            add_user(conn, name, generate_hash(psw))   
            st.success(f" Account created! Please log in.")
            st.button("Go to Login Page", on_click=lambda: st.switch_page("main.py"))
        except Exception as e:
            st.error(f"Username already exists.")  
        finally:
            conn.close()

def require_login():
    if st.session_state.logged_in != True:
        st.warning("Please log in to access this page.")

        if st.button("Go to Login Page"):
            st.switch_page("main.py")  # Redirect to login page
        st.stop()  # Stop further execution of the page if not logged in
    
# SQL DATABASE
conn = get_connection()
user_table = create_user_table(conn)  # Ensure the users table exists
    
# STREAMLIT
st.set_page_config(page_title='Home', page_icon=':home:', layout='wide')

st.title("Welcome to Cyber Incidents Viewing Platform")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

st.write('''If you have an existing account, please log in.
Otherwise, please register to create an account.''')
tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    login_page()

with tab_register:
    register_page()
