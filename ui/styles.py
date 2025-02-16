import streamlit as st

class Style:
    style = """
        ...
    """
    
    @classmethod
    def render(cls):
        st.markdown(cls.style, unsafe_allow_html=True)