import pandas as pd
import os
from datetime import datetime

# Nome do arquivo de logs
LOG_FILE = "logs_operacoes.csv"

# Criar o arquivo se não existir
if not os.path.exists(LOG_FILE):
    df = pd.DataFrame(columns=["Data", "Par", "Tipo", "Preço Entrada", "Preço Saída", "Lucro/Prejuízo"])
    df.to_csv(LOG_FILE, index=False)

def registrar_operacao(par, tipo, preco_entrada, preco_saida, lucro_prejuizo):
    """ Registra uma operação no arquivo CSV """
    df = pd.read_csv(LOG_FILE)
    nova_operacao = pd.DataFrame({
        "Data": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Par": [par],
        "Tipo": [tipo],
        "Preço Entrada": [preco_entrada],
        "Preço Saída": [preco_saida],
        "Lucro/Prejuízo": [lucro_prejuizo]
    })
    df = pd.concat([df, nova_operacao], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)
    print(f"📜 Operação registrada: {tipo} {par} - Entrada: {preco_entrada}, Saída: {preco_saida}, Resultado: {lucro_prejuizo}")
