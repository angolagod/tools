import numpy as np
import pandas as pd
import yfinance as yf
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# 1️⃣ Coletar dados Forex
def coletar_dados_forex(par="EURUSD=X", periodo="6mo", intervalo="1h"):
    df = yf.download(par, period=periodo, interval=intervalo)
    df = df[["Close"]].dropna()
    return df

# 2️⃣ Preparar os dados para a Rede Neural
def preparar_dados(df, janela=50):
    scaler = MinMaxScaler(feature_range=(0, 1))
    df_scaled = scaler.fit_transform(df)

    X, y = [], []
    for i in range(janela, len(df_scaled)):
        X.append(df_scaled[i-janela:i, 0])
        y.append(df_scaled[i, 0])

    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    return X, y, scaler

# 3️⃣ Criar modelo de Rede Neural LSTM mais profunda
def criar_modelo(janela=50):
    modelo = Sequential([
        LSTM(units=100, return_sequences=True, input_shape=(janela, 1)),
        Dropout(0.2),
        LSTM(units=100, return_sequences=True),
        Dropout(0.2),
        LSTM(units=50, return_sequences=False),
        Dense(units=25),
        Dense(units=1)
    ])
    modelo.compile(optimizer="adam", loss="mean_squared_error")
    return modelo

# 4️⃣ Treinar e testar o modelo
df = coletar_dados_forex()
X, y, scaler = preparar_dados(df)

modelo = criar_modelo()
modelo.fit(X, y, epochs=10, batch_size=32)

# Salvar o modelo treinado
modelo.save("modelo_forex_lstm.h5")

# 5️⃣ Fazer previsões
dados_teste = df[-50:].values
dados_teste = scaler.transform(dados_teste)
dados_teste = np.reshape(dados_teste, (1, dados_teste.shape[0], 1))

previsao = modelo.predict(dados_teste)
previsao = scaler.inverse_transform(previsao)

print(f"📈 Previsão do próximo preço: {previsao[0][0]}")

# 6️⃣ Criar um gráfico com a previsão
plt.figure(figsize=(10, 5))
plt.plot(df.index[-200:], df["Close"][-200:], label="Preço Real")
plt.axhline(y=previsao, color="r", linestyle="--", label="Previsão")
plt.title("Previsão Forex com LSTM - EUR/USD")
plt.legend()
plt.show()
