import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def coletar_dados_forex(par="EURUSD=X", periodo="1mo", intervalo="1h"):
    """Baixa dados históricos do par de moedas especificado"""
    df = yf.download(par, period=periodo, interval=intervalo)
    return df

# Coletar dados do EUR/USD
dados_forex = coletar_dados_forex()

# Exibir as 5 primeiras linhas dos dados coletados
print(dados_forex.head())

# Criar um gráfico do preço de fechamento
plt.figure(figsize=(10, 5))
plt.plot(dados_forex["Close"], label="Preço de Fechamento")
plt.title("Histórico de Preços Forex - EUR/USD")
plt.legend()
plt.show()
