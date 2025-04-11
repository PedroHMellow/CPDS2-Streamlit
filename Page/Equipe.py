import streamlit as st
from pathlib import Path

current_dir = Path(__file__).parent.parent if "__file__" in locals() else Path.cwd().parent
profile_pic = current_dir  / "Assets" / "Profile picture.png"
Gustavo_pic = current_dir  / "Assets" / "Gustavo.jpg"  

def show():
    st.title("👥 Equipe/Grupo")
    st.write("###")

    col1, col2, col3, col4, col5 = st.columns(5, gap="small")

    with col1:
        st.write("Gabriel Borba")
        st.write("RM553187")

    with col2:
        st.write("Enzo Teles de Moura")
        st.write("RM553899")

    with col3:
        st.image(str(Gustavo_pic), width=230)
        st.write("Gustavo Gouvêa Soares")
        st.write("RM553842 ")

    with col4:
        st.write("Henrique Rafael Gomes de Souza")
        st.write("RM553945")

    with col5:
        st.image(str(profile_pic), width=230)
        st.write("Pedro Henrique Mello Silva Alves")
        st.write("RM554223")
