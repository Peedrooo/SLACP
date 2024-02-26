import datetime

# Obter a data atual
data_atual = datetime.datetime.now()

# Extrair o dia e o mês
dia_atual = data_atual.day
mes_atual = data_atual.month

def dia_mes():
    return dia_atual, mes_atual

