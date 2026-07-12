import streamlit as st
from app_model.db import get_connection
from app_model.users import add_user, get_user, get_email, generate_hash
def register_page():
    st.title("Create Account")

    with st.form("register_form"):
        username  = st.text_input("Choose a username")
        email = st.text_input("Enter your email:")
        st.warning("Email should follow the following format: 'abc123@email.com'")
        password   = st.text_input("Choose a password", type="password")
        st.warning("Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
        confirm_password  = st.text_input("Confirm password",  type="password")
        submitted = st.form_submit_button("Register")
    
    letters_only = ""
    for char in username:
        if char.isalpha():
            letters_only += char
    
    username_errors = []
    email_errors = []
    password_successes = []
    password_errors = []

    if submitted:
        if not username:
            username_errors.append("Username is required.")
            return
        
        if not email:
            email_errors.append("Email is required.")
            return
        
        if not password:
            password_errors.append("Password is required.")
            return
        
        if not confirm_password:
            password_errors.append("Confirmation of password is required.")
            return
        
        
        if username.lower() == "admin":
            username_errors.append("This username is reserved. Please choose another.")
        
        if "@" not in email or "." not in email:
            email_errors.append("Please enter a valid email address using the given format.")
            
        conn = get_connection()

        try:
            existing_user = get_user(conn, username)
            existing_email = get_email(conn, email)

            if existing_user and existing_email:
                username_errors.append("An account with these details already existes. Please log in instead.")

            elif existing_user: # if user exists
                username_errors.append("Username is already taken. Please choose another.")

            elif existing_email: #if email in database
                email_errors.append("This email is already registered. Please log in instead.")    
            
        finally:
            conn.close()

        if username_errors:
            st.error("Username constraints:\n\n" + "\n".join(username_errors))
        
        if email_errors:
            st.error("Email constraints:\n\n" + "\n".join(email_errors))
        
        if username_errors or email_errors:
            return

        if password != confirm_password:
            password_errors.append("Passwords do not match.")
        
        if len(password) >= 8:
            password_successes.append("At least 8 characters long.")
        else:
            password_errors.append("At least 8 characters long.")

        if any(c.isupper() for c in password):
            password_successes.append("At least one uppercase letter.")
        else:
            password_errors.append("At least one uppercase letter.")

        if any(c.islower() for c in password):
            password_successes.append("At least one lowercase letter.")
        else:
            password_errors.append("At least one lowercase letter.")

        if any(c.isdigit() for c in password):
            password_successes.append("At least one number.")
        else:
            password_errors.append("At least one number.")

        if any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in password):
            password_successes.append("At least one special character.")
        else:
            password_errors.append("At least one special character.")
           
        if username.lower() in password.lower():
            password_errors.append("Cannot contain your username.")
           
        if letters_only and letters_only.lower() in password.lower():
            password_errors.append("Cannot be similar to username.")
            
        if "password" in password.lower():
            password_errors.append("Cannot contain the word 'password'.")
        
        if password_successes:
            st.success("Password requirements met:\n\n" + "\n\n".join(password_successes))

        if password_errors:
            st.error("Password issues:\n\n" + "\n\n".join(password_errors))
            return
        

        conn = get_connection()
        try:
            add_user(conn, username, email, generate_hash(password))   
            st.success(f" Account created! Please log in.")
        except Exception as e:
            st.error(f"Username or email already exists.")  
        finally:
            conn.close()

register_page()

st.write("Already have an account? Log in.")
if st.button("Log in"):
    st.switch_page("main.py")