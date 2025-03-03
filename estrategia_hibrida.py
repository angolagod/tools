import yfinance as yf
import pandas as pd
import ta

# 1️⃣ Coletar dados Forex
def coletar_dados(par="EURUSD=X"):
    df = yf.download(par, period="1mo", interval="1h")
    df["SMA"] = ta.trend.sma_indicator(df["Close"], window=14)
    df["RSI"] = ta.momentum.rsi(df["Close"], window=14)
    df["MACD"] = ta.trend.macd(df["Close"])
    df.dropna(inplace=True)
    return df

# 2️⃣ Criar Regras da Estratégia
def tomar_decisao(df):
    ultima_linha = df.iloc[-1]
    
    # Regras:
    if ultima_linha["RSI"] < 30 and ultima_linha["Close"] > ultima_linha["SMA"]:
        return "COMPRA"
    elif ultima_linha["RSI"] > 70 and ultima_linha["Close"] < ultima_linha["SMA"]:
        return "VENDA"
    else:
        return "AGUARDAR"

# 3️⃣ Testar Estratégia
dados_forex = coletar_dados()
acao = tomar_decisao(dados_forex)

print(f"📊 Decisão de negociação: {acao}")
