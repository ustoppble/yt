FROM python:3.11-slim

# atualiza o sistema e instala dependências do sistema (ffmpeg e yt-dlp)
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && \
    chmod a+rx /usr/local/bin/yt-dlp && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# cria diretório de trabalho
WORKDIR /app

# copia arquivos do projeto
COPY . .

# instala dependências python
RUN pip install --no-cache-dir -r requirements.txt

# expõe a porta 8000 (padrão uvicorn)
EXPOSE 8000

# comando para rodar a API
CMD ["uvicorn", "api_legenda:app", "--host", "0.0.0.0", "--port", "8000"]
