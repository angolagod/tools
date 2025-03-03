import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

dados = pd.DataFrame({
    "Produto": ["Notebook", "Smartphone", "Headset"],
    "Preço": [3500, 2500, 600]
})

fig = px.bar(dados, x="Produto", y="Preço", title="Comparação de Preços")

app.layout = html.Div([
    html.H1("Dashboard de Preços"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run_server(debug=True)
