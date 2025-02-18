import streamlit as st
from views.views import View
from models.admin import Admin
import uuid

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
            else:  
                st.error("Usuário não encontrado.")

    @staticmethod
    def render_register_form():
        st.title("Register")
        name = st.text_input("Name", key="register_name")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        if st.button("Register"):
            if name and email and password:
                try:
                    View.create_user(name, email, password)
                    user = View.authenticate_user(email, password)
                    if user:
                        st.session_state.user_id = user["id"]
                        st.session_state.user_name = user["name"]
                        st.session_state.authenticated = True
                        st.success("Registration successful! Redirecting to main page...")
                        st.rerun()
                except Exception as e:
                    st.error(f"{e} Insira todos os campos corretamente.")
            else:
                st.warning("Preencha todos os campos para continuar")

    @staticmethod
    def render_admin_page():
        st.title("Admin")
        username = st.text_input("Username", key="admin_username")
        password = st.text_input("Password", type="password", key="admin_password")
        if st.button("Login as Admin"):
            if Admin.authenticate_admin(username, password):
                st.session_state.authenticated = True
                st.session_state.authenticated_is_admin = True
                st.success("Admin login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials.")

    @staticmethod
    def render_logout_button():
        if st.session_state.get("authenticated") or st.session_state.get("authenticated_is_admin"):

            if st.button("Logout", key="logout_button"):
                st.session_state.clear()
                st.success("Logout realizado com sucesso!")
                st.rerun()

    @staticmethod
    def is_authenticated():
        return st.session_state.get('authenticated', False)
    
    @staticmethod
    def render_page():
        col1, col2, col3 = st.columns([1, 1, 1])

        if Auth.is_authenticated():
            Auth.render_logout_button()
        else:
            with col2:
                if Auth.is_authenticated():
                    Auth.render_logout_button()
                else:
                    auth_type = st.selectbox("Login or Register", ["Login", "Register", "Admin"])
                    if auth_type == "Login":
                        Auth.render_login_form()
                    elif auth_type == "Register":
                        Auth.render_register_form()
                    elif auth_type == "Admin":
                        Auth.render_admin_page()

