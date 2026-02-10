import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==============================================================================

st.set_page_config(
    page_title="Jornada de Poder Pokémon", 
    page_icon="🔥", 
    layout="wide" # Usa a tela inteira, melhor para gráficos lado a lado
)

# ==============================================================================
# 2. CARREGAMENTO DE DADOS (Extração)
# ==============================================================================

# @st.cache_data: Isso é vital! Salva o resultado na memória RAM.
# Sem isso, toda vez que você mudar um filtro, o Streamlit releria o banco de dados do zero.
@st.cache_data(ttl=3600) 
def carregar_dados():
    # Caminho do banco de dados (ajuste de acordo com seu caminho local)
    db_path = ("pokemon_dw.db")
    conn = sqlite3.connect(db_path)

    # --- Tabela de Nomes ---
    # Pegamos apenas o essencial: ID numérico e Nome (ex: 1, Bulbasaur)
    df_pokemon = pd.read_sql_query("SELECT id, name FROM pokemon", conn)

    # --- Tabela de Status ---
    # DISTINCT: Garante que não vamos pegar linhas duplicadas se o banco estiver sujo.
    # stat_name: Garante que pegamos HP, Atk, Def separadamente.
    query_stats = """
    SELECT DISTINCT 
        pokemon_id, 
        stat_name, 
        base_stat 
    FROM pokemon_stats
    """
    df_stats = pd.read_sql_query(query_stats, conn)

    # --- Tabela de Evolução ---
    # chain_id: O "sobrenome" da família (todos da família Bulbasaur têm o mesmo chain_id).
    # from/to: Quem é o pai e quem é o filho.
    # trigger: O que causa a evolução (Item, Level, etc).
    query_evo = "SELECT chain_id, from_species, to_species, trigger FROM evolution"
    df_evolution = pd.read_sql_query(query_evo, conn)

    conn.close() # Sempre feche a conexão para não travar o arquivo do banco
    return df_pokemon, df_stats, df_evolution

# Executa a função e guarda nas variáveis
df_pokemon, df_stats, df_evolution = carregar_dados()

# ==============================================================================
# 3. PROCESSAMENTO DE DADOS (Transformação / ETL)
# ==============================================================================

# --- Passo 1: Calcular o BST (Base Stat Total) ---
# O BST é a soma de HP + Atk + Def + SpA + SpD + Spe.
# groupby("pokemon_id"): Agrupa as 6 linhas de stats de cada Pokémon em um único bloco.
# ["base_stat"].sum(): Soma os valores dentro desse bloco.
bst_por_pokemon = df_stats.groupby("pokemon_id")["base_stat"].sum().reset_index()
bst_por_pokemon.columns = ["id", "BST"] # Renomeia colunas para ficar limpo

# --- Passo 2: Criar a Lista Completa da Família ---
# Precisamos listar TODOS os pokémons de uma cadeia, não apenas os que evoluem.
# Ex: Se pegarmos só "to_species", perdemos o Bulbasaur.
part_from = df_evolution[["chain_id", "from_species"]].rename(columns={"from_species": "name"})
part_to = df_evolution[["chain_id", "to_species"]].rename(columns={"to_species": "name"})

# concat: Empilha as listas (Pai em cima, Filho embaixo).
# drop_duplicates: Remove repetições (ex: Gloom evolui para Vileplume e Bellossom, ele apareceria 2x).
df_familia = pd.concat([part_from, part_to]).drop_duplicates().dropna()

# --- Passo 3: Enriquecer a Tabela (Joins) ---
# Adicionamos o ID (baseado no nome) e depois o BST (baseado no ID).
# 'inner': Só mantém se tiver dados nas duas pontas.
df_familia = df_familia.merge(df_pokemon, on="name", how="inner")
df_familia = df_familia.merge(bst_por_pokemon, on="id", how="inner")

# --- Passo 4: Definir a Ordem da Evolução ---
# Ordenamos primeiro pela Família (chain_id), depois pela Força (BST).
# Assumimos que a evolução é sempre mais forte que a pré-evolução.
df_familia = df_familia.sort_values(by=["chain_id", "BST"], ascending=[True, True])

# --- Passo 5: Criar a Coluna "Estágio" ---
# cumcount(): Conta sequencialmente dentro do grupo.
# O mais fraco da família vira 0, o médio 1, o forte 2.
# Somamos +1 para ficar legível (Estágio 1, 2, 3).
df_familia["estagio"] = df_familia.groupby("chain_id").cumcount() + 1
# clip(upper=3): Força qualquer coisa acima de 3 (Mega Evoluções) a ser considerada 3, para não quebrar o gráfico.
df_familia["estagio"] = df_familia["estagio"].clip(upper=3)

# --- Passo 6: Calcular o "Lucro" da Evolução (Delta) ---
# diff(): Subtrai o valor da linha atual pelo da linha anterior.
# Ex: Charmeleon (405) - Charmander (309) = 96 de ganho.
df_familia["delta_BST"] = df_familia.groupby("chain_id")["BST"].diff()

# ==============================================================================
# 4. DASHBOARD E STORYTELLING (Visualização)
# ==============================================================================

# --- Título e Introdução ---
st.title("🧬 A Matemática da Evolução Pokémon")
st.markdown("""
Esta análise investiga o **ganho de poder (BST)** quando um Pokémon evolui. 
Afinal, vale a pena gastar tempo treinando aquele Caterpie? O salto de poder é constante?
""")
st.divider() # Linha visual para separar seções

# --- KPI Section (Indicadores Chave) ---
st.header("1. O Salto de Poder Médio")
st.markdown("Quanto poder bruto um Pokémon ganha, em média, ao atingir o próximo estágio?")

# Cálculo das médias para exibir nos cartões
media_1_2 = df_familia[df_familia["estagio"] == 2]["delta_BST"].mean()
media_2_3 = df_familia[df_familia["estagio"] == 3]["delta_BST"].mean()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("De Base para Estágio 2", f"+{media_1_2:.0f} pts", help="Média de ganho da primeira evolução (Ex: Bulbasaur -> Ivysaur)")
with col2:
    st.metric("De Estágio 2 para Estágio 3", f"+{media_2_3:.0f} pts", help="Média de ganho da segunda evolução (Ex: Ivysaur -> Venusaur)")
with col3:
    st.info("💡 **Insight:** O ganho costuma ser ligeiramente maior na segunda evolução, recompensando a dedicação do treinador.")

# --- Gráfico de Barras ---
st.subheader("Comparativo Visual dos Ganhos")
df_barras = pd.DataFrame({
    "Transição": ["Base → 1ª Evolução", "1ª → 2ª Evolução"],
    "Ganho Médio (BST)": [media_1_2, media_2_3]
})
# Text_auto mostra o número em cima da barra
fig_bar = px.bar(df_barras, x="Transição", y="Ganho Médio (BST)", text_auto='.0f', color="Transição")
fig_bar.update_layout(showlegend=False) # Esconde legenda duplicada
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---") 

# --- Gráfico de Boxplot (Distribuição) ---
st.header("2. Nem todas as evoluções são iguais")
st.markdown("""
A média acima esconde a verdade: **alguns Pokémon explodem de poder, outros mal mudam.**
O gráfico abaixo mostra essa variação. 
* A **caixa** mostra onde está a maioria dos Pokémon.
* Os **pontos** (outliers) são casos extremos, como **Magikarp**, que ganha +340 pontos ao virar Gyarados!
""")

# Filtramos apenas as linhas que têm ganho (tiramos os Estágios 1 que são NaN)
df_validos = df_familia.dropna(subset=["delta_BST"]).copy()
# Criamos nomes amigáveis para o eixo X
df_validos["Tipo de Evolução"] = df_validos["estagio"].map({2: "1ª Evolução (Base -> Stage 2)", 3: "2ª Evolução (Stage 2 -> Stage 3)"})

fig_box = px.box(
    df_validos, 
    x="Tipo de Evolução", 
    y="delta_BST", 
    points="all", # Mostra todos os pontos individuais
    hover_data=["name"], # Mostra o nome do Pokémon ao passar o mouse (IMPORTANTE!)
    color="Tipo de Evolução"
)
st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")

# --- Gráfico Sankey (Fluxo) ---
st.header("3. O Caminho da Evolução")
st.markdown("""
Como os Pokémon chegam ao poder máximo? A maioria evolui por **nível**, mas pedras e trocas são atalhos comuns.
Este diagrama mostra o fluxo: **Método (Trigger) → Estágio Alvo**.
""")

# Recuperamos o trigger da tabela original fazendo um merge
df_trigger = df_familia.merge(df_evolution[["to_species", "trigger"]], left_on="name", right_on="to_species", how="left")

# Lógica para construir o Sankey
triggers = list(df_trigger["trigger"].dropna().unique())
estagios_nomes = ["Estágio Base", "Estágio 2", "Estágio 3"]
all_nodes = triggers + estagios_nomes
node_indices = {nome: i for i, nome in enumerate(all_nodes)} # Dicionário para mapear Nome -> Número

links = []
for _, row in df_trigger.dropna(subset=["trigger"]).iterrows():
    if row["estagio"] in [2, 3]: # Só queremos ver para onde a evolução vai
        origem = row["trigger"] # Ex: "level-up"
        destino = estagios_nomes[row["estagio"]-1] # Ex: "Estágio 2"
        
        links.append({
            "source": node_indices[origem],
            "target": node_indices[destino],
            "value": 1
        })

if links:
    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15, thickness=20, line=dict(color="black", width=0.5),
            label=all_nodes, color="lightblue"
        ),
        link=dict(
            source=[l["source"] for l in links],
            target=[l["target"] for l in links],
            value=[l["value"] for l in links]
        )
    )])
    st.plotly_chart(fig_sankey, use_container_width=True)

# --- Rodapé ---
with st.expander("🔎 Ver Tabela de Dados Completa"):
    st.markdown("Use esta tabela para conferir os dados brutos de qualquer Pokémon.")

    st.dataframe(df_familia[["name", "chain_id", "estagio", "BST", "delta_BST"]], use_container_width=True)
