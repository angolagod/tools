import MetaTrader5 as mt5
import time
import yfinance as yf
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from gestao_risco import calcular_volume
from telegram_alerta import enviar_mensagem

# Avisar que o bot iniciou
enviar_mensagem("🚀 O Bot Forex está rodando no Heroku!")

def operar():
    for par in PARES:
        preco_atual, _ = obter_preco(par)

        # Fazer previsão usando IA
        dados = yf.download(f"{par}=X", period="1mo", interval="1h")[["Close"]]
        dados_scaled = scaler.fit_transform(dados)
        dados_teste = np.reshape(dados_scaled[-50:], (1, 50, 1))
        previsao = modelo.predict(dados_teste)
        previsao = scaler.inverse_transform(previsao)

        stop_loss = preco_atual * (1 - STOP_LOSS_PERCENT)
        take_profit = preco_atual * (1 + TAKE_PROFIT_PERCENT)

        if previsao > preco_atual:
            ordem = mt5.OrderSend({
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": par,
                "volume": VOLUME,
                "type": mt5.ORDER_TYPE_BUY,
                "price": preco_atual,
                "sl": stop_loss,
                "tp": take_profit,
                "comment": "Compra AI",
            })
            enviar_mensagem(f"✅ COMPRA realizada para {par}! 💰 Preço: {preco_atual}")

        elif previsao < preco_atual:
            ordem = mt5.OrderSend({
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": par,
                "volume": VOLUME,
                "type": mt5.ORDER_TYPE_SELL,
                "price": preco_atual,
                "sl": stop_loss,
                "tp": take_profit,
                "comment": "Venda AI",
            })
            enviar_mensagem(f"❌ VENDA realizada para {par}! 💰 Preço: {preco_atual}")


VOLUME = calcular_volume(preco_atual)  # Calcula volume baseado no risco

# Conectar ao MetaTrader5
if not mt5.initialize():
    print("Erro ao conectar ao MetaTrader5")
    mt5.shutdown()

# Configurações dos pares de moedas
PARES = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]
VOLUME = 0.1  # Lote mínimo
STOP_LOSS_PERCENT = 0.005  # 0.5% de stop-loss
TAKE_PROFIT_PERCENT = 0.01  # 1% de take-profit

# Carregar modelo treinado
modelo = load_model("modelo_forex_lstm.h5")
scaler = MinMaxScaler(feature_range=(0, 1))

# Função para obter preço Forex em tempo real
def obter_preco(par):
    info = mt5.symbol_info_tick(par)
    return info.ask, info.bid

# Função para operar com múltiplos pares de moedas
from enviar_alertas import enviar_mensagem

def operar():
    for par in PARES:
        preco_atual, _ = obter_preco(par)

        # Fazer previsão usando IA
        dados = yf.download(f"{par}=X", period="1mo", interval="1h")[["Close"]]
        dados_scaled = scaler.fit_transform(dados)
        dados_teste = np.reshape(dados_scaled[-50:], (1, 50, 1))
        previsao = modelo.predict(dados_teste)
        previsao = scaler.inverse_transform(previsao)

        stop_loss = preco_atual * (1 - STOP_LOSS_PERCENT)
        take_profit = preco_atual * (1 + TAKE_PROFIT_PERCENT)

        if previsao > preco_atual:
            ordem = mt5.OrderSend(
                {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": par,
                    "volume": VOLUME,
                    "type": mt5.ORDER_TYPE_BUY,
                    "price": preco_atual,
                    "sl": stop_loss,
                    "tp": take_profit,
                    "comment": "Compra AI",
                }
            )
            mensagem = f"✅ COMPRA realizada para {par}!\n💰 Preço: {preco_atual}\n📉 SL: {stop_loss}\n📈 TP: {take_profit}"
            enviar_mensagem(mensagem)
        
        elif previsao < preco_atual:
            ordem = mt5.OrderSend(
                {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": par,
                    "volume": VOLUME,
                    "type": mt5.ORDER_TYPE_SELL,
                    "price": preco_atual,
                    "sl": stop_loss,
                    "tp": take_profit,
                    "comment": "Venda AI",
                }
            )
            mensagem = f"❌ VENDA realizada para {par}!\n💰 Preço: {preco_atual}\n📉 SL: {stop_loss}\n📈 TP: {take_profit}"
            enviar_mensagem(mensagem)


# Loop para operar a cada 10 minutos 
while True:
    operar()
    time.sleep(600)
