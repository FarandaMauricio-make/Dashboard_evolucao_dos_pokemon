# Imagem base oficial do Python
FROM python:3.11-slim

# Evita problemas de buffer no output
ENV PYTHONUNBUFFERED=1

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir streamlit pandas plotly

# Expor a porta padrão do Streamlit
EXPOSE 8501

# Comando para rodar o Streamlit apontando para seu arquivo
CMD ["streamlit", "run", "poke_evo_buffs.py", "--server.port=8501", "--server.address=0.0.0.0"]
