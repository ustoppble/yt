import subprocess
import re
import os
from fastapi import FastAPI, Query

app = FastAPI()

# Defina o diretório de downloads
DOWNLOAD_DIR = "/app/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def baixar_legenda(url, video_id):
    # Defina o comando para baixar a legenda usando yt-dlp
    comando = [
        "yt-dlp",
        "--write-auto-sub",
        "--sub-lang", "pt",
        "--skip-download",
        "--convert-subs", "vtt",
        "--no-part",  # Evita múltiplos arquivos de legenda
        "-o", f"{DOWNLOAD_DIR}/{video_id}.%(ext)s",
        url
    ]
    
    try:
        # Executa o comando e captura a saída
        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
        print("stdout:", resultado.stdout)  # Exibe a saída do comando
        print("stderr:", resultado.stderr)  # Exibe o erro caso ocorra
    except subprocess.CalledProcessError as e:
        # Captura o erro caso o comando falhe
        print("Erro ao baixar legenda:", e)
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)
        raise Exception(f"Falha ao baixar legenda: {e.stderr}")

    return f"{DOWNLOAD_DIR}/{video_id}.pt.vtt"

def limpar_vtt_conteudo(arquivo_vtt):
    # Lê o arquivo VTT
    with open(arquivo_vtt, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Limpeza do conteúdo do arquivo VTT
    conteudo = re.sub(r'WEBVTT.*?\n', '', conteudo, flags=re.DOTALL)
    conteudo = re.sub(r'Kind:.*?\n', '', conteudo, flags=re.DOTALL)
    conteudo = re.sub(r'Language:.*?\n', '', conteudo, flags=re.DOTALL)
    conteudo = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', conteudo)
    conteudo = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*?\n', '', conteudo)
    conteudo = re.sub(r'<c>', '', conteudo)
    conteudo = re.sub(r'</c>', '', conteudo)
    conteudo = re.sub(r'\[&nbsp;__&nbsp;\]', '', conteudo)
    conteudo = re.sub(r' +', ' ', conteudo)

    # Remove linhas repetidas
    linhas = conteudo.split('\n')
    linhas_filtradas = []
    for i, linha in enumerate(linhas):
        if i == 0 or linha.strip() != linhas[i-1].strip():
            if linha.strip():
                linhas_filtradas.append(linha.strip())

    # Retorna o texto processado
    return ' '.join(linhas_filtradas)

@app.get("/transcrever")
def transcrever(url: str = Query(...)):
    # Obtém o video_id a partir da URL
    video_id = url.split("v=")[-1].split("&")[0]
    
    try:
        # Baixa a legenda
        vtt_file = baixar_legenda(url, video_id)
        
        # Limpa o conteúdo da legenda e a retorna
        texto = limpar_vtt_conteudo(vtt_file)
        
        # Remove o arquivo de legenda após o processamento
        os.remove(vtt_file)
        
        return {"status": "ok", "transcricao": texto}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Endpoint de healthcheck para o Easypanel
@app.get("/health")
def health():
    return {"status": "ok"}
