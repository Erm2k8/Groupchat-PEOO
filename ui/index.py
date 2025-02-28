import streamlit as st
from .styles import Style
from ui.components.admin import AdminUI
from ui.components.sidebar import Sidebar
from ui.components.group import Groups
from ui.components.auth import Auth
from ui.components.explore import Explore
from views.views import View

class Index:
    @staticmethod
    def main():
        Style.global_render()

        if not Auth.is_authenticated():
            Auth.render_page()
        else:
            col1, col2 = st.columns([5, 2])

            with col1:
                if not st.session_state.authenticated_is_admin:
                    Sidebar.render()  
                    if st.session_state.selected_group != "explore":
                        Style.padding_adjust_render()
                        Groups.render_group(st.session_state.selected_group)
                    else:
                        Explore.search()
                else:
                    st.title("Admin page")
                    AdminUI.render()
            with col2:
                if st.session_state.authenticated and not st.session_state.authenticated_is_admin and not st.session_state.selected_group == "explore":
                    st.title("")
                    is_admin = View.is_user_group_admin(st.session_state.user_id, View.get_group_by_name(st.session_state.selected_group).id)
                    Groups.group_info(st.session_state.selected_group, user_is_admin=is_admin)
                    

if __name__ == "__main__":
    Index.main()
