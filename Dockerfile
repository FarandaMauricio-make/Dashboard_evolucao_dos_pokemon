# 1. Imagem base: Python 3.11 Slim
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do container
# Tudo que fizer vai acontecer dentro da pasta /app
WORKDIR /app

# 3. Instala dependências do sistema (necessário para algumas libs de cálculo)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# 4. Copia o arquivo de requisitos primeiro
# Fazemos isso antes de copiar o resto para o Docker fazer "cache" da instalação
COPY requirements.txt .

# 5. Instala as bibliotecas Python (Streamlit, Pandas, Plotly)
RUN pip install --no-cache-dir -r requirements.txt

# 6. PASSO CRÍTICO: Copia TODO o resto dos arquivos para o container
# Isso inclui o script .py E o arquivo 'pokemon_dw.db'
COPY . .

# 7. Expõe a porta padrão do Streamlit
EXPOSE 8501

# 8. Verificação de saúde (ajuda o Render a saber se o app travou)
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 9. Comando para iniciar o aplicativo
ENTRYPOINT ["streamlit", "run", "Poke_evo_buffs.py", "--server.port=8501", "--server.address=0.0.0.0"]
