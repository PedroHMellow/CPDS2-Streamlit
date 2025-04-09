import streamlit as st
from pathlib import Path
from streamlit_option_menu import option_menu


# Configurações da Pagina 
TPagina = "CP2DS | Dashboards"
st.set_page_config(page_title=TPagina)

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "Styles" / "Main.css"


with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(
        f"""
        <div style="text-align: center;">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174855.png" 
                     style="width: 180px; height: 180px; border-radius: 50%; object-fit: cover;">
            </a>
            <p style="margin-top: 10px; font-size: 16px; font-weight: bold;">Análise Instagram</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    selected = option_menu("Navegação", ["Home", "Intervalo de Confiança", "Testes de Hipótese", "Equipe"],
                           icons=['house', 'graph-up', 'bar-chart', 'people-fill'], 
                           menu_icon="cast", default_index=0)

if selected == "Home":
    from Page import Home
    Home.show()

elif selected == "Intervalo de Confiança":
    from Page import Intervalo
    Intervalo.show()

elif selected == "Testes de Hipótese":
    from Page import Testes
    Testes.show()

elif selected == "Equipe":
    from Page import Equipe
    Equipe.show()