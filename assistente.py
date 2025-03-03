import openai
import speech_recognition as sr
import pyttsx3

# Configuração da chave de API do OpenAI
openai.api_key = "SUA-CHAVE-OPENAI"

# Configuração do motor de voz
voz = pyttsx3.init()

def falar(texto):
    """ Faz o assistente falar """
    voz.say(texto)
    voz.runAndWait()

def ouvir():
    """ Captura o áudio do microfone e converte para texto """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Ouvindo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        comando = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {comando}")
        return comando.lower()
    except sr.UnknownValueError:
        return "Não entendi o que você disse."
    except sr.RequestError:
        return "Erro ao conectar com o serviço de voz."

def responder(comando):
    """ Envia o comando para a IA e recebe uma resposta """
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": comando}]
    )
    return resposta["choices"][0]["message"]["content"]

# Loop principal do assistente
while True:
    comando_usuario = ouvir()
    resposta_ia = responder(comando_usuario)
    falar(resposta_ia)
