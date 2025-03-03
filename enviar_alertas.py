import requests

TOKEN = "7819937972:AAHKCvjGBe9uYKChMcCHsl52G65qR1drlLA"
CHAT_ID = "7808325891"

def enviar_mensagem(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": mensagem}
    requests.get(url, params=params)

# Teste de envio
enviar_mensagem("🚀 O Bot Forex está ativo!")
