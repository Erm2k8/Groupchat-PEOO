import streamlit as st
from views.views import View

class Auth:
    @staticmethod    
    def render_login_form():
        st.title("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            user = View.authenticate_user(email, password)
            if user:
                st.session_state.user_id = user["id"]
                st.session_state.user_name = user["name"]
                st.session_state.authenticated = True
                st.success("Login successful!")
                st.rerun()

    @staticmethod
    def render_register_form():
        st.title("Register")
        name = st.text_input("Name", key="register_name")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        if st.button("Register"):
            if name and email and password:
                View.create_user(name, email, password)
                user = View.authenticate_user(email, password)
                if user:
                    st.session_state.user_id = user["id"]
                    st.session_state.user_name = user["name"]
                    st.session_state.authenticated = True
                    st.success("Registration successful! Redirecting to main page...")
                    st.rerun()

    @staticmethod
    def render_logout_button():
        if "authenticated" in st.session_state and st.session_state.authenticated:
            if st.button("Logout"):
                st.session_state.clear()
                st.success("Logged out successfully!")
                st.rerun()

    @staticmethod
    def is_authenticated():
        return st.session_state.get('authenticated', False)
    
    @staticmethod
    def render_page():
        if Auth.is_authenticated():
            Auth.render_logout_button()
        else:
            page = st.selectbox("Choose action", ["Login", "Register"])
            if page == "Login":
                Auth.render_login_form()
            elif page == "Register":
                Auth.render_register_form()
