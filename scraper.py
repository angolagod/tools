import requests
from bs4 import BeautifulSoup

def coletar_preco_amazon(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        titulo = soup.find("span", {"id": "productTitle"}).get_text().strip()
        preco = soup.find("span", {"class": "a-offscreen"}).get_text().strip()
        return f"Produto: {titulo}, Preço: {preco}"
    except AttributeError:
        return "Não foi possível encontrar o preço."

# Exemplo: Buscando um produto na Amazon
print(coletar_preco_amazon("https://www.amazon.com.br/dp/B09G9FPHYB"))
