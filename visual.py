import tkinter as tk
import config

numeros = (
    config.carregar_contatos()
)  # devolve a lista de contatos. Lista vazia se o arquivo nao existir.
texto = (
    config.carregar_mensagem()
)  # devolve o texto a enviar. Cai no padrao se o arquivo nao existir.

janela = tk.Tk()
listbox = tk.Listbox(janela)
entry = tk.Entry(janela)
text = tk.Text(janela)
button = tk.Button(janela, text="Adicionar numero", command=adicionar_numero)
