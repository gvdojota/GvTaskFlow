import customtkinter as ctk
from datetime import datetime
from database import (
    carregar_dados, salvar_dados, 
    carregar_config, salvar_config, 
    carregar_abas, salvar_abas
)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Gv TaskFlow")  # <--- Podes mudar o nome do teu app aqui!
janela.geometry("580x780")

# --- DICIONÁRIO DE IDIOMAS ---
textos_idioma = {
    "Português": {
        "titulo": "✨ Minhas Tarefas",
        "placeholder_busca": "🔍  Pesquisar tarefa...",
        "placeholder_nova": "O que você precisa fazer hoje?",
        "lbl_prioridade": "⚡ PRIORIDADE",
        "btn_add": "+ Adicionar Tarefa",
        "btn_limpar": "Limpar Lista Completa",
        "btn_nova_aba": "+ Nova Aba",
        "sem_tarefas": "Tudo limpo por aqui! 🎉",
        "uma_tarefa": "1 tarefa pendente",
        "varias_tarefas": " tarefas pendentes",
        "pref_titulo": "⚙️ Preferências",
        "lbl_idioma": "Idioma / Language:",
        "lbl_cor": "Cor Principal da Tarefa:",
        "lbl_fonte": "Tamanho da Fonte:",
        "prio_nenhum": "Nenhum",
        "prio_baixa": "Baixa",
        "prio_media": "Média",
        "prio_alta": "Alta"
    },
    "English": {
        "titulo": "✨ My Tasks",
        "placeholder_busca": "🔍  Search task...",
        "placeholder_nova": "What do you need to do today?",
        "lbl_prioridade": "⚡ PRIORITY",
        "btn_add": "+ Add Task",
        "btn_limpar": "Clear Complete List",
        "sem_tarefas": "All clean here! 🎉",
        "uma_tarefa": "1 pending task",
        "varias_tarefas": " pending tasks",
        "pref_titulo": "⚙️ Preferences",
        "lbl_idioma": "Language:",
        "lbl_cor": "Main Task Color:",
        "lbl_fonte": "Font Size:",
        "prio_nenhum": "None",
        "prio_baixa": "Low",
        "prio_media": "Medium",
        "prio_alta": "High"
    }
}

config_inicial = carregar_config()
idioma_atual = config_inicial.get("idioma", "Português")
cor_atual_nome = config_inicial.get("cor", "Azul Clássico")
tamanho_fonte_nome = config_inicial.get("fonte", "Médio (14px)")

botoes_principais = []
menus_suspensos = []
itens_tarefas = []

lista_abas = carregar_abas()
aba_ativa = lista_abas[0] if lista_abas else "Geral"

def obter_tamanhos_fonte(nome_tamanho):
    if "Pequena" in nome_tamanho or "Small" in nome_tamanho:
        return {"tarefa": 12, "data": 10, "ui": 11}
    elif "Grande" in nome_tamanho or "Large" in nome_tamanho:
        return {"tarefa": 16, "data": 13, "ui": 15}
    else:
        return {"tarefa": 14, "data": 11, "ui": 13}

def obter_codigo_cor(nome_cor):
    mapa_cores = {
        "Azul Clássico": "#1f538d",
        "Verde Esmeralda": "#2fa572",
        "Roxo / Lavanda": "#6c5ce7",
        "Rosa / Magenta": "#e84393",
        "Laranja / Coral": "#e17055"
    }
    return mapa_cores.get(nome_cor, "#1f538d")

def aplicar_cor_imediata(nome_cor):
    global cor_atual_nome
    cor_atual_nome = nome_cor
    nova_cor_hex = obter_codigo_cor(nome_cor)
    
    for btn in botoes_principais:
        try:
            btn.configure(fg_color=nova_cor_hex)
        except Exception:
            pass
            
    for menu in menus_suspensos:
        try:
            menu.configure(fg_color=nova_cor_hex, button_color=nova_cor_hex, button_hover_color=nova_cor_hex)
        except Exception:
            pass

    salvar_config({"idioma": idioma_atual, "cor": cor_atual_nome, "fonte": tamanho_fonte_nome})

# --- TEMA (SOL / LUA) ---
def alternar_tema():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
        btn_tema.configure(text="🌙", fg_color="#E0E0E0", text_color="#333333")
    else:
        ctk.set_appearance_mode("Dark")
        btn_tema.configure(text="☀️", fg_color="#2B2B2B", text_color="#FFD700")

def atualizar_interface_completa():
    atualizar_textos_interface()
    atualizar_botoes_abas()
    reconstruir_lista_visual()

# --- PAINEL DE PREFERÊNCIAS ---
def abrir_preferencias():
    pref_janela = ctk.CTkToplevel(janela)
    pref_janela.title("Preferências")
    pref_janela.geometry("380x420")
    pref_janela.grab_set()
    pref_janela.bind("<Escape>", lambda e: pref_janela.destroy())

    t = textos_idioma[idioma_atual]

    lbl_pref_titulo = ctk.CTkLabel(pref_janela, text=t["pref_titulo"], font=("Segoe UI", 18, "bold"))
    lbl_pref_titulo.pack(pady=15)

    lbl_id = ctk.CTkLabel(pref_janela, text=t["lbl_idioma"], font=("Segoe UI", 13))
    lbl_id.pack(anchor="w", padx=30)

    def mudar_idioma(escolha):
        global idioma_atual
        idioma_atual = escolha
        salvar_config({"idioma": idioma_atual, "cor": cor_atual_nome, "fonte": tamanho_fonte_nome})
        atualizar_interface_completa()
        pref_janela.destroy()
        abrir_preferencias()

    menu_idioma = ctk.CTkOptionMenu(pref_janela, values=["Português", "English"], command=mudar_idioma, width=320)
    menu_idioma.set(idioma_atual)
    menu_idioma.pack(pady=5, padx=30)

    lbl_c = ctk.CTkLabel(pref_janela, text=t["lbl_cor"], font=("Segoe UI", 13))
    lbl_c.pack(anchor="w", padx=30, pady=(10, 0))

    cores_opcoes = ["Azul Clássico", "Verde Esmeralda", "Roxo / Lavanda", "Rosa / Magenta", "Laranja / Coral"]
    
    def mudar_cor_app(escolha):
        aplicar_cor_imediata(escolha)

    menu_cor = ctk.CTkOptionMenu(pref_janela, values=cores_opcoes, command=mudar_cor_app, width=320)
    menu_cor.set(cor_atual_nome)
    menu_cor.pack(pady=5, padx=30)

    lbl_f = ctk.CTkLabel(pref_janela, text=t["lbl_fonte"], font=("Segoe UI", 13))
    lbl_f.pack(anchor="w", padx=30, pady=(10, 0))

    fontes_opcoes = ["Pequena (12px)", "Médio (14px)", "Grande (16px)"]

    def mudar_fonte(escolha):
        global tamanho_fonte_nome
        tamanho_fonte_nome = escolha
        salvar_config({"idioma": idioma_atual, "cor": cor_atual_nome, "fonte": tamanho_fonte_nome})
        atualizar_interface_completa()

    menu_fonte = ctk.CTkOptionMenu(pref_janela, values=fontes_opcoes, command=mudar_fonte, width=320)
    menu_fonte.set(tamanho_fonte_nome)
    menu_fonte.pack(pady=5, padx=30)

# --- TOPO ---
frame_topo = ctk.CTkFrame(janela, fg_color="transparent")
frame_topo.pack(fill="x", padx=30, pady=(15, 5))

btn_config = ctk.CTkButton(
    frame_topo, text="⚙️", width=42, height=42, corner_radius=21,
    fg_color="transparent", border_width=1, font=("Segoe UI", 16),
    command=abrir_preferencias
)
btn_config.pack(side="left", padx=(0, 10))

titulo = ctk.CTkLabel(frame_topo, text="", font=("Segoe UI", 24, "bold"))
titulo.pack(side="left")

btn_tema = ctk.CTkButton(
    frame_topo, text="☀️", width=42, height=42, corner_radius=21,
    fg_color="#2B2B2B", hover_color="#3B3B3B", border_width=0, font=("Segoe UI", 16),
    text_color="#FFD700", command=alternar_tema
)
btn_tema.pack(side="right")

# --- CONTADOR ---
contador_label = ctk.CTkLabel(janela, text="", font=("Segoe UI", 13), text_color=("#666666", "#A0A0A0"))
contador_label.pack(anchor="w", padx=35, pady=(0, 5))

# --- BARRA DE ABAS ---
frame_abas_container = ctk.CTkScrollableFrame(
    janela, orientation="horizontal", height=45, 
    fg_color="transparent",
    scrollbar_fg_color="transparent"
)
frame_abas_container.pack(fill="x", padx=30, pady=(0, 5))

def selecionar_aba(nome_aba):
    global aba_ativa
    aba_ativa = nome_aba
    atualizar_botoes_abas()
    filtrar_tarefas()

def atualizar_botoes_abas():
    for widget in frame_abas_container.winfo_children():
        widget.destroy()

    for aba in lista_abas:
        is_ativo = (aba == aba_ativa)
        cor_bg = obter_codigo_cor(cor_atual_nome) if is_ativo else ("#E0E0E0", "#2B2B2B")
        cor_txt = "#FFFFFF" if is_ativo else ("#333333", "#DDDDDD")

        btn_aba = ctk.CTkButton(
            frame_abas_container, text=aba, height=32, corner_radius=16,
            fg_color=cor_bg, text_color=cor_txt, font=("Segoe UI", 12, "bold"),
            command=lambda a=aba: selecionar_aba(a)
        )
        btn_aba.pack(side="left", padx=3)

        def menu_clique_direito(event, a_exc=aba):
            global lista_abas, aba_ativa
            if len(lista_abas) > 1:
                from tkinter import messagebox
                if messagebox.askyesno("Excluir Categoria", f"Deseja realmente excluir a aba '{a_exc}'?"):
                    lista_abas.remove(a_exc)
                    salvar_abas(lista_abas)
                    if aba_ativa == a_exc:
                        aba_ativa = lista_abas[0]
                    atualizar_botoes_abas()
                    reconstruir_lista_visual()
            else:
                from tkinter import messagebox
                messagebox.showwarning("Aviso", "Você não pode excluir a última aba restante!")

        btn_aba.bind("<Button-3>", menu_clique_direito)
        btn_aba.bind("<Button-2>", menu_clique_direito)

    def criar_nova_aba():
        dlg = ctk.CTkInputDialog(text="Digite o nome da nova aba / categoria:", title="Nova Aba")
        nova = dlg.get_input()
        if nova and nova.strip():
            nome_limpo = nova.strip()
            if nome_limpo not in lista_abas:
                lista_abas.append(nome_limpo)
                salvar_abas(lista_abas)
                selecionar_aba(nome_limpo)

    t = textos_idioma[idioma_atual]
    btn_add_aba = ctk.CTkButton(
        frame_abas_container, text=t["btn_nova_aba"], height=32, corner_radius=16,
        fg_color="transparent", border_width=1, font=("Segoe UI", 12),
        command=criar_nova_aba
    )
    btn_add_aba.pack(side="left", padx=4)

# --- BARRA DE PESQUISA ---
campo_busca = ctk.CTkEntry(
    janela, placeholder_text="",
    width=500, height=40, corner_radius=10, font=("Segoe UI", 13)
)
campo_busca.pack(pady=(0, 10), padx=30)

# --- ENTRADA DE TAREFA E PRIORIDADE ---
frame_entrada_principal = ctk.CTkFrame(janela, fg_color="transparent")
frame_entrada_principal.pack(padx=30, pady=(0, 5), fill="x")

frame_esq = ctk.CTkFrame(frame_entrada_principal, fg_color="transparent")
frame_esq.pack(side="left", fill="x", expand=True, padx=(0, 10))

campo_tarefa = ctk.CTkEntry(
    frame_esq, placeholder_text="",
    height=45, corner_radius=10, font=("Segoe UI", 14)
)
campo_tarefa.pack(fill="x", expand=True)

frame_dir = ctk.CTkFrame(frame_entrada_principal, fg_color="transparent")
frame_dir.pack(side="right")

lbl_prioridade_titulo = ctk.CTkLabel(
    frame_dir, text="", 
    font=("Segoe UI", 12, "bold"), 
    text_color=("#1f538d", "#3b8ed0")
)
lbl_prioridade_titulo.pack(anchor="w", pady=(0, 3))

menu_prioridade = ctk.CTkOptionMenu(
    frame_dir, values=["Nenhum", "Baixa", "Média", "Alta"],
    width=130, height=45, corner_radius=10, font=("Segoe UI", 13, "bold")
)
menu_prioridade.set("Nenhum")
menu_prioridade.pack()
menus_suspensos.append(menu_prioridade)

# --- ÁREA DE LISTA ---
frame_lista = ctk.CTkScrollableFrame(
    janela, width=480, height=250, corner_radius=12,
    fg_color=("#F0F0F0", "#1E1E1E")
)
frame_lista.pack(pady=10, fill="both", expand=True, padx=30)

def atualizar_textos_interface():
    t = textos_idioma[idioma_atual]
    titulo.configure(text=t["titulo"])
    campo_busca.configure(placeholder_text=t["placeholder_busca"])
    campo_tarefa.configure(placeholder_text=t["placeholder_nova"])
    lbl_prioridade_titulo.configure(text=t["lbl_prioridade"])
    btn_add.configure(text=t["btn_add"])
    btn_limpar.configure(text=t["btn_limpar"])
    atualizar_botoes_abas()
    atualizar_contador()

def atualizar_contador():
    t = textos_idioma[idioma_atual]
    pendentes = sum(1 for item in itens_tarefas if item["aba"] == aba_ativa and item["check_var"].get() == 0)
    if pendentes == 0:
        contador_label.configure(text=t["sem_tarefas"])
    elif pendentes == 1:
        contador_label.configure(text=t["uma_tarefa"])
    else:
        contador_label.configure(text=f"{pendentes}{t['varias_tarefas']}")

def obter_peso_prioridade(prioridade):
    p = str(prioridade).lower()
    if "alta" in p or "high" in p:
        return 3
    elif "média" in p or "medium" in p:
        return 2
    elif "baixa" in p or "low" in p:
        return 1
    return 0

def obter_cor_prioridade(prioridade):
    p = str(prioridade).lower()
    if "alta" in p or "high" in p:
        return "#FF5252"
    elif "média" in p or "medium" in p:
        return "#FFB142"
    elif "baixa" in p or "low" in p:
        return "#33D9B2"
    return "#888888"

def criar_widget_tarefa(texto, data_hora, prioridade, aba, concluida=False):
    t_tam = obter_tamanhos_fonte(tamanho_fonte_nome)

    item_frame = ctk.CTkFrame(
        frame_lista, corner_radius=8, 
        fg_color=("#FFFFFF", "#2A2A2A")
    )
    
    check_var = ctk.IntVar(value=1 if concluida else 0)
    cor_prio = obter_cor_prioridade(prioridade)

    lbl_cor = ctk.CTkLabel(item_frame, text="●", font=("Segoe UI", t_tam["tarefa"] + 2), text_color=cor_prio)
    lbl_cor.pack(side="left", padx=(12, 5), pady=10)

    cor_texto_inicial = cor_prio if (prioridade != "Nenhum" and not concluida) else ("#000000", "#FFFFFF")
    if concluida:
        cor_texto_inicial = ("#888888", "#777777")

    check = ctk.CTkCheckBox(
        item_frame, text=texto, variable=check_var,
        font=("Segoe UI", t_tam["tarefa"], "bold"),
        text_color=cor_texto_inicial,
        checkbox_width=22, checkbox_height=22, corner_radius=6
    )
    check.pack(side="left", padx=5, pady=10)

    lbl_data = ctk.CTkLabel(
        item_frame, text=data_hora, 
        font=("Segoe UI", t_tam["data"]), text_color=("#888888", "#999999")
    )
    lbl_data.pack(side="left", padx=10, pady=10)

    def ao_marcar():
        if check_var.get() == 1:
            check.configure(text_color=("#888888", "#777777"))
        else:
            check.configure(text_color=cor_prio if prioridade != "Nenhum" else ("#000000", "#FFFFFF"))
        atualizar_contador()
        salvar_dados(itens_tarefas)

    check.configure(command=ao_marcar)

    item_data = {
        "frame": item_frame,
        "texto": texto,
        "data_hora": data_hora,
        "prioridade": prioridade,
        "aba": aba,
        "check_var": check_var,
        "checkbox": check
    }

    def deletar_tarefa():
        if item_data in itens_tarefas:
            itens_tarefas.remove(item_data)
        item_frame.destroy()
        atualizar_contador()
        salvar_dados(itens_tarefas)

    btn_deletar = ctk.CTkButton(
        item_frame, text="✕", width=28, height=28, corner_radius=14,
        fg_color="transparent", text_color=("#888888", "#AAAAAA"),
        hover_color=("#FFCCCC", "#5A2A2A"), font=("Segoe UI", 12, "bold"),
        command=deletar_tarefa
    )
    btn_deletar.pack(side="right", padx=10, pady=10)

    return item_data

def ordenar_e_exibir_tarefas():
    itens_tarefas.sort(key=lambda x: obter_peso_prioridade(x["prioridade"]), reverse=True)
    termo = campo_busca.get().lower()

    for item in itens_tarefas:
        item["frame"].pack_forget()

    for item in itens_tarefas:
        if item["aba"] == aba_ativa and (not termo or termo in item["texto"].lower()):
            item["frame"].pack(fill="x", pady=6, padx=5)

def reconstruir_lista_visual():
    global itens_tarefas
    dados_atuais = []
    for item in itens_tarefas:
        dados_atuais.append({
            "texto": item["texto"],
            "data_hora": item["data_hora"],
            "prioridade": item["prioridade"],
            "aba": item["aba"],
            "concluida": item["check_var"].get() == 1
        })
        item["frame"].destroy()
    
    itens_tarefas.clear()

    for d in dados_atuais:
        novo_item = criar_widget_tarefa(d["texto"], d["data_hora"], d["prioridade"], d["aba"], d["concluida"])
        itens_tarefas.append(novo_item)

    ordenar_e_exibir_tarefas()
    atualizar_contador()

def adicionar_tarefa():
    texto_tarefa = campo_tarefa.get().strip()
    
    if texto_tarefa == "":
        campo_tarefa.configure(border_color="#FF5252")
        return
    else:
        campo_tarefa.configure(border_color=["#1f538d", "#3b8ed0"])

    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    prioridade_sel = menu_prioridade.get()

    novo_item = criar_widget_tarefa(texto_tarefa, data_hora_atual, prioridade_sel, aba_ativa, concluida=False)
    itens_tarefas.append(novo_item)
    
    ordenar_e_exibir_tarefas()
    atualizar_contador()
    salvar_dados(itens_tarefas)

    campo_tarefa.delete(0, "end")
    campo_tarefa.focus()

def filtrar_tarefas(event=None):
    ordenar_e_exibir_tarefas()

campo_busca.bind("<KeyRelease>", filtrar_tarefas)

btn_add = ctk.CTkButton(
    janela, text="", width=500, height=45,
    corner_radius=10, font=("Segoe UI", 14, "bold"), command=adicionar_tarefa
)
btn_add.pack(pady=5)
botoes_principais.append(btn_add)

def limpar_tudo():
    global itens_tarefas
    novos_itens = []
    for item in itens_tarefas:
        if item["aba"] == aba_ativa:
            item["frame"].destroy()
        else:
            novos_itens.append(item)
    itens_tarefas = novos_itens
    atualizar_contador()
    salvar_dados(itens_tarefas)

btn_limpar = ctk.CTkButton(
    janela, text="", width=500, height=35,
    corner_radius=10, fg_color="transparent", border_width=1,
    font=("Segoe UI", 12), text_color=("#666666", "#AAAAAA"),
    command=limpar_tudo
)
btn_limpar.pack(pady=(0, 20))

campo_tarefa.bind("<Return>", lambda event: adicionar_tarefa())

atualizar_textos_interface()
aplicar_cor_imediata(cor_atual_nome)

dados_salvos = carregar_dados()
for d in dados_salvos:
    item_criado = criar_widget_tarefa(d["texto"], d["data_hora"], d["prioridade"], d["aba"], d["concluida"])
    itens_tarefas.append(item_criado)

ordenar_e_exibir_tarefas()
atualizar_contador()

janela.mainloop()