import MetaTrader5 as mt5
import time
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression

# Conectar ao MetaTrader5
if not mt5.initialize():
    print("Erro ao conectar ao MetaTrader5")
    mt5.shutdown()

# Definir o par de moedas e volume
PAR_MOEDA = "EURUSD"
VOLUME = 0.1  # Lote mínimo

# Função para coletar preços Forex
def coletar_dados_forex(par="EURUSD=X", periodo="1mo", intervalo="1h"):
    df = yf.download(par, period=periodo, interval=intervalo)
    df["Média Móvel"] = df["Close"].rolling(window=5).mean()
    df.dropna(inplace=True)
    return df

# Função para prever tendência
def prever_tendencia(df):
    X = np.array(range(len(df))).reshape(-1, 1)
    y = df["Close"].values

    modelo = LinearRegression()
    modelo.fit(X, y)

    previsao = modelo.predict([[len(df) + 1]])
    return previsao[0]

# Função para executar compra/venda
def operar():
    dados = coletar_dados_forex()
    previsao = prever_tendencia(dados)

    preco_atual = dados["Close"].iloc[-1]

    # Definir estratégia de compra/venda
    if previsao > preco_atual:
        ordem = mt5.OrderSend(
            {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": PAR_MOEDA,
                "volume": VOLUME,
                "type": mt5.ORDER_TYPE_BUY,
                "price": mt5.symbol_info_tick(PAR_MOEDA).ask,
                "deviation": 10,
                "magic": 0,
                "comment": "Compra AI",
                "type_filling": mt5.ORDER_FILLING_FOK,
            }
        )
        print(f"✅ COMPRA realizada! Preço: {preco_atual}")
    
    elif previsao < preco_atual:
        ordem = mt5.OrderSend(
            {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": PAR_MOEDA,
                "volume": VOLUME,
                "type": mt5.ORDER_TYPE_SELL,
                "price": mt5.symbol_info_tick(PAR_MOEDA).bid,
                "deviation": 10,
                "magic": 0,
                "comment": "Venda AI",
                "type_filling": mt5.ORDER_FILLING_FOK,
            }
        )
        print(f"❌ VENDA realizada! Preço: {preco_atual}")

# Loop para operar automaticamente
while True:
    operar()
    time.sleep(3600)  # Atualiza a cada hora
