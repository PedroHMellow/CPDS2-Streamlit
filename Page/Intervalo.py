import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from scipy import stats


current_dir = Path(__file__).parent.parent if "__file__" in locals() else Path.cwd().parent
intervalo_png = current_dir  / "Assets" / "calculo_intervalo.png"


def show():    
    st.write("# Tabela IG para consulta:")
    st.divider()
    with st.expander("📊 Tabela"):
        st.write(" ")
        st.write(" ")
        st.dataframe(st.session_state["df_ig"])


    st.write("# Cálculo para Intervalo de Confiança:")
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    col2.write(" ")
    col2.write(" ")
    col2.write(" ")
    col2.write(" ")
    col2.image(str(intervalo_png), width=230)
    col3.write("CI = Intervalo de Confiança")
    col3.write("x̅ = Média da Amostra")
    col3.write("z = Valor do Nível de Confiança")
    col3.write("s = Desvio Padrão da Amostra")
    col3.write("n = Tamanho da Amostra")


    st.write(" ")
    st.write(" ")
    st.write("# Intervalo de Confiança:")
    st.divider()
    col1, col2, col3 = st.columns([4, 3, 3])

    col1.write("##### Valor a ser analisado:")
    valor_dado = col1.selectbox(
        label="",
        options=("Alcance", "Curtidas", "Compartilhamentos", "Novos Seguidores", "Comentários", "Vídeos Salvos", "Visualizações"),
        index = None,
        placeholder="Classificar dados por..."
                                )
    col1.write(" ")
    col1.write(" ")

    col2.write("##### Como nomear os dados:")
    nome_dado = col2.selectbox(
        label="",
        options=("Nome dos Posts", "Duração (segundos)", "Horário de Postagem", "Dia da Semana do Post", "Tipo de Publicação"),
        index = None,
        placeholder="Nomear os dados por..."
                                )
    col2.write(" ")
    col2.write(" ")

    col3.write("##### Valor de Confiança:")
    confianca_dado = col3.selectbox(
        label="",
        options=(0.80, 0.90, 0.99),
        index = None,
        placeholder="Confiabilidade do dado..."
                                )
    col3.write(" ")
    col3.write(" ")



    if not valor_dado or not nome_dado or not confianca_dado:
        col1, col2, col3 = st.columns([4, 3, 3])
        col2.write(" ")
        col2.write("## ❗Selecionar:")
        if not valor_dado:
            col2.write("- ❌Valor a ser analisado")
        else:
            col2.write(f"- ✅Valor a ser analisado : {valor_dado}")
        if not nome_dado:
            col2.write("- ❌Como nomear os dados")
        else:
            col2.write(f"- ✅Como nomear os dados : {nome_dado}")
        if not confianca_dado:
            col2.write("- ❌Valor de Confiança")
        else:
            col2.write(f"- ✅Valor de Confiança : {confianca_dado}")
    else:
        # coluna específica e sem valores nulos
        coluna_escolhida = st.session_state["df_ig"][[valor_dado, nome_dado]].dropna()

        # retirar imagens
        if nome_dado == "Duração (segundos)":
            coluna_escolhida = coluna_escolhida[coluna_escolhida[nome_dado] > 0]
            
        # descrição da coluna escolhida
        amostra_descricao = coluna_escolhida[valor_dado].describe()
        amostra_descricao.rename(index={'count': 'Contagem', 'mean': 'Média', "std":"Desvio Padrão"}, inplace=True)
        st.divider()
        st.write("### Abordagem sem Valores Nulos")


        with st.expander("➕ Detalhes"):
            col1, col2 = st.columns([7, 3])

            if nome_dado == "Nome dos Posts":
                col2.write(" ")
                col2.write(" ")
                col2.write("###### Descrição da Amostra:")
                col2.dataframe(amostra_descricao)

                media = amostra_descricao['Média']
                sem = amostra_descricao["Desvio Padrão"]
                ic = stats.t.interval(confianca_dado, len(coluna_escolhida[valor_dado])-1, loc=media, scale=sem)
                erro_superior = ic[1] - media
                erro_inferior = media - ic[0]
                if media - erro_inferior < 0:
                    erro_inferior = media
                fig_intervalo_antigo = go.Figure()
                fig_intervalo_antigo.add_trace(go.Scatter(
                    x=[nome_dado],
                    y=[media],
                    error_y=dict(
                        type='data',
                        array=[erro_superior],
                        arrayminus=[erro_inferior],
                        visible=True,
                        thickness=2,
                        color='rgb(189, 89, 89)'
                    ),
                    mode='markers',
                    marker=dict(size=10, color='red')
                ))
                fig_intervalo_antigo.update_layout(
                    title=f"Média de {valor_dado} com Intervalo de Confiança de {confianca_dado*100}%",
                    yaxis_title="Média",
                    showlegend=False
                )
                col1.plotly_chart(fig_intervalo_antigo, key="apresentação antigo grupo")
            else:
                df_divisoes = pd.DataFrame(columns=["Divisão","Média", "Desvio Padrão", "Limite Superior", "Limite Inferior"])
                lista_tipo = None
                lista_tipo_intervalo = None
                if nome_dado == "Duração (segundos)":
                    lista_tipo = None
                    lista_tipo_intervalo = [(1, 15), (15, 30), (30,45), (45,90)]
                elif nome_dado == "Horário de Postagem":
                    lista_tipo = None
                    lista_tipo_intervalo = [(0, 13), (13, 14), (14,19)]
                elif nome_dado == "Dia da Semana do Post":
                    lista_tipo = ["Domingo", "Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado"]
                    lista_tipo_intervalo = None
                # Tipo de Publicação
                else:
                    lista_tipo = ["Carrossel do Instagram", "Imagem do Instagram", "Reel do IG"]
                    lista_tipo_intervalo = None
                    
                if lista_tipo is not None:
                    for tipo in lista_tipo:
                        divisao = coluna_escolhida[coluna_escolhida[nome_dado] == tipo]
                        media = np.mean(divisao[valor_dado])
                        sem = stats.sem(divisao[valor_dado])
                        ic = stats.t.interval(confianca_dado, len(divisao[valor_dado])-1, loc=media, scale=sem)
                        erro_superior = ic[1] - media
                        erro_inferior = media - ic[0]
                        if media - erro_inferior < 0:
                            erro_inferior = media
                        if erro_superior > 0:
                            df_divisao = pd.DataFrame({"Divisão":tipo, "Média":media, "Desvio Padrão":sem, "Limite Superior":erro_superior, "Limite Inferior":erro_inferior}, index=[0])
                            df_divisoes = pd.concat([df_divisoes, df_divisao], ignore_index=True)
                            col2.write(tipo)
                            descricao_tipo = divisao[valor_dado].describe()
                            descricao_tipo = descricao_tipo.loc[["count", "max", "mean", "min"]]
                            amostra_descricao.rename(index={'count': 'Contagem', 'mean': 'Média'}, inplace=True)
                            col2.dataframe(descricao_tipo)
                if lista_tipo_intervalo is not None:
                    for tipo in lista_tipo_intervalo:
                        divisao = coluna_escolhida[coluna_escolhida[nome_dado] >= tipo[0]]
                        divisao = divisao[divisao[nome_dado] < tipo[1]]
                        media = np.mean(divisao[valor_dado])
                        sem = stats.sem(divisao[valor_dado])
                        ic = stats.t.interval(confianca_dado, len(divisao[valor_dado])-1, loc=media, scale=sem)
                        erro_superior = ic[1] - media
                        erro_inferior = media - ic[0]
                        if media - erro_inferior < 0:
                            erro_inferior = media
                        if erro_superior > 0:
                            df_divisao = pd.DataFrame({"Divisão":f"{tipo[0]}-{tipo[1]}", "Média":media, "Desvio Padrão":sem, "Limite Superior":erro_superior, "Limite Inferior":erro_inferior}, index=[0])
                            df_divisoes = pd.concat([df_divisoes, df_divisao], ignore_index=True)
                            col2.write(f"{tipo[0]}-{tipo[1]}")
                            descricao_tipo = divisao[valor_dado].describe()
                            descricao_tipo = descricao_tipo.loc[["count", "max", "mean", "min"]]
                            amostra_descricao.rename(index={'count': 'Contagem', 'mean': 'Média'}, inplace=True)
                            col2.dataframe(descricao_tipo)
                    
                fig_intervalo_antigo = go.Figure()
                fig_intervalo_antigo.add_trace(
                    go.Scatter(
                        x=df_divisoes["Divisão"],
                        y=df_divisoes["Média"],
                        error_y=dict(
                            type='data',
                            array=df_divisoes["Limite Superior"],
                            arrayminus=df_divisoes["Limite Inferior"],
                            visible=True,
                            thickness=2,
                            color='rgb(189, 89, 89)'
                        ),
                        mode='markers',
                        marker=dict(size=10, color='red')
                    )
                )
                fig_intervalo_antigo.update_layout(
                    title=f"Média de {valor_dado} com Intervalo de Confiança de {confianca_dado*100}%",
                    yaxis_title="Média",
                    xaxis_title=nome_dado,
                    hovermode="x"
                )
                col1.plotly_chart(fig_intervalo_antigo, key="apresentação antigo grupo")
                col1.write(" ")
                col1.write(" ")
                col1.write("###### Descrição da Amostra:")
                col1.dataframe(amostra_descricao)
            st.session_state["imagem_intervalo_antigo"] = fig_intervalo_antigo

            fig = px.box(coluna_escolhida, y=valor_dado, points="all", hover_data={nome_dado: True}, title="Boxplot da Amostra")
            fig.update_traces(marker=dict(size=10, color="red", opacity=0.7), jitter=0.3)
            col1.plotly_chart(fig)


        
        q1 = coluna_escolhida[valor_dado].quantile(0.25)
        q3 = coluna_escolhida[valor_dado].quantile(0.75)
        iqr = q3 - q1
        # limite superior para retira outliers
        limite_superior = q3 + 1.5*iqr
        # coluna específica, sem valores nulos e sem outliers
        coluna_escolhida_reduzida = coluna_escolhida[coluna_escolhida[valor_dado] <= limite_superior]
        st.write(f"### Abordagem sem Valores Nulos e antigos Outliers(antigo Limite Superior: {limite_superior})")
        
        with st.expander("➕ Detalhes"):
            # descrição da coluna escolhida reduzido
            amostra_reduzida_descricao = coluna_escolhida_reduzida[valor_dado].describe()
            amostra_reduzida_descricao.rename(index={'count': 'Contagem', 'mean': 'Média', "std":"Desvio Padrão"}, inplace=True)
            col1, col2 = st.columns([7, 3])

            if nome_dado == "Nome dos Posts":
                col2.write(" ")
                col2.write(" ")
                col2.write("###### Descrição da Amostra:")
                col2.dataframe(amostra_reduzida_descricao)

                media = amostra_reduzida_descricao['Média']
                sem = amostra_reduzida_descricao["Desvio Padrão"]
                ic = stats.t.interval(confianca_dado, len(coluna_escolhida_reduzida[valor_dado])-1, loc=media, scale=sem)
                erro_superior = ic[1] - media
                erro_inferior = media - ic[0]
                if media - erro_inferior < 0:
                    erro_inferior = media
                fig_intervalo_novo = go.Figure()
                fig_intervalo_novo.add_trace(go.Scatter(
                    x=[nome_dado],
                    y=[media],
                    error_y=dict(
                        type='data',
                        array=[erro_superior],
                        arrayminus=[erro_inferior],
                        visible=True,
                        thickness=2,
                        color='rgb(189, 89, 89)'
                    ),
                    mode='markers',
                    marker=dict(size=10, color='red')
                ))
                fig_intervalo_novo.update_layout(
                    title=f"Média de {valor_dado} com Intervalo de Confiança de {confianca_dado*100}%",
                    yaxis_title="Média",
                    showlegend=False
                )
                col1.plotly_chart(fig_intervalo_novo, key="apresentação novo único")
            else:
                df_divisoes = pd.DataFrame(columns=["Divisão","Média", "Desvio Padrão", "Limite Superior", "Limite Inferior"])
                lista_tipo = None
                lista_tipo_intervalo = None
                if nome_dado == "Duração (segundos)":
                    lista_tipo = None
                    lista_tipo_intervalo = [(1, 15), (15, 30), (30,45), (45,90)]
                elif nome_dado == "Horário de Postagem":
                    lista_tipo = None
                    lista_tipo_intervalo = [(0, 13), (13, 14), (14,19)]
                elif nome_dado == "Dia da Semana do Post":
                    lista_tipo = ["Domingo", "Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado"]
                    lista_tipo_intervalo = None
                # Tipo de Publicação
                else:
                    lista_tipo = ["Carrossel do Instagram", "Imagem do Instagram", "Reel do IG"]
                    lista_tipo_intervalo = None
                    
                if lista_tipo is not None:
                    for tipo in lista_tipo:
                        divisao = coluna_escolhida_reduzida[coluna_escolhida_reduzida[nome_dado] == tipo]
                        media = np.mean(divisao[valor_dado])
                        sem = stats.sem(divisao[valor_dado])
                        ic = stats.t.interval(confianca_dado, len(divisao[valor_dado])-1, loc=media, scale=sem)
                        erro_superior = ic[1] - media
                        erro_inferior = media - ic[0]
                        if media - erro_inferior < 0:
                            erro_inferior = media
                        if erro_superior > 0:
                            df_divisao = pd.DataFrame({"Divisão":tipo, "Média":media, "Desvio Padrão":sem, "Limite Superior":erro_superior, "Limite Inferior":erro_inferior}, index=[0])
                            df_divisoes = pd.concat([df_divisoes, df_divisao], ignore_index=True)
                            col2.write(tipo)
                            descricao_tipo = divisao[valor_dado].describe()
                            descricao_tipo = descricao_tipo.loc[["count", "max", "mean", "min"]]
                            amostra_reduzida_descricao.rename(index={'count': 'Contagem', 'mean': 'Média'}, inplace=True)
                            col2.dataframe(descricao_tipo)
                if lista_tipo_intervalo is not None:
                    for tipo in lista_tipo_intervalo:
                        divisao = coluna_escolhida_reduzida[coluna_escolhida_reduzida[nome_dado] >= tipo[0]]
                        divisao = divisao[divisao[nome_dado] < tipo[1]]
                        media = np.mean(divisao[valor_dado])
                        sem = stats.sem(divisao[valor_dado])
                        ic = stats.t.interval(confianca_dado, len(divisao[valor_dado])-1, loc=media, scale=sem)
                        erro_superior = ic[1] - media
                        erro_inferior = media - ic[0]
                        if media - erro_inferior < 0:
                            erro_inferior = media
                        if erro_superior > 0:
                            df_divisao = pd.DataFrame({"Divisão":f"{tipo[0]}-{tipo[1]}", "Média":media, "Desvio Padrão":sem, "Limite Superior":erro_superior, "Limite Inferior":erro_inferior}, index=[0])
                            df_divisoes = pd.concat([df_divisoes, df_divisao], ignore_index=True)
                            col2.write(f"{tipo[0]}-{tipo[1]}")
                            descricao_tipo = divisao[valor_dado].describe()
                            descricao_tipo = descricao_tipo.loc[["count", "max", "mean", "min"]]
                            amostra_reduzida_descricao.rename(index={'count': 'Contagem', 'mean': 'Média'}, inplace=True)
                            col2.dataframe(descricao_tipo)
                    
                fig_intervalo_novo = go.Figure()
                fig_intervalo_novo.add_trace(
                    go.Scatter(
                        x=df_divisoes["Divisão"],
                        y=df_divisoes["Média"],
                        error_y=dict(
                            type='data',
                            array=df_divisoes["Limite Superior"],
                            arrayminus=df_divisoes["Limite Inferior"],
                            visible=True,
                            thickness=2,
                            color='rgb(189, 89, 89)'
                        ),
                        mode='markers',
                        marker=dict(size=10, color='red')
                    )
                )
                fig_intervalo_novo.update_layout(
                    title=f"Média de {valor_dado} com Intervalo de Confiança de {confianca_dado*100}%",
                    yaxis_title="Média",
                    xaxis_title=nome_dado,
                    hovermode="x"
                )
                col1.plotly_chart(fig_intervalo_novo, key="apresentação novo grupo")
                col1.write(" ")
                col1.write(" ")
                col1.write("###### Descrição da Amostra:")
                col1.dataframe(amostra_reduzida_descricao)
            st.session_state["imagem_intervalo_novo"] = fig_intervalo_novo

            fig = px.box(coluna_escolhida_reduzida, y=valor_dado, points="all", hover_data={nome_dado: True}, title="Boxplot da Amostra")
            fig.update_traces(marker=dict(size=10, color="red", opacity=0.7), jitter=0.3)
            col1.plotly_chart(fig)



        st.write("### Abordagem Antiga X Abordagem Nova")
        col1, col2 = st.columns(2)
        col1.plotly_chart(st.session_state["imagem_intervalo_antigo"], key="versus antigo")
        col2.plotly_chart(st.session_state["imagem_intervalo_novo"], key="versus novo")



    st.write(" ")
    st.write(" ")
    st.write("# Interpretações:")
    st.divider()
    st.write("Analisando as simulações foi possível observar uma redução da Margem de Erro tanto através da redução  do Valor de Confiança quanto da remoção dos Outliers da Primeira Abordagem.")
    st.write("No primeiro caso(Valor de Confiança), a redução da Margem de erro é efeito direto de uma redução da precisão desse Intervalo. Desse forma, um aumento da Margem de erro devido a um aumento do Valor de Confiança se mostra benéfico por se aproximar mais do conjunto real.")
    st.write("Já no segundo caso(Outliers da Primeira Abordagem), a redução da Margem de erro é efeito direto da redução do Desvio Padrão, consequência da remoção dos antigos Outliers e da construção uma amostra com valores mais próximos uns dos outros. Essa remoção se mostra necessária porque nessa amostragem em específico há posts que receberam um boost de publicidade, mas que não foram identificados, precisando, assim, supor que eles seriam os valores discrepantes(Outliers). Desse forma, uma redução da Margem de erro devido à remoção de Outliers de  se mostra benéfico por se aproximar mais do conjunto real e aumentar a precisão do Intervalo de Confiança.")