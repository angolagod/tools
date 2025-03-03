import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# 1️⃣ Carregar os logs das operações
LOG_FILE = "logs_operacoes.csv"

def carregar_dados():
    try:
        df = pd.read_csv(LOG_FILE)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Data", "Par", "Tipo", "Preço Entrada", "Preço Saída", "Lucro/Prejuízo"])

# 2️⃣ Criar o Dashboard
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📊 Relatórios do Bot Forex"),
    
    # Gráfico de Lucro por Operação
    dcc.Graph(id="grafico-lucro"),
    
    # Tabela das operações
    html.H3("📜 Histórico de Operações"),
    html.Div(id="tabela-operacoes"),
])

@app.callback(
    dash.dependencies.Output("grafico-lucro", "figure"),
    dash.dependencies.Output("tabela-operacoes", "children"),
    dash.dependencies.Input("grafico-lucro", "id")
)
def atualizar_dashboard(_):
    df = carregar_dados()

    # Criar gráfico de lucros
    fig = px.bar(df, x="Data", y="Lucro/Prejuízo", color="Par", title="Lucro por Operação")

    # Criar tabela HTML
    tabela = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df.columns])),
        html.Tbody([
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(len(df))
        ])
    ])

    return fig, tabela

# 3️⃣ Rodar o servidor do Dashboard
if __name__ == "__main__":
    app.run_server(debug=True)
