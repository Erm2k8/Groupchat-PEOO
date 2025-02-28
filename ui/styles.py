import streamlit as st

class Style:
    global_style = """
        <style>
            *:not[.stSelectbox] {
                overflow: hidden;
            }
        </style>
    """

    padding_adjustment = """
        <style>
            .stMainBlockContainer {
                padding-top: 2rem;
                padding-left: 5rem;
            }
        </style>
    """
    
    @classmethod
    def global_render(cls):
        st.markdown(cls.global_style, unsafe_allow_html=True)

    @classmethod
    def padding_adjust_render(cls):
        st.markdown(cls.padding_adjustment, unsafe_allow_html=True)