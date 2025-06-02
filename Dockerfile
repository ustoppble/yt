# Usa a imagem oficial Python 3.11 slim
FROM python:3.11-slim

# Atualiza o sistema e instala as dependências necessárias para o ChromeDriver e Selenium
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    curl \
    unzip \
    wget \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libayatana-appindicator3-1 \
    libglib2.0-0 \
    && \
    curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && \
    chmod a+rx /usr/local/bin/yt-dlp && \
    wget https://chromedriver.storage.googleapis.com/115.0.5790.102/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver_linux64.zip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Cria diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 8000 (padrão uvicorn)
EXPOSE 8000

# Comando para rodar a API
CMD ["uvicorn", "api_legenda:app", "--host", "0.0.0.0", "--port", "8000"]
