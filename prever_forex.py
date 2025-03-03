import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# 1. Coletar dados do Forex
def coletar_dados_forex(par="EURUSD=X", periodo="1mo", intervalo="1h"):
    df = yf.download(par, period=periodo, interval=intervalo)
    df["Média Móvel"] = df["Close"].rolling(window=5).mean()
    df.dropna(inplace=True)  # Remover valores nulos
    return df

# 2. Criar modelo de IA para prever o próximo preço
def prever_tendencia(df):
    X = np.array(range(len(df))).reshape(-1, 1)
    y = df["Close"].values

    modelo = LinearRegression()
    modelo.fit(X, y)

    previsao = modelo.predict([[len(df) + 1]])
    return previsao[0]

# Rodar previsão
dados_forex = coletar_dados_forex()
previsao = prever_tendencia(dados_forex)

print(f"📈 Previsão do próximo preço: {previsao}")

# Criar um gráfico com a previsão
plt.figure(figsize=(10, 5))
plt.plot(dados_forex["Close"], label="Preço de Fechamento")
plt.axhline(y=previsao, color="r", linestyle="--", label="Previsão")
plt.title("Previsão Forex - EUR/USD")
plt.legend()
plt.show()
