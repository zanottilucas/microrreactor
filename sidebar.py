import streamlit as st

logo_usjt = "logo-usjt.png"
logo_usjt_branco = "logo-usjt-branco.png"

st.logo(logo_usjt_branco, icon_image=logo_usjt)

st.set_page_config(layout="wide")

st.markdown("""
    <style>
        /* Altera o fundo da sidebar */
        [data-testid="stSidebar"] {
            background-color: #0C2D57;
        }

        /* Altera a cor do texto na sidebar */
        [data-testid="stSidebar"] * {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

pages = {
    "": [
                st.Page("simulador.py", title="Simulação", icon=":material/input:"),
        st.Page("disclaimer.py", title="Em desenvolvimento", icon=":material/info:")
    ],
}

pg = st.navigation(pages)
pg.run()

