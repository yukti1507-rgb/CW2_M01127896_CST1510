import streamlit as st
from main import require_login

require_login()

st.set_page_config(page_title='Dashboard', layout='wide')

st.title(f"Welcome back, {st.session_state.username}!")