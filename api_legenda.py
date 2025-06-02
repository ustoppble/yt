import subprocess
import re
import os
from fastapi import FastAPI, Query

app = FastAPI()

def baixar_legenda(url, video_id):
    comando = [
        "yt-dlp",
        "--write-auto-sub",
        "--sub-lang", "pt",
        "--skip-download",
        "--convert-subs", "vtt",
        "--no-part",
        "-o", f"{video_id}.%(ext)s",
        url
    ]
    subprocess.run(comando, check=True)
    return f"{video_id}.pt.vtt"

def limpar_vtt_conteudo(arquivo_vtt):
    with open(arquivo_vtt, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # limpeza bruta
    conteudo = re.sub(r'WEBVTT.*?\n', '', conteudo, flags=re.DOTALL)
    conteudo = re.sub(r'Kind:.*?\n', '', conteudo, flags=re.DOTALL)
    conteudo = re.sub(r'Language:.*?\n', '', conteudo, flags=re.DOTALL)
    conteudo = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', conteudo)
    conteudo = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*?\n', '', conteudo)
    conteudo = re.sub(r'<c>', '', conteudo)
    conteudo = re.sub(r'</c>', '', conteudo)
    conteudo = re.sub(r'\[&nbsp;__&nbsp;\]', '', conteudo)
    conteudo = re.sub(r' +', ' ', conteudo)
    
    # separa em frases pelo \n
    linhas = conteudo.split('\n')
    
    # remove duplicatas exatas
    frases = []
    for linha in linhas:
        linha = linha.strip()
        if linha and linha not in frases:
            frases.append(linha)

    # junta tudo
    texto_final = ' '.join(frases)
    return texto_final

@app.get("/transcrever")
def transcrever(url: str = Query(...)):
    video_id = url.split("v=")[-1].split("&")[0]
    vtt_file = baixar_legenda(url, video_id)
    texto = limpar_vtt_conteudo(vtt_file)
    os.remove(vtt_file)
    return {"status": "ok", "transcricao": texto}
