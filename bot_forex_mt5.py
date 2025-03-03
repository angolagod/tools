import MetaTrader5 as mt5
import time
import yfinance as yf
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Conectar ao MetaTrader5
if not mt5.initialize():
    print("Erro ao conectar ao MetaTrader5")
    mt5.shutdown()

# Configurações
PAR_MOEDA = "EURUSD"
VOLUME = 0.1  # Lote mínimo
STOP_LOSS_PERCENT = 0.005  # 0.5% de stop-loss
TAKE_PROFIT_PERCENT = 0.01  # 1% de take-profit

# Carregar modelo treinado
modelo = load_model("modelo_forex_lstm.h5")
scaler = MinMaxScaler(feature_range=(0, 1))

# Função para obter preço Forex em tempo real
def obter_preco():
    info = mt5.symbol_info_tick(PAR_MOEDA)
    return info.ask, info.bid

# Função para operar
def operar():
    preco_atual, _ = obter_preco()

    # Fazer previsão usando IA
    dados = yf.download("EURUSD=X", period="1mo", interval="1h")[["Close"]]
    dados_scaled = scaler.fit_transform(dados)
    dados_teste = np.reshape(dados_scaled[-50:], (1, 50, 1))
    previsao = modelo.predict(dados_teste)
    previsao = scaler.inverse_transform(previsao)

    # Definir Stop-Loss e Take-Profit
    stop_loss = preco_atual * (1 - STOP_LOSS_PERCENT)
    take_profit = preco_atual * (1 + TAKE_PROFIT_PERCENT)

    if previsao > preco_atual:
        ordem = mt5.OrderSend(
            {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": PAR_MOEDA,
                "volume": VOLUME,
                "type": mt5.ORDER_TYPE_BUY,
                "price": preco_atual,
                "sl": stop_loss,
                "tp": take_profit,
                "comment": "Compra AI",
            }
        )
        print(f"✅ COMPRA realizada! Preço: {preco_atual} SL: {stop_loss} TP: {take_profit}")

# Loop para operar a cada 1 hora
while True:
    operar()
    time.sleep(3600)
