import streamlit as st
from ui.index import Index

st.set_page_config(
    page_title="TriboPapo",
    page_icon="😎",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Mensagens e grupos de conversa",
    },
)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'selected_group' not in st.session_state:
    st.session_state.selected_group = "explore"

if 'authenticated_is_admin' not in st.session_state:
    st.session_state.authenticated_is_admin = False

if 'admin_selected_page' not in st.session_state:
    st.session_state.admin_selected_page = None


if __name__ == "__main__":
    Index.main()