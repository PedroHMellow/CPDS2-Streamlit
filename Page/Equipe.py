import streamlit as st
from pathlib import Path
import base64

# Função para converter imagem em base64
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Caminhos das imagens
current_dir = Path(__file__).parent.parent if "__file__" in locals() else Path.cwd().parent
profile_pic = current_dir  / "Assets" / "Profile picture.png"
Gustavo_pic = current_dir  / "Assets" / "Gustavo.jpg"  
Borba = current_dir  / "Assets" / "Borba.jpg"  
Henrique = current_dir  / "Assets" / "Henrique_perfil.png"
EnzoT = current_dir  / "Assets" / "enzo.jpeg"

def circular_profile(base64_img, nome, rm):
    return f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{base64_img}" 
                 style="width: 230px; height: 230px; border-radius: 50%; object-fit: cover; margin-bottom: 10px;">
            <div style="font-weight: bold; font-size: 22px;">{nome}</div>
            <div style="font-size: 14px;">{rm}</div>
        </div>
    """


def show():
    st.title("👥 Equipe/Grupo")
    st.write("###")

    col1, col2, col3 = st.columns(3, gap="small")

    with col1:
        st.markdown(circular_profile(get_base64_image(Borba), "Gabriel Borba", "RM553187"), unsafe_allow_html=True)

    with col2:
        st.markdown(circular_profile(get_base64_image(EnzoT), "Enzo Teles de Moura", "RM553899"), unsafe_allow_html=True)

    with col3:
        st.markdown(circular_profile(get_base64_image(Gustavo_pic), "Gustavo Gouvêa Soares", "RM553842"), unsafe_allow_html=True)

    st.write("###")

    col_empty1, col4, col5, col_empty2 = st.columns([1, 2, 2, 1], gap="small")

    with col4:
        st.markdown(circular_profile(get_base64_image(Henrique), "Henrique Rafael Gomes de Souza", "RM553945"), unsafe_allow_html=True)

    with col5:
         st.image(str(profile_pic), width=230)
         st.write("Pedro Henrique Mello Silva Alves")
         st.write("RM554223")
         st.markdown(circular_profile(get_base64_image(profile_pic), "Pedro Henrique Mello Silva Alves", "RM554223"), unsafe_allow_html=True)
