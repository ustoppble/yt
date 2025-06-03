FROM python:3.10.17-bookworm

# Variáveis de ambiente
ENV PYTHONPATH=/usr/local/bin
ENV PORT=8000
ENV LANG=C.UTF-8

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    wget \
    unzip \
    nano \
    sudo \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libayatana-appindicator3-1 \
    chromium \
    chromium-sandbox \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicação
COPY . .

# Expor porta
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "api_legenda:app", "--host", "0.0.0.0", "--port", "8000"]
