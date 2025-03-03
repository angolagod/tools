import pandas as pd
import yfinance as yf
import random

# 1️⃣ Definir Parâmetros do Simulador
CAPITAL_INICIAL = 10000
PARES = ["EURUSD=X", "GBPUSD=X", "USDJPY=X"]

# 2️⃣ Simular operações usando dados históricos
def simular_trading():
    capital = CAPITAL_INICIAL
    historico = []

    for par in PARES:
        df = yf.download(par, period="3mo", interval="1h")
        
        for i in range(len(df) - 1):
            preco_entrada = df["Close"].iloc[i]
            preco_saida = df["Close"].iloc[i + 1]

            # Simular decisão de compra/venda aleatória
            if random.choice([True, False]):
                capital -= preco_entrada
                lucro = preco_saida - preco_entrada
                capital += preco_saida
                historico.append([par, "COMPRA", preco_entrada, preco_saida, lucro])
            else:
                historico.append([par, "AGUARDAR", preco_entrada, None, 0])

    return pd.DataFrame(historico, columns=["Par", "Tipo", "Preço Entrada", "Preço Saída", "Lucro"])

# 3️⃣ Rodar a simulação
df_simulado = simular_trading()
print(df_simulado)

# Salvar resultados
df_simulado.to_csv("simulacao_trading.csv", index=False)
print(f"📊 Simulação concluída! Resultado final: ${capital:.2f}")
