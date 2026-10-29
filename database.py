import json
import os
from datetime import datetime

ARQUIVO_DADOS = "tarefas.json"
ARQUIVO_CONFIG = "config.json"
ARQUIVO_ABAS = "abas.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                for d in dados:
                    if "data_hora" not in d:
                        d["data_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                    if "prioridade" not in d:
                        d["prioridade"] = "Nenhum"
                    if "aba" not in d:
                        d["aba"] = "Geral"
                return dados
        except Exception:
            return []
    return []

def salvar_dados(itens_tarefas):
    dados = []
    for item in itens_tarefas:
        dados.append({
            "texto": item["texto"],
            "data_hora": item["data_hora"],
            "prioridade": item["prioridade"],
            "aba": item["aba"],
            "concluida": item["check_var"].get() == 1
        })
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def carregar_config():
    if os.path.exists(ARQUIVO_CONFIG):
        try:
            with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"idioma": "Português", "cor": "Azul Clássico", "fonte": "Médio (14px)"}

def salvar_config(config_dict):
    with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config_dict, f, ensure_ascii=False, indent=4)

def carregar_abas():
    if os.path.exists(ARQUIVO_ABAS):
        try:
            with open(ARQUIVO_ABAS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return ["Geral", "Trabalho", "Pessoal"]

def salvar_abas(abas):
    with open(ARQUIVO_ABAS, "w", encoding="utf-8") as f:
        json.dump(abas, f, ensure_ascii=False, indent=4)