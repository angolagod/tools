import numpy as np
import pandas as pd
import yfinance as yf
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Conv1D, MaxPooling1D, Flatten, Dense, Dropout
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# 1️⃣ Coletar dados Forex
def coletar_dados_forex(par="EURUSD=X", periodo="6mo", intervalo="1h"):
    df = yf.download(par, period=periodo, interval=intervalo)
    df = df[["Close"]].dropna()
    return df

# 2️⃣ Preparar os dados
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

# 3️⃣ Criar Modelo Avançado CNN + LSTM
def criar_modelo(janela=50):
    modelo = Sequential([
        Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(janela, 1)),
        MaxPooling1D(pool_size=2),
        LSTM(units=100, return_sequences=True),
        Dropout(0.2),
        LSTM(units=50, return_sequences=False),
        Dense(units=25),
        Dense(units=1)
    ])
    modelo.compile(optimizer="adam", loss="mean_squared_error")
    return modelo

# 4️⃣ Treinar o Modelo
df = coletar_dados_forex()
X, y, scaler = preparar_dados(df)

modelo = criar_modelo()
modelo.fit(X, y, epochs=15, batch_size=32)

# Salvar modelo treinado
modelo.save("modelo_forex_cnn_lstm.h5")

# 5️⃣ Fazer Previsões
dados_teste = df[-50:].values
dados_teste = scaler.transform(dados_teste)
dados_teste = np.reshape(dados_teste, (1, 50, 1))

previsao = modelo.predict(dados_teste)
previsao = scaler.inverse_transform(previsao)

print(f"📈 Previsão do próximo preço: {previsao[0][0]}")

# Criar um gráfico com a previsão
plt.figure(figsize=(10, 5))
plt.plot(df.index[-200:], df["Close"][-200:], label="Preço Real")
plt.axhline(y=previsao, color="r", linestyle="--", label="Previsão")
plt.title("Previsão Forex com CNN + LSTM - EUR/USD")
plt.legend()
plt.show()
