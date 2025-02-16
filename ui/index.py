import streamlit as st
from ui.components.sidebar import Sidebar
from ui.components.group import Groups
from ui.components.auth import Auth

st.set_page_config(
    page_title="TriboPapo",
    page_icon="😎",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    },
)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'selected_group' not in st.session_state:
    st.session_state.selected_group = None

def main():
    if not Auth.is_authenticated():
        Auth.render_page()
    else:
        Sidebar.render()  
        if st.session_state.selected_group:
            Groups.render_group(st.session_state.selected_group)
        else:
            st.write("Select a group to get started.")

if __name__ == "__main__":
    main()
