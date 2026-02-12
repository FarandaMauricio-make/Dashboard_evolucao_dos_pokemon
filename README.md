
# 🧬 PokéEvo Analytics: A Matemática da Evolução

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![Plotly](https://img.shields.io/badge/Visualization-Plotly-purple)
![SQLite](https://img.shields.io/badge/Database-SQLite3-green)

> **Dashboard Analítico** que responde à pergunta fundamental de todo treinador Pokémon: *"Quanto meu time realmente melhora ao evoluir?"*. O projeto analisa o ganho de atributos (BST) através das gerações e mapeia os métodos de evolução.

## 📋 Sobre o Projeto

Este dashboard conecta-se ao Data Warehouse criado anteriormente (`pokemon_dw.db`) para realizar uma análise aprofundada sobre a mecânica de evolução.

Diferente de uma simples Pokédex, esta ferramenta foca no **"Delta" (Variação)**. Ela calcula a diferença matemática de poder entre um estágio e outro, revelando quais Pokémon têm os maiores "Power Spikes" (picos de poder) e quais evoluções são apenas estéticas.

---

## 🚀 Funcionalidades e Insights

### 1. 📊 Cálculo de BST (Base Stat Total)
O script agrega os 6 status base (HP, Atk, Def, SpA, SpD, Spe) para criar uma métrica única de poder.
- **Insight:** Permite comparar Pokémon de tipos diferentes usando uma régua comum.

### 2. 📈 Análise de "Buffs" (Ganhos)
- **KPIs de Evolução:** Calcula a média de pontos ganhos na 1ª evolução (Base → Estágio 2) vs 2ª evolução (Estágio 2 → Estágio 3).
- **Boxplot de Distribuição:** Identifica outliers.
    - *Exemplo:* O gráfico revela o **"Efeito Magikarp"**, onde um Pokémon fraco ganha +340 pontos de uma vez ao evoluir, enquanto outros ganham menos de 50.

### 3. 🔄 Fluxo de Evolução (Sankey Diagram)
- **Mapeamento de Triggers:** Um diagrama de fluxo (Sankey) que conecta o *Método de Evolução* (Nível, Pedra, Troca) ao *Estágio de Destino*.
- **Visualização de Caminhos:** Ajuda a entender se Pokémon que evoluem por "Pedra" tendem a ir direto para o estágio final ou não.

---

## 🛠️ Tecnologias Utilizadas

* **[Streamlit](https://streamlit.io/):** Interface web e cache de dados (`@st.cache_data`).
* **[Pandas](https://pandas.pydata.org/):** ETL (Merge, GroupBy, Diff) para calcular os deltas de evolução.
* **[Plotly Graph Objects (GO) & Express](https://plotly.com/python/):** Gráficos interativos avançados (Sankey, Boxplot).
* **[SQLite3](https://www.sqlite.org/):** Leitura eficiente das tabelas relacionais.

---

## 📦 Como Rodar o Projeto

### Pré-requisitos
⚠️ **Importante:** Você precisa ter o arquivo `pokemon_dw.db` na mesma pasta. Este arquivo é gerado pelo script de ETL (Extração) do projeto anterior.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/poke-evo-analytics.git](https://github.com/SEU-USUARIO/poke-evo-analytics.git)
    cd poke-evo-analytics
    ```

2.  **Verifique o Banco de Dados:**
    Certifique-se de que `pokemon_dw.db` está na raiz do projeto.

3.  **Instale as dependências:**
    ```bash
    pip install streamlit pandas plotly
    ```

4.  **Execute o Dashboard:**
    ```bash
    streamlit run poke_evo_buffs.py
    ```

---

## 📂 Estrutura de Arquivos

---

## 🧠 Exemplo de Análise (Storytelling)

Ao utilizar o dashboard, é possível notar padrões de design da Game Freak:

1.  **Recompensa Tardia:** A evolução do Estágio 2 para o 3 geralmente concede mais status que a primeira, incentivando o jogador a levar o Pokémon até o nível máximo.
2.  **Outliers:** Pokémon "bebês" (Pichu, Cleffa) ou peixes fracos (Feebas, Magikarp) possuem os maiores deltas do jogo, funcionando como uma mecânica de "alto risco, alta recompensa".

---

## 🤝 Contribuição

Tem ideias para analisar Mega Evoluções ou formas Regionais?

1.  Faça um Fork.
2.  Crie sua Feature Branch.
3.  Commit e Push.
4.  Abra um Pull Request.

---

**Evoluindo com Dados!** 🧬

Você pode acessar o Dashboard no seguinte endereço: [A Matemática da Evolução Pokémon](https://dashboard-evolucao-dos-pokemon.onrender.com)
