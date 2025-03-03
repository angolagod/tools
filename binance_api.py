import ccxt

# 1️⃣ Configuração da API Binance
binance = ccxt.binance({
    'apiKey': 'SUA_API_KEY',
    'secret': 'SUA_API_SECRET',
    'enableRateLimit': True
})

# 2️⃣ Obter Preço Atual de um Par
def obter_preco_binance(par="BTC/USDT"):
    preco = binance.fetch_ticker(par)['last']
    return preco

# 3️⃣ Criar Ordem de Compra/Venda
def comprar_binance(par="BTC/USDT", quantidade=0.001):
    order = binance.create_market_buy_order(par, quantidade)
    return order

def vender_binance(par="BTC/USDT", quantidade=0.001):
    order = binance.create_market_sell_order(par, quantidade)
    return order

# Teste
print(f"Preço Atual BTC/USDT: {obter_preco_binance()}")
