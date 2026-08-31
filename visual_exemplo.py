"""Interface para configurar e disparar o envio das mensagens."""

import tkinter as tk
from tkinter import messagebox

import config

janela = tk.Tk()
janela.title("Envio WhatsApp")
janela.geometry("440x700")


# ---------- helpers ----------

def _ler_int(campo, nome, minimo=0):
    """Le um campo de texto como inteiro, avisando se estiver invalido."""
    try:
        valor = int(campo.get().strip())
    except ValueError:
        messagebox.showwarning("Valor invalido", f"{nome} precisa ser um numero inteiro.")
        return None
    if valor < minimo:
        messagebox.showwarning("Valor invalido", f"{nome} nao pode ser menor que {minimo}.")
        return None
    return valor


def _preencher(campo, valor):
    campo.delete(0, tk.END)
    campo.insert(0, str(valor))


# ---------- acoes ----------

def adicionar_numero():
    numero = campo_numero.get().strip()
    if not numero:
        messagebox.showwarning("Vazio", "Digite um numero antes de adicionar.")
        return
    if numero in lista_numeros.get(0, tk.END):
        messagebox.showwarning("Repetido", f"{numero} ja esta na lista.")
        return
    lista_numeros.insert(tk.END, numero)
    campo_numero.delete(0, tk.END)


def remover_selecionado():
    selecao = lista_numeros.curselection()
    if not selecao:
        messagebox.showwarning("Nada selecionado", "Clique num numero da lista.")
        return
    # de tras pra frente: apagar do inicio bagunca os indices seguintes
    for indice in reversed(selecao):
        lista_numeros.delete(indice)


def capturar_posicao():
    """Espera 5s e grava onde o mouse estiver: a caixa de texto do WhatsApp."""
    confirmou = messagebox.askyesno(
        "Capturar posicao",
        "Vou minimizar esta janela e capturar a posicao do mouse em 5 segundos.\n\n"
        "Deixe o WhatsApp aberto numa conversa e leve o mouse ate a\n"
        "caixa onde voce digita a mensagem. Nao precisa clicar.",
    )
    if not confirmou:
        return
    janela.iconify()
    # after() agenda sem travar a interface (um sleep aqui congelaria tudo)
    janela.after(5000, _gravar_posicao)


def _gravar_posicao():
    import pyautogui as pa

    x, y = pa.position()
    _preencher(campo_x, x)
    _preencher(campo_y, y)
    janela.deiconify()
    messagebox.showinfo("Capturado", f"Posicao da caixa de mensagem: ({x}, {y})")


def salvar():
    x = _ler_int(campo_x, "Posicao X")
    y = _ler_int(campo_y, "Posicao Y")
    espera = _ler_int(campo_espera, "Espera do WhatsApp", minimo=1)
    if x is None or y is None or espera is None:
        return False

    ajustes = config.carregar_ajustes()
    ajustes.update(
        {"caixa_mensagem_x": x, "caixa_mensagem_y": y, "espera_whatsapp": espera}
    )

    config.salvar_contatos(list(lista_numeros.get(0, tk.END)))
    config.salvar_mensagem(campo_mensagem.get("1.0", tk.END).strip())
    config.salvar_ajustes(ajustes)
    return True


def salvar_com_aviso():
    if salvar():
        messagebox.showinfo("Salvo", "Contatos, mensagem e ajustes foram salvos.")


def enviar_agora():
    numeros = list(lista_numeros.get(0, tk.END))
    if not numeros:
        messagebox.showwarning("Lista vazia", "Adicione pelo menos um numero.")
        return
    if not salvar():
        return

    ajustes = config.carregar_ajustes()
    if config.coordenada_configurada(ajustes):
        modo = "com clique na caixa de mensagem"
    else:
        modo = "apenas teclado (sem posicao configurada)"

    minutos = estimar_minutos(len(numeros), ajustes)
    confirmou = messagebox.askyesno(
        "Confirmar envio",
        f"Enviar para {len(numeros)} contato(s) AGORA?\n\n"
        f"Modo: {modo}.\n"
        f"Tempo estimado: {minutos}.\n\n"
        "Nao mexa no mouse nem no teclado durante o envio.\n"
        "Para abortar: jogue o mouse no canto superior esquerdo da tela.",
    )
    if not confirmou:
        return

    import mensagem  # so aqui: importar no topo carregaria o pyautogui a toa

    janela.iconify()  # tira a janela da frente do WhatsApp
    janela.update()
    try:
        mensagem.enviar_todos()
    finally:
        janela.deiconify()  # volta mesmo se der erro no meio
    messagebox.showinfo("Fim", "Envio concluido. Confira o WhatsApp.")


def estimar_minutos(quantidade, ajustes):
    """Estimativa grosseira do tempo total, so para avisar o usuario."""
    por_contato = (
        1
        + ajustes["espera_busca"]
        + ajustes["espera_conversa"]
        + 1.0
        + ajustes["espera_entre_contatos"]
        + 1.7  # digitacao e as pausas internas do pyautogui
    )
    total = 12.5 + quantidade * por_contato
    return f"{int(total // 60)} min {int(total % 60)} s"


# ---------- montagem da tela ----------

tk.Label(janela, text="Numeros", font=("Segoe UI", 10, "bold")).pack(pady=(10, 0))

lista_numeros = tk.Listbox(janela, height=8, selectmode=tk.EXTENDED)
lista_numeros.pack(fill="x", padx=10, pady=5)

linha_add = tk.Frame(janela)
linha_add.pack(fill="x", padx=10)
campo_numero = tk.Entry(linha_add)
campo_numero.pack(side="left", fill="x", expand=True)
campo_numero.bind("<Return>", lambda evento: adicionar_numero())
tk.Button(linha_add, text="Adicionar", command=adicionar_numero).pack(side="left", padx=(5, 0))

tk.Button(janela, text="Remover selecionado", command=remover_selecionado).pack(pady=5)

tk.Label(janela, text="Mensagem", font=("Segoe UI", 10, "bold")).pack(pady=(10, 0))
campo_mensagem = tk.Text(janela, height=5, wrap="word")
campo_mensagem.pack(fill="x", padx=10, pady=5)

# --- ajustes desta maquina ---
grupo = tk.LabelFrame(janela, text="Ajustes desta maquina", font=("Segoe UI", 9, "bold"))
grupo.pack(fill="x", padx=10, pady=(10, 5))

tk.Label(
    grupo,
    text=(
        "Posicao e opcional: em 0,0 o envio usa so o teclado.\n"
        "Configure se a mensagem nao estiver sendo digitada."
    ),
    font=("Segoe UI", 8),
    justify="left",
    fg="#555555",
).pack(padx=8, pady=(6, 0), anchor="w")

linha_xy = tk.Frame(grupo)
linha_xy.pack(fill="x", padx=8, pady=(8, 4))
tk.Label(linha_xy, text="Caixa de mensagem  X:").pack(side="left")
campo_x = tk.Entry(linha_xy, width=6)
campo_x.pack(side="left", padx=(4, 8))
tk.Label(linha_xy, text="Y:").pack(side="left")
campo_y = tk.Entry(linha_xy, width=6)
campo_y.pack(side="left", padx=4)

tk.Button(grupo, text="Capturar posicao", command=capturar_posicao).pack(pady=4)

linha_espera = tk.Frame(grupo)
linha_espera.pack(fill="x", padx=8, pady=(4, 8))
tk.Label(linha_espera, text="Segundos para o WhatsApp abrir:").pack(side="left")
campo_espera = tk.Entry(linha_espera, width=5)
campo_espera.pack(side="left", padx=4)

tk.Button(janela, text="Salvar", command=salvar_com_aviso).pack(pady=5)
tk.Button(janela, text="Enviar agora", command=enviar_agora, bg="#c8e6c9").pack(pady=(0, 10))


# ---------- carregar o que ja esta salvo ----------

for numero in config.carregar_contatos():
    lista_numeros.insert(tk.END, numero)
campo_mensagem.insert("1.0", config.carregar_mensagem())

_ajustes = config.carregar_ajustes()
_preencher(campo_x, _ajustes["caixa_mensagem_x"])
_preencher(campo_y, _ajustes["caixa_mensagem_y"])
_preencher(campo_espera, _ajustes["espera_whatsapp"])

janela.mainloop()
