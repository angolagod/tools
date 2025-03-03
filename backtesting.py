import backtrader as bt
import yfinance as yf

# 1️⃣ Criar Estratégia de Backtesting
class EstrategiaSimples(bt.Strategy):
    params = (("sma_period", 20),)

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_period)

    def next(self):
        if self.data.close[0] > self.sma[0]:  # Compra quando o preço está acima da média
            self.buy()
        elif self.data.close[0] < self.sma[0]:  # Vende quando o preço está abaixo da média
            self.sell()

# 2️⃣ Baixar Dados Forex
def baixar_dados(par="EURUSD=X"):
    df = yf.download(par, period="6mo", interval="1h")
    return df

# 3️⃣ Rodar Backtest
def rodar_backtest():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(EstrategiaSimples)

    df = baixar_dados()
    data = bt.feeds.PandasData(dataname=df)

    cerebro.adddata(data)
    cerebro.broker.set_cash(10000)
    cerebro.broker.setcommission(commission=0.0001)
    cerebro.run()

    print(f"Saldo Final: ${cerebro.broker.getvalue():.2f}")
    cerebro.plot()

rodar_backtest()
