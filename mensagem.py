import pyautogui as pa
from Contatos import CONTATOS

TEXTO = "Bom dia meu amor, tudo bem? Espero que sim, te amo muito e que seu dia seja maravilhoso"


def abrir_whatsapp():
    """Abre o WhatsApp uma vez so, antes de comecar a rodar a lista."""
    pa.press("win")
    pa.sleep(1)  # menu iniciar abrir
    pa.write("whatsapp")
    pa.sleep(1.5)  # a busca do Windows achar o app
    pa.press("enter")
    pa.sleep(10)  # WhatsApp abrir E carregar a lista de conversas


def enviar_para(contato, texto=TEXTO):
    """Assume o WhatsApp ja aberto. Busca o contato e manda a mensagem."""
    pa.click(2129, 127)  # barra de busca do WhatsApp
    pa.sleep(1)
    pa.hotkey("ctrl", "a")  # limpa a busca do contato anterior
    pa.press("delete")
    pa.write(contato)
    pa.sleep(2)  # ESSENCIAL: esperar a lista filtrar

    pa.click(2167, 279)  # 1o resultado, agora ja filtrado
    pa.sleep(2)  # a conversa abrir

    pa.click(2555, 679)  # caixa de mensagem
    pa.sleep(0.5)
    pa.write(texto)
    pa.sleep(0.5)
    pa.press("enter")


def enviar_todos(contatos=CONTATOS, texto=TEXTO):
    abrir_whatsapp()
    for i, contato in enumerate(contatos, 1):
        print(f"[{i}/{len(contatos)}] enviando para {contato}")
        enviar_para(contato, texto)
        pa.sleep(3)  # respiro entre um envio e o proximo
    print("Todos enviados.")


if __name__ == "__main__":
    enviar_todos()
