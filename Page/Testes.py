# Testes.py
import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.express as px
from scipy.stats import shapiro, mannwhitneyu, spearmanr

def show():
    st.title("📊 Testes de Hipótese Avançados")
    
    # Widget para seleção da métrica
    variavel_alvo = st.selectbox(
        "Selecione a Métrica para Análise",
        ["Visualizações", "Curtidas", "Compartilhamentos", "Novos Seguidores"],
        index=0,
        key="var_alvo"
    )
    
    # Verificação de dados carregados
    if "df_ig" not in st.session_state:
        st.error("Dados não carregados!")
        return
    
    # Pré-processamento seguro
    try:
        df = st.session_state["df_ig"].copy()
        
        # Colunas essenciais e tratamento de dados
        essential_cols = [
            "Visualizações", "Alcance", "Curtidas", "Nome dos Posts",
            "Tipo de Publicação", "Duração (segundos)", "Horário de Postagem",
            "Dia da Semana do Post", "Novos Seguidores", "Compartilhamentos", 
            "Vídeos Salvos"
        ]
        
        df = df.dropna(subset=essential_cols).reset_index(drop=True)
        
        # Tratamento de outliers
        Q1 = df["Visualizações"].quantile(0.25)
        Q3 = df["Visualizações"].quantile(0.75)
        IQR = Q3 - Q1
        df = df[~((df["Visualizações"] < (Q1 - 1.5 * IQR)) | 
                 (df["Visualizações"] > (Q3 + 1.5 * IQR)))]
        
        # Transformações e CTAs
        df["log_curtidas"] = np.log1p(df["Curtidas"])
        df["Tem CTA"] = df["Nome dos Posts"].str.contains(
            r'(?i)(comente|link na bio|clique|inscreva|responda|aprender|acesse|clica|conheça)',
            regex=True,
            na=False
        ).astype(bool)
        
        assert df["Tem CTA"].dtype == bool
        
    except Exception as e:
        st.error(f"Erro no pré-processamento: {str(e)}")
        st.stop()

    # =========================================================================
    # TESTE 1: Comparação Reels vs Imagens
    # =========================================================================
    with st.expander("🎬 Reels vs Imagens", expanded=True):
        st.subheader("Análise Comparativa de Formatos")
        
        reel_data = df[df["Tipo de Publicação"].str.contains("Reel", na=False)]
        imagem_data = df[df["Tipo de Publicação"].str.contains("Imagem", na=False)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.box(
                df, 
                x="Tipo de Publicação", 
                y=variavel_alvo,
                color="Tipo de Publicação",
                color_discrete_sequence=["#1f77b4", "#ff7f0e"],
                title=f"Distribuição de {variavel_alvo}",
                points="all",
                hover_data=["Nome dos Posts"]
            )
            fig.update_layout(
                template="plotly_white",
                xaxis_title=None,
                yaxis_title=variavel_alvo,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.caption("""
            **📌 Como interpretar:**  
            • Cada caixa representa a distribuição dos dados  
            • Linha central = Mediana (valor que divide os dados ao meio)  
            • Bordas da caixa = Quartis 25% e 75%  
            • Pontos fora = Posts com desempenho excepcional
            """)
            
        with col2:
            if len(reel_data) >= 10 and len(imagem_data) >= 10:
                _, p_reel = shapiro(reel_data[variavel_alvo])
                _, p_img = shapiro(imagem_data[variavel_alvo])
                
                if p_reel > 0.05 and p_img > 0.05:
                    t_stat, p_val = stats.ttest_ind(reel_data[variavel_alvo], imagem_data[variavel_alvo])
                    st.metric("Teste T de Student", f"p = {p_val:.4f}")
                else:
                    u_stat, p_val = mannwhitneyu(reel_data[variavel_alvo], imagem_data[variavel_alvo])
                    st.metric("Teste Mann-Whitney U", f"p = {p_val:.4f}")
                
                st.metric("Diferença Mediana", 
                        f"{reel_data[variavel_alvo].median() - imagem_data[variavel_alvo].median():.1f}",
                        help="Diferença entre os valores típicos de cada grupo")
                
                st.caption("""
                **🔍 Interpretação do p-valor:**  
                • p < 0.05 → Diferença **significativa** entre grupos  
                • p > 0.05 → Diferença **não significativa**  
                • Valores próximos de 0 indicam maior confiança
                """)
                
            else:
                pass

    # =========================================================================
    # TESTE 2: Análise Temporal
    # =========================================================================
    with st.expander("⏰ Melhor Horário para Postar"):
        st.subheader("Performance Temporal Detalhada")
        
        df["Período"] = pd.cut(df["Horário de Postagem"],
                             bins=[0, 9, 12, 15, 18, 24],
                             labels=["Madrugada", "Manhã", "Almoço", "Tarde", "Noite"])
        
        heatmap_data = df.pivot_table(
            index="Dia da Semana do Post",
            columns="Período",
            values=variavel_alvo,
            aggfunc='median'
        )
        
        fig = px.imshow(
            heatmap_data,
            labels=dict(x="Período", y="Dia", color=variavel_alvo),
            color_continuous_scale='Greens',
            title=f"Desempenho de {variavel_alvo} por Dia/Horário"
        )
        fig.update_layout(
            xaxis=dict(tickangle=-45),
            coloraxis_colorbar=dict(title="Média")
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption("""
        **🧭 Guia de uso:**  
        • Cores mais escuras → Melhor desempenho  
        • Combine dias da semana e horários com maior intensidade  
        • Dados vazios (brancos) indicam falta de posts no período
        """)

    # =========================================================================
    # TESTE 3: Impacto de CTAs
    # =========================================================================
    with st.expander("📣 Efeito de Chamadas à Ação"):
        st.subheader("Análise de CTAs")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = px.histogram(
                df,
                x=variavel_alvo,
                color="Tem CTA",
                nbins=30,
                marginal="rug",
                opacity=0.7,
                color_discrete_sequence=["#2ca02c", "#d62728"],
                title=f"Distribuição de {variavel_alvo} por CTA",
                barmode="overlay"
            )
            fig.update_layout(
                template="plotly_white",
                legend_title_text="Tem CTA?",
                hoverlabel=dict(bgcolor="white")
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.caption("""
            **📊 O que observar:**  
            • Sobreposição total = CTAs não fazem diferença  
            • Separação clara = CTAs impactam o desempenho  
            • Rug plot (barrinhas) mostra distribuição detalhada
            """)
            
        with col2:
            cta_stats = df.groupby("Tem CTA")[variavel_alvo].agg([
                ('Média', 'mean'),
                ('Mediana', 'median'),
                ('Total Posts', 'count')
            ])
            
            st.dataframe(
                cta_stats.style.format({
                    'Média': '{:.1f}',
                    'Mediana': '{:.1f}',
                    'Total Posts': '{:.0f}'
                }),
                use_container_width=True
            )
            
            if len(df[df["Tem CTA"]]) >= 10 and len(df[~df["Tem CTA"]]) >= 10:
                _, p_val = mannwhitneyu(
                    df[df["Tem CTA"]][variavel_alvo],
                    df[~df["Tem CTA"]][variavel_alvo]
                )
                st.metric("Teste Mann-Whitney U", f"p = {p_val:.4f}")
                
                st.caption(f"""
                **🎯 Resultado:**  
                {'✅ Diferença significativa' if p_val < 0.05 else '❌ Sem diferença relevante'}  
                {'(CTAs funcionam!)' if p_val < 0.05 else '(CTAs não fazem diferença)'}
                """)

    # =========================================================================
    # TESTE 4: Correlações
    # =========================================================================
    with st.expander("🔗 Relações entre Métricas"):
        st.subheader("Análise de Correlação Multivariada")
        
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        selected = st.multiselect("Selecione variáveis para análise:", numeric_cols, default=numeric_cols[:4])
        
        if len(selected) >= 2:
            corr_matrix = df[selected].corr(method='spearman')
            p_values = df[selected].apply(lambda x: df[selected].apply(
                lambda y: spearmanr(x, y).pvalue
            ))
            
            mask = (p_values < 0.05) & (abs(corr_matrix) > 0.3)
            corr_filtrada = corr_matrix.where(mask)
            
            fig = px.imshow(
                corr_filtrada,
                text_auto=".2f",
                color_continuous_scale='RdBu',
                range_color=[-1, 1],
                title="Correlações Relevantes (p < 0.05 e |r| > 0.3)"
            )
            fig.update_layout(
                xaxis=dict(tickangle=45),
                width=800, height=800
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.caption("""
            **🔗 Escala de Correlação:**  
            • 🔵 **+1** = Aumento conjunto perfeito  
            • 🔴 **-1** = Relação inversa perfeita  
            • **0** = Sem relação detectada  
            • Somente correlações estatisticamente relevantes são exibidas
            """)

    # =========================================================================
    # TESTE 5: Duração de Reels (Quartis Explicados)
    # =========================================================================
    with st.expander("⏱️ Análise de Duração de Vídeos"):
        st.subheader("Otimização de Duração")
        
        df_reels = df[df["Tipo de Publicação"].str.contains("Reel", na=False)].copy()
        
        if not df_reels.empty:
            df_reels["Quartil Duração"] = pd.qcut(
                df_reels["Duração (segundos)"],
                q=4,
                labels=["Q1 (25% Mais Curtos)", "Q2", "Q3", "Q4 (25% Mais Longos)"]
            )
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.box(
                    df_reels,
                    x="Quartil Duração",
                    y=variavel_alvo,
                    color="Quartil Duração",
                    color_discrete_sequence=px.colors.sequential.Blues,
                    title=f"Desempenho por Duração de Reels"
                )
                fig.update_layout(
                    template="plotly_white",
                    xaxis_title="Quartil de Duração",
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.caption("""
                **📐 O que são Quartis?**  
                Divisão dos vídeos em 4 grupos igualmente populados:  
                1. **Q1:** 25% mais curtos (ex: 0-15 segundos)  
                2. **Q2:** 25-50% de duração  
                3. **Q3:** 50-75% de duração  
                4. **Q4:** 25% mais longos (ex: acima de 45 segundos)
                """)
                
            with col2:
                duration_stats = df_reels.groupby("Quartil Duração")[variavel_alvo].agg([
                    ('Quantidade', 'count'),
                    ('Média', 'mean'),
                    ('Desvio Padrão', 'std'),
                    ('Mínimo', 'min'),
                    ('25%', lambda x: x.quantile(0.25)),
                    ('Mediana', 'median'),
                    ('75%', lambda x: x.quantile(0.75)),
                    ('Máximo', 'max')
                ])
                
                st.dataframe(
                    duration_stats.style.format({
                        'Média': '{:.1f}',
                        'Desvio Padrão': '{:.1f}',
                        '25%': '{:.1f}',
                        'Mediana': '{:.1f}',
                        '75%': '{:.1f}'
                    }),
                    use_container_width=True
                )
                
                st.caption("""
                **📈 Legenda da Tabela:**  
                • **Mediana:** Valor típico de cada grupo  
                • **25%/75%:** Limites inferior/superior da maioria dos dados  
                • **Desvio Padrão:** Medida de variação (valores altos = mais dispersão)
                """)

    # =========================================================================
    # TESTE 6: Validação dos Dados (Explicação Detalhada)
    # =========================================================================
    with st.expander("🔍 Validação e Consistência"):
        st.subheader("Verificação de Qualidade dos Dados")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Posts Analisados", len(df), help="Posts após limpeza de dados")
            st.metric("Posts com Reels", df["Tipo de Publicação"].str.contains("Reel").sum(), 
                     help="Vídeos curtos no formato Reel")
            st.metric("Posts com Imagens", df["Tipo de Publicação"].str.contains("Imagem").sum(),
                     help="Posts estáticos de imagem única")
            
        with col2:
            cta_counts = df["Tem CTA"].value_counts(normalize=True).reset_index()
            cta_counts.columns = ["Tem CTA", "Proporção"]
            fig = px.bar(
                cta_counts, 
                x="Proporção", 
                y="Tem CTA",
                orientation='h',
                color="Tem CTA",
                color_discrete_sequence=["#1f77b4", "#ff7f0e"],
                text_auto=".1%",
                title="Proporção de Posts com CTAs"
            )
            fig.update_layout(template="plotly_white", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            st.caption("""
            **📢 O que isso significa?**  
            Mostra a frequência de uso de Chamadas à Ação:  
            • **True:** Posts com instruções diretas ao público  
            • **False:** Posts apenas informativos  
            • Exemplo: 70% em True = maioria pede ação do público
            """)

if __name__ == "__main__":
    show()
