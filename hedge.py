import yfinance as yf

# 1️⃣ Definir Pares de Hedge
PARES = [("EURUSD=X", "USDJPY=X"), ("GBPUSD=X", "AUDUSD=X")]

# 2️⃣ Coletar Dados dos Pares de Hedge
def obter_precos():
    precos = {}
    for par1, par2 in PARES:
        df1 = yf.download(par1, period="1mo", interval="1h")["Close"].iloc[-1]
        df2 = yf.download(par2, period="1mo", interval="1h")["Close"].iloc[-1]
        precos[par1] = df1
        precos[par2] = df2
    return precos

# 3️⃣ Criar Estratégia de Hedge
def estrategia_hedge():
    precos = obter_precos()
    
    for par1, par2 in PARES:
        if precos[par1] < precos[par2]:
            print(f"⚠️ Mercado em baixa! Comprando {par2} para hedge.")
        else:
            print(f"📈 Mercado estável! Mantendo posição.")

# Testar o Hedge
estrategia_hedge()
