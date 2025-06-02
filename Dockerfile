FROM python:3.10-slim

# atualiza e instala dependências do sistema
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# cria diretório de trabalho
WORKDIR /app

# copia o arquivo de cookies primeiro (isso garante que ele será copiado antes do código)
COPY cookies.json /app/cookies.json

# cria pasta para salvar legendas temporárias
RUN mkdir /app/downloads

# copia arquivos do projeto
COPY . .

# instala dependências python
RUN pip install --no-cache-dir -r requirements.txt

# expõe a porta
EXPOSE 8000

# roda a aplicação
CMD ["uvicorn", "api_legenda:app", "--host", "0.0.0.0", "--port", "8000"]
