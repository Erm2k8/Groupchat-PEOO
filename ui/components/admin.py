import streamlit as st

class Admin:
    @staticmethod
    def render_admin_page():
        st.title("Admin Page")
        st.write("You are logged in as an admin.")