import numpy as np
import pandas as pd
import yfinance as yf
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# 1️⃣ Coletar dados Forex
def coletar_dados_forex(par="EURUSD=X", periodo="6mo", intervalo="1h"):
    df = yf.download(par, period=periodo, interval=intervalo)
    df = df[["Close"]].dropna()
    return df

# 2️⃣ Preparar os dados para o Autoencoder
def preparar_dados(df, janela=50):
    scaler = MinMaxScaler(feature_range=(0, 1))
    df_scaled = scaler.fit_transform(df)

    X = []
    for i in range(janela, len(df_scaled)):
        X.append(df_scaled[i-janela:i, 0])

    X = np.array(X)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    return X, scaler

# 3️⃣ Criar um Autoencoder para detectar padrões anômalos
def criar_autoencoder(janela=50):
    modelo = Sequential([
        LSTM(50, activation='relu', input_shape=(janela, 1), return_sequences=True),
        LSTM(25, activation='relu', return_sequences=False),
        Dense(25, activation='relu'),
        Dense(janela, activation='linear')
    ])
    modelo.compile(optimizer="adam", loss="mean_squared_error")
    return modelo

# 4️⃣ Treinar o modelo
df = coletar_dados_forex()
X, scaler = preparar_dados(df)

modelo = criar_autoencoder()
modelo.fit(X, X, epochs=20, batch_size=32)

# Salvar modelo treinado
modelo.save("modelo_autoencoder.h5")

# 5️⃣ Testar o modelo
reconstruido = modelo.predict(X)
erro = np.mean(np.abs(reconstruido - X), axis=1)

# 6️⃣ Exibir anomalias no gráfico
plt.figure(figsize=(10, 5))
plt.plot(erro, label="Erro de Reconstrução")
plt.axhline(y=np.mean(erro) + 2*np.std(erro), color="r", linestyle="--", label="Limite Anômalo")
plt.title("Detecção de Anomalias no Mercado Forex")
plt.legend()
plt.show()
