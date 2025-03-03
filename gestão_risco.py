CAPITAL_TOTAL = 10000  # Capital disponível
RISCO_POR_OPERACAO = 0.02  # 2% do capital
STOP_LOSS_PERCENT = 0.01  # Stop-Loss de 1%
TAKE_PROFIT_PERCENT = 0.02  # Take-Profit de 2%

def calcular_volume(preco_atual):
    """ Calcula o volume de negociação baseado no risco """
    risco_maximo = CAPITAL_TOTAL * RISCO_POR_OPERACAO
    volume = risco_maximo / (preco_atual * STOP_LOSS_PERCENT)
    return round(volume, 2)
