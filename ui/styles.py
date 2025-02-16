import streamlit as st

class Style:
    style = """
        <style>
            * {
                overflow: hidden;
            }

            .stMainBlockContainer {
                padding-top: 2rem;
                padding-left: 5rem;

            }
        </style>
    """
    
    @classmethod
    def render(cls):
        st.markdown(cls.style, unsafe_allow_html=True)