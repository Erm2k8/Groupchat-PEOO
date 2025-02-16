import streamlit as st

class Scripts:
    popup = """
        <script>
            alert("Hello, Streamlit!");
        </script>
    """

    @classmethod
    def popup_render(cls):
        st.markdown(cls.popup, unsafe_allow_html=True)