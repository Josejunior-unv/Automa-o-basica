from datetime import date, timedelta
import calendar

dia_alvo = 31  # TESTE - devolver para 20 depois


def data_do_mes(ano, mes, dia):
    ultimo = calendar.monthrange(ano, mes)[1]  # É POR CONTA DO FEV PIT DOG
    return date(ano, mes, min(dia, ultimo))


def FDS(d):
    return d.weekday() >= 5


def antecipar_para_sexta(d):
    while FDS(d):
        d -= timedelta(days=1)
    return d


def datas_de_execucao(ano):
    """As 12 datas do ano em que o script deve rodar."""
    datas = []
    for mes in range(1, 13):
        alvo = data_do_mes(ano, mes, dia_alvo)
        datas.append(antecipar_para_sexta(alvo))
    return datas


def eh_dia_de_execucao(d):
    return d in datas_de_execucao(d.year)


# So roda quando voce abre ESTE arquivo direto, nao quando ele e importado
if __name__ == "__main__":
    for d in datas_de_execucao(date.today().year):
        print(d.strftime("%d/%m/%Y"))
