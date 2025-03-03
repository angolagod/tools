import MetaTrader5 as mt5

# Conectar ao MetaTrader5
if not mt5.initialize():
    print("Erro ao conectar ao MetaTrader5")
    mt5.shutdown()

# Obter preço atual do EUR/USD
info = mt5.symbol_info_tick("EURUSD")
print(f"Preço EUR/USD: {info.ask}")

# Fechar conexão
mt5.shutdown()
