from datetime import date
from pathlib import Path

import calendario
import mensagem

CONTROLE = Path(__file__).parent / "ultimo_envio.txt"


def ja_enviou_hoje(hoje):
    if not CONTROLE.exists():
        return False
    return CONTROLE.read_text().strip() == hoje.isoformat()


def marcar_enviado(hoje):
    CONTROLE.write_text(hoje.isoformat())


hoje = date.today()

if not calendario.eh_dia_de_execucao(hoje):
    print(f"{hoje:%d/%m/%Y} nao e dia de execucao. Nada a fazer.")
elif ja_enviou_hoje(hoje):
    print(f"{hoje:%d/%m/%Y} ja foi enviado. Nada a fazer.")
else:
    print(f"{hoje:%d/%m/%Y} e dia de execucao. Enviando...")
    mensagem.enviar_todos()
    marcar_enviado(hoje)
    print("Enviado.")
