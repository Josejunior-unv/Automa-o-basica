"""Leitura e escrita dos dados do projeto.

Tudo que precisa desses dados passa por aqui: o mensagem.py para enviar e
a interface para editar. Assim o formato dos arquivos fica num lugar so.

Sao tres arquivos:
  contatos.json  - a lista de numeros
  mensagem.json  - o texto a enviar
  ajustes.json   - o que depende da maquina (coordenada, esperas)
"""

import json
import sys
from pathlib import Path

# Dentro de um .exe do PyInstaller, __file__ aponta para uma pasta temporaria
# que e apagada ao fechar. Nesse caso os dados vao ao lado do executavel.
if getattr(sys, "frozen", False):
    PASTA = Path(sys.executable).parent
else:
    PASTA = Path(__file__).parent

ARQUIVO_CONTATOS = PASTA / "contatos.json"
ARQUIVO_MENSAGEM = PASTA / "mensagem.json"
ARQUIVO_AJUSTES = PASTA / "ajustes.json"

MENSAGEM_PADRAO = "Bom dia!"

# Valores que mudam de uma maquina para outra.
# Coordenada 0,0 significa "ninguem configurou ainda".
AJUSTES_PADRAO = {
    "caixa_mensagem_x": 0,
    "caixa_mensagem_y": 0,
    "espera_whatsapp": 10,
    "espera_busca": 2,
    "espera_conversa": 2,
    "espera_entre_contatos": 3,
}


def _gravar(caminho, dados):
    caminho.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def carregar_contatos():
    """Devolve a lista de contatos. Lista vazia se o arquivo nao existir."""
    if not ARQUIVO_CONTATOS.exists():
        return []
    dados = json.loads(ARQUIVO_CONTATOS.read_text(encoding="utf-8"))
    return dados.get("contatos", [])


def salvar_contatos(contatos):
    """Grava a lista de contatos, substituindo o que estava la."""
    _gravar(ARQUIVO_CONTATOS, {"contatos": list(contatos)})


def carregar_mensagem():
    """Devolve o texto a enviar. Cai no padrao se o arquivo nao existir."""
    if not ARQUIVO_MENSAGEM.exists():
        return MENSAGEM_PADRAO
    dados = json.loads(ARQUIVO_MENSAGEM.read_text(encoding="utf-8"))
    return dados.get("mensagem", MENSAGEM_PADRAO)


def salvar_mensagem(texto):
    """Grava o texto a enviar."""
    _gravar(ARQUIVO_MENSAGEM, {"mensagem": texto})


def carregar_ajustes():
    """Devolve os ajustes da maquina, completando o que faltar com o padrao."""
    ajustes = dict(AJUSTES_PADRAO)
    if ARQUIVO_AJUSTES.exists():
        salvos = json.loads(ARQUIVO_AJUSTES.read_text(encoding="utf-8"))
        ajustes.update({k: v for k, v in salvos.items() if k in AJUSTES_PADRAO})
    return ajustes


def salvar_ajustes(ajustes):
    """Grava os ajustes da maquina, ignorando chaves desconhecidas."""
    completo = dict(AJUSTES_PADRAO)
    completo.update({k: v for k, v in ajustes.items() if k in AJUSTES_PADRAO})
    _gravar(ARQUIVO_AJUSTES, completo)


def coordenada_configurada(ajustes=None):
    """A caixa de mensagem so vale se alguem configurou de fato (nao 0,0)."""
    if ajustes is None:
        ajustes = carregar_ajustes()
    return ajustes["caixa_mensagem_x"] > 0 and ajustes["caixa_mensagem_y"] > 0


if __name__ == "__main__":
    print("contatos:", len(carregar_contatos()))
    print("mensagem:", repr(carregar_mensagem()[:40]))
    print("ajustes:", carregar_ajustes())
    print("coordenada configurada?", coordenada_configurada())
