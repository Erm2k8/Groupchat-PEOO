import streamlit as st
from views.views import View

class Sidebar:
    @staticmethod
    def render():
        with st.sidebar:
            st.title("TriboPapo")
            explore = st.button("Explorar Tribos", use_container_width=True, type="primary")
            st.divider()
            st.write("Your Groups")
            
            groups = View.list_groups()
            
            if explore:
                st.session_state.selected_group = "explore"
            if groups:
                for group in groups:
                    group_button = st.button(group.group_name, use_container_width=True)
                    if group_button:
                        st.session_state.selected_group = group.group_name
                        st.rerun()
            else:
                st.write("No groups found.")
            
            st.divider()
            st.button("Logout", on_click=lambda: st.session_state.clear())
