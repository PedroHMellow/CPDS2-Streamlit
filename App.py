import pandas as pd
import streamlit as st
from datetime import datetime
from pathlib import Path
from streamlit_option_menu import option_menu


# Configurações da Pagina 
TPagina = "CP2DS | Dashboards"
st.set_page_config(page_title=TPagina, layout="wide")


# Armazenar banco de dados tratado no Streamlit
if "df_ig" not in st.session_state:
        # leitura do excel
        df = pd.read_excel("instagram_completo_formatado.xlsx", index_col=False)

        # criar colunas de Dia da Semana e Horário do Post
        datahora = df["Hora de publicação"].to_list()
        dia_da_semana = []
        hora_do_post = []
        semana_dict = {
            "Sun":"Domingo",
            "Mon":"Segunda-Feira",
            "Tue":"Terça-Feira",
            "Wed":"Quarta-Feira",
            "Thu":"Quinta-Feira",
            "Fri":"Sexta-Feira",
            "Sat":"Sábado",
        }
        for data in datahora:
            data_datetime = datetime.strptime(data, "%m/%d/%Y %H:%M")
            dia_da_semana.append( f"{semana_dict[data_datetime.strftime("%a")]}" )
            hora_do_post.append(int(f"{data_datetime.strftime("%H")}"))
        dia_da_semana_df = pd.DataFrame({"Dia da Semana do Post":dia_da_semana})
        hora_do_post_df = pd.DataFrame({"Horário de Postagem":hora_do_post})
        df["Dia da Semana do Post"] = dia_da_semana_df
        df["Horário de Postagem"] = hora_do_post_df


        # Renomear colunas necessárias
        df.rename(columns={'Gostos': 'Curtidas', 'Partilhas': 'Compartilhamentos','Seguimentos': 'Novos Seguidores', 'Itens guardados': 'Vídeos Salvos', "Descrição":"Nome dos Posts", "Ligação permanente":"Link", "Tipo de publicação":"Tipo de Publicação"}, inplace=True)
        # Remover colunas indesejadas e Organizar Restantes
        df = df[["Nome dos Posts", "Link", "Duração (segundos)", "Horário de Postagem", "Dia da Semana do Post", "Tipo de Publicação", "Alcance", 'Curtidas', 'Compartilhamentos', 'Novos Seguidores', "Comentários", "Vídeos Salvos", "Visualizações"]]
        df.drop(axis="index", index=[0], inplace=True)

        st.session_state["df_ig"] = df


#css
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "Styles" / "Main.css"

with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.markdown(
        f"""
        <div style="text-align: center;">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174855.png" 
                     style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;">
            </a>
            <p style="margin-top: 10px; font-size: 20px; font-weight: bold;">Análise Instagram</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    selected = option_menu("Navegação", ["Home", "Intervalo de Confiança", "Testes de Hipótese", "Equipe"],
                           icons=['house', 'graph-up', 'bar-chart', 'people-fill'], 
                           menu_icon="cast",
                           default_index=0,
                           styles={"menu-title": {"font-size": "30px"}})

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