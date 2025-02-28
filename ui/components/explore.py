import streamlit as st
from views.views import View
import uuid

class Explore:
    @staticmethod
    def search():
        if "search" not in st.session_state:
            st.session_state.search = ""

        col1, col2 = st.columns([6, 1])
        with col1:
            search = st.text_input("", placeholder="Digite o nome do grupo", value=st.session_state.search, key="search_input", label_visibility="collapsed")
        with col2:
            search_button = st.button("Buscar", key="search_button", use_container_width=True)

        st.session_state.search = search

        groups_container = st.container()
        groups = View.search_groups(st.session_state.search)
        filtered_groups = []

        if st.session_state.search == "":
            filtered_groups = groups
        else:
            filtered_groups = [group for group in groups if st.session_state.search.lower() in group.group_name.lower()]

        with groups_container:
            for group in filtered_groups:
                with st.container(border=True):
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.markdown(f"#### {group.group_name}")
                    with col2:
                        is_member = st.session_state.user_id in [member['user_id'] for member in group.members]
                        if not is_member:
                            if st.button("Entrar", key=f"join_{group.id}", use_container_width=True):
                                View.add_member(group.id, st.session_state.user_id)
                                st.rerun()