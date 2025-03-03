from flask import Flask, render_template, jsonify
import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

# Criar aplicação Flask
app = Flask(__name__)

# Criar o Dashboard com Dash
dash_app = dash.Dash(__name__, server=app, routes_pathname_prefix='/dashboard/')

# 1️⃣ Coletar dados Forex
def coletar_dados(par="EURUSD=X"):
    df = yf.download(par, period="1mo", interval="1h")
    df = df.reset_index()
    return df

# 2️⃣ Criar o Gráfico
dados = coletar_dados()
fig = go.Figure()
fig.add_trace(go.Scatter(x=dados["Datetime"], y=dados["Close"], mode="lines", name="Preço de Fechamento"))

dash_app.layout = html.Div([
    html.H1("📊 Dashboard do Bot Forex"),
    dcc.Graph(figure=fig)
])

# 3️⃣ Criar a Página Web com Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    return jsonify({"status": "Bot rodando", "pares_monitorados": ["EURUSD", "GBPUSD", "USDJPY"]})

if __name__ == "__main__":
    app.run(debug=True)
