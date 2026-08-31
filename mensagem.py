"""Envio das mensagens pelo WhatsApp Desktop, via automacao de teclado/mouse.

Nada aqui e fixo por maquina: coordenada e tempos vem do ajustes.json.
"""

import pyautogui as pa

import config


def abrir_whatsapp(ajustes):
    """Abre o WhatsApp uma vez so, antes de comecar a rodar a lista."""
    pa.press("win")
    pa.sleep(1)  # menu iniciar abrir
    pa.write("whatsapp")
    pa.sleep(1.5)  # a busca do Windows achar o app
    pa.press("enter")
    pa.sleep(ajustes["espera_whatsapp"])  # abrir E carregar as conversas


def enviar_para(contato, texto, ajustes):
    """Assume o WhatsApp ja aberto. Busca o contato e manda a mensagem."""
    pa.hotkey("ctrl", "f")  # barra de busca do WhatsApp
    pa.sleep(1)
    pa.hotkey("ctrl", "a")  # limpa a busca do contato anterior
    pa.press("delete")
    pa.write(contato)
    pa.sleep(ajustes["espera_busca"])  # ESSENCIAL: esperar a lista filtrar

    pa.press("enter")  # 1o resultado, agora ja filtrado
    pa.sleep(ajustes["espera_conversa"])  # a conversa abrir

    # Foco na caixa de texto. Com a posicao configurada, clica nela (mais
    # seguro). Sem posicao, confia no foco que o WhatsApp da sozinho ao
    # abrir a conversa - funciona quase sempre, mas nao e garantido.
    if config.coordenada_configurada(ajustes):
        pa.click(ajustes["caixa_mensagem_x"], ajustes["caixa_mensagem_y"])
        pa.sleep(0.5)

    pa.write(texto, interval=0.01)  # interval: digitacao mais estavel
    pa.sleep(0.5)
    pa.press("enter")


def enviar_todos(contatos=None, texto=None, ajustes=None):
    """Le do JSON o que nao for passado explicitamente."""
    if contatos is None:
        contatos = config.carregar_contatos()
    if texto is None:
        texto = config.carregar_mensagem()
    if ajustes is None:
        ajustes = config.carregar_ajustes()

    if not contatos:
        print("Nenhum contato em contatos.json. Nada a fazer.")
        return

    if config.coordenada_configurada(ajustes):
        print("Modo: clique na caixa de mensagem "
              f"({ajustes['caixa_mensagem_x']}, {ajustes['caixa_mensagem_y']})")
    else:
        print("Modo: apenas teclado (posicao da caixa nao configurada)")

    abrir_whatsapp(ajustes)
    for i, contato in enumerate(contatos, 1):
        print(f"[{i}/{len(contatos)}] enviando para {contato}")
        enviar_para(contato, texto, ajustes)
        pa.sleep(ajustes["espera_entre_contatos"])
    print("Todos enviados.")


if __name__ == "__main__":
    enviar_todos()
