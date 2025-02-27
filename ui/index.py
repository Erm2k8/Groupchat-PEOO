import streamlit as st
from .styles import Style
from ui.components.admin import AdminUI
from ui.components.sidebar import Sidebar
from ui.components.group import Groups
from ui.components.auth import Auth
from ui.components.explore import Explore

class Index:
    @staticmethod
    def main():
        Style.global_render()

        if not Auth.is_authenticated():
            Auth.render_page()
        else:
            col1, col2 = st.columns([8, 2])

            with col1:
                if not st.session_state.authenticated_is_admin:
                    Sidebar.render()  
                    if st.session_state.selected_group != "explore":
                        Style.padding__adjust_render()
                        Groups.render_group(st.session_state.selected_group)
                    else:
                        Explore.search()
                else:
                    st.title("Admin page")
                    AdminUI.render()


if __name__ == "__main__":
    Index.main()
