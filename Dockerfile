# 1. Usar a imagem oficial leve do Python 3.11
FROM python:3.11-slim

# 2. Definir pasta de trabalho
WORKDIR /app

# 3. Atualizar o pip para garantir que ele baixe os wheels (binários) mais novos
RUN pip install --upgrade pip

# 4. Copiar e instalar requerimentos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar o restante dos arquivos (app e banco de dados)
COPY . .

# 6. Expor a porta
EXPOSE 8501

# 7. Verificação de saúde básica
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 8. Comando de execução
# IMPORTANTE: Verifique se o nome do arquivo é EXATAMENTE esse. 
# Se o seu arquivo se chamar "app.py", mude abaixo.
ENTRYPOINT ["streamlit", "run", "Poke_evo_buffs.py", "--server.port=8501", "--server.address=0.0.0.0"]
