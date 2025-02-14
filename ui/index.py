import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="TriboPapo",
    page_icon="😎",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    },
)

def main():
    # Styling for the main content and sidebar
    sidebar_style = '''
        <style>
        /* Main content styling */
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer.block-container > div > div > div > div > div:first-child {
            font-size: 16px;
            font-family: "Source Sans Pro", sans-serif;
            font-weight: 400;
            line-height: 1.6;
            text-size-adjust: 100%;
            -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
            -webkit-font-smoothing: auto;
            color: rgb(49, 51, 63);
            color-scheme: light;
            box-sizing: border-box;
            width: 550px !important;
            margin-right: 20px !important;
            flex: none !important;
        }
        
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer.block-container {
            max-width: 55rem;
        }

        /* Right sidebar styling */
        #right-sidebar-filters {
            text-size-adjust: 100%;
            -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
            -webkit-font-smoothing: auto;
            color-scheme: light;
            word-break: break-word;
            text-wrap: pretty;
            box-sizing: border-box;
            font-family: "Source Sans Pro", sans-serif;
            font-weight: 600;
            color: rgb(49, 51, 63);
            padding: 1.25rem 0px 1rem;
            margin: 0px;
            line-height: 1.2;
            font-size: 1.5rem;
            scroll-margin-top: 3.75rem;
        }

        /* Background color of column 3 (right column) */
        .css-1y4n1cn {
            background-color: #f0f8ff !important;  /* Alterar para a cor desejada */
            padding: 20px;
            border-radius: 10px;
        }

        /* Styling columns */
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer.block-container > div {
            margin-top: -40px;
        }
        </style>
    '''
    st.markdown(sidebar_style, unsafe_allow_html=True)

    # Left Sidebar - Filters
    with st.sidebar:
        st.title("Filtros")
        grupo = st.selectbox("Selecione um grupo", ["Grupo 1", "Grupo 2", "Grupo 3"])

    # Main Content Layout - with columns 
    col1, col2 = st.columns([3, 1])

    # Left Column (Main Content Area)
    with col1:
        usuario = "Usuário Exemplo"
        avatar_url = "https://www.w3schools.com/w3images/avatar2.png"  
        hora_envio = datetime.now().strftime("%H:%M:%S")

        mensagens = [
            "Olá, pessoal!",
            "Tudo bem com vocês?",
            "Que dia está maravilhoso!"
        ]

        for msg in mensagens:
            st.markdown(f"""
                <div style="border: 2px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 15px; background-color: #f9f9f9;">
                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                        <img src="{avatar_url}" alt="Avatar" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 10px;">
                        <div>
                            <strong>{usuario}</strong><br>
                            <small style="color: #888;">{hora_envio}</small>
                        </div>
                    </div>
                    <p>{msg}</p>
                </div>
            """, unsafe_allow_html=True)

    # Right Column (Sidebar Filters)
    with col2:
        st.title("Filtros Laterais")
        right_filter1 = st.selectbox("Selecione uma opção", ["Option 1", "Option 2", "Option 3"])
        right_filter2 = st.multiselect("Selecione múltiplas opções", ["Option A", "Option B", "Option C"])

        st.write("Opção Selecionada:", right_filter1)
        st.write("Opções Selecionadas:", right_filter2)

if __name__ == "__main__":
    main()
