import streamlit as st
from views.views import View
from ui.components.group import Groups

class Sidebar:
    @staticmethod
    def render():
        with st.sidebar:
            st.title("TriboPapo")
            explore = st.button("Explorar Tribos", use_container_width=True, type="primary", icon="🌎")
            create_group = st.button("Criar Grupo", use_container_width=True, type="secondary", icon="➕")

            if create_group:
                Groups.create_group()

            st.divider()
            st.write("Seus Grupos")

            groups = View.list_groups()
            user_groups = [group for group in groups if st.session_state.user_id in [member['user_id'] for member in group.members]]
            
            if explore:
                st.session_state.selected_group = "explore"
            if user_groups:
                for group in user_groups:
                    group_button = st.button(group.group_name, use_container_width=True)
                    if group_button:
                        st.session_state.selected_group = group.group_name
                        st.rerun()
            else:
                st.write("Você ainda não participa de nenhum grupo.")
            
            st.divider()
            if st.button("Logout"):
                st.session_state.clear()
                st.rerun()