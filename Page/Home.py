import streamlit as st

def show():
    st.title("🏠 Home")
    
    st.header("Descrição do Problema")
    st.markdown("""
### 🎯 Análise do Problema — Desempenho de Conteúdo no Instagram da THM Estatística

A conta **@thmestatistica**, do projeto **THM Estatística | Ciência de Dados**, utiliza o Instagram como um canal de divulgação científica e educacional voltado à estatística e ciência de dados. O conteúdo é majoritariamente publicado nos formatos de **Reels** e **Imagens**, com o objetivo de promover engajamento, ampliar o alcance e conquistar novos seguidores.

No entanto, os dados analisados revelam **fortes variações no desempenho das publicações**, o que indica que fatores estratégicos estão influenciando os resultados, muitas vezes de forma não controlada. Isso cria a necessidade de uma abordagem baseada em dados para identificar padrões de sucesso e oportunidades de melhoria.

---

### 📊 Contexto dos Dados

A base inclui métricas detalhadas como:
- **Tipo de publicação** (Reel ou Imagem);
- **Duração dos vídeos (em segundos)**;
- **Horário e data da publicação**;
- **Alcance, visualizações, curtidas, comentários, partilhas, seguidores conquistados e salvamentos**.

---

### 🔍 Principais Observações

1. **Disparidade no desempenho**  
   - Algumas publicações ultrapassam **4 milhões de visualizações**, enquanto outras, com características semelhantes, ficam abaixo de **50 mil**.  
   - Essa variação sugere que pequenos ajustes de formato, conteúdo ou tempo podem causar grande impacto.

2. **Formato importa**  
   - Os **Reels** se destacam com desempenho amplamente superior às imagens.  
   - Isso está alinhado com a tendência da plataforma em priorizar vídeos curtos e envolventes.

3. **Duração dos Reels**  
   - Vídeos curtos (cerca de 7 a 10 segundos) frequentemente performam melhor.  
   - Porém, essa relação não é universal, indicando que **o conteúdo é tão importante quanto o tempo de duração**.

4. **Engajamento nem sempre converte em seguidores**  
   - Nem todas as publicações de alto desempenho resultam em crescimento da base de seguidores.  
   - Isso sugere que é necessário focar também na **construção de conexão com o público**, e não apenas no alcance.

5. **Ausência de insights qualitativos**  
   - A falta de comentários descritivos sobre cada post impede uma análise mais rica de elementos como tom de voz, tipo de humor, ou tema abordado.

---

### 🧠 Hipóteses Iniciais

- O tipo de conteúdo (educativo, humorístico, motivacional) pode afetar diretamente o engajamento.
- A duração ideal do Reel pode estar entre 7 e 15 segundos.
- Horário e dia da semana influenciam o alcance.
- Reels com chamadas diretas à ação (CTA) tendem a gerar mais partilhas e salvamentos.

---

### ✅ Conclusão

A conta da THM Estatística possui **alto potencial de crescimento**, mas é necessário compreender melhor os fatores que influenciam o desempenho das publicações. Através de uma análise orientada por dados, é possível tomar decisões estratégicas mais eficientes para produzir conteúdos que gerem não apenas visualizações, mas também **conexão e conversão**.

Essa análise abre o caminho para:
- Comparar métricas entre formatos e temas;
- Identificar os melhores horários de postagem;
- Avaliar quais elementos aumentam seguidores e salvamentos;
- Estruturar uma **estratégia de conteúdo otimizada e validada por evidências**.
""", unsafe_allow_html=True)

    st.markdown("#")

    st.header("Descrição Tipo de Variáveis")
    st.write("Escrever...")
