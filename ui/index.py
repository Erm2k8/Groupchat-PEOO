import streamlit as st
from .styles import Style
from ui.components.sidebar import Sidebar
from ui.components.group import Groups
from ui.components.auth import Auth

class Index:
    @staticmethod
    def main():
        Style.render()

        if not Auth.is_authenticated():
            Auth.render_page()
        else:
            col1, col2 = st.columns([8, 2])

            with col1:

                if not st.session_state.authenticated_is_admin:
                    Sidebar.render()  
                    if st.session_state.selected_group != "explore":
                        Groups.render_group(st.session_state.selected_group)
                    else:
                        st.write("Select a group to get started.")
                else:
                    st.title("Admin page")
                    Auth.render_logout_button()


if __name__ == "__main__":
    Index.main()
