import backtrader as bt
import yfinance as yf
from deap import base, creator, tools, algorithms
import random

# 1️⃣ Criar Estratégia de Trading
class EstrategiaOtimizada(bt.Strategy):
    params = (("sma_period", 20), ("stop_loss", 0.01), ("take_profit", 0.02))

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_period)

    def next(self):
        if self.data.close[0] > self.sma[0]:  
            self.buy()
        elif self.data.close[0] < self.sma[0]:  
            self.sell()

# 2️⃣ Baixar Dados Forex
def baixar_dados(par="EURUSD=X"):
    df = yf.download(par, period="6mo", interval="1h")
    return df

# 3️⃣ Criar Função de Avaliação
def avaliar(individual):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(EstrategiaOtimizada, sma_period=int(individual[0]), stop_loss=individual[1], take_profit=individual[2])
    
    df = baixar_dados()
    data = bt.feeds.PandasData(dataname=df)
    
    cerebro.adddata(data)
    cerebro.broker.set_cash(10000)
    cerebro.run()
    
    return (cerebro.broker.getvalue(),)

# 4️⃣ Implementar Algoritmo Genético
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individuo", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_int", random.randint, 5, 50)
toolbox.register("attr_float", random.uniform, 0.005, 0.05)
toolbox.register("individual", tools.initCycle, creator.Individuo, (toolbox.attr_int, toolbox.attr_float, toolbox.attr_float), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", avaliar)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selBest)

# 5️⃣ Executar Otimização
def otimizar():
    pop = toolbox.population(n=10)
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=10, verbose=True)
    melhor_individuo = tools.selBest(pop, k=1)[0]
    print(f"🔍 Melhor Estratégia: SMA {melhor_individuo[0]}, Stop-Loss {melhor_individuo[1]}, Take-Profit {melhor_individuo[2]}")

otimizar()
