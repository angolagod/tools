import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

# 1️⃣ Coletar dados Forex
def coletar_dados(par="EURUSD=X"):
    df = yf.download(par, period="1mo", interval="1h")
    df = df.reset_index()
    return df

# 2️⃣ Criar o Dashboard
app = dash.Dash(__name__)
dados = coletar_dados()

fig = go.Figure()
fig.add_trace(go.Scatter(x=dados["Datetime"], y=dados["Close"], mode="lines", name="Preço de Fechamento"))

app.layout = html.Div([
    html.H1("📊 Painel de Controle - Bot Forex"),
    dcc.Graph(figure=fig)
])

# 3️⃣ Rodar o Servidor Web
if __name__ == "__main__":
    app.run_server(debug=True)
