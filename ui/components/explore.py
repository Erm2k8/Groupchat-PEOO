from ctypes import alignment
from multiprocessing import Value
from turtle import width
import streamlit as st
from views.views import View

class Explore:
    @staticmethod
    def search():
        if "search" not in st.session_state:
            st.session_state.search = ""

        search = st.text_input("Buscar grupo", value="", key="search")

        if search != st.session_state.search:
            st.session_state.search = search
        
        if st.session_state.search:
            for group in View.search_groups(st.session_state.search):
                if st.session_state.search.lower() in group.group_name.lower():
                    with st.container(border=True):
                        col1, col2= st.columns([7, 1])
                        with col1:
                            st.markdown("#### " + group.group_name)
                        with col2:
                            st.button("Pedir pra entrar")


