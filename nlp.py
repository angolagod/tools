import openai
import speech_recognition as sr
import pyttsx3

# Configuração do motor de voz
engine = pyttsx3.init()

# Configuração da API OpenAI
openai.api_key = "SUA-CHAVE-OPENAI"

def falar(texto):
    engine.say(texto)
    engine.runAndWait()

def ouvir_comando():
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
        print("Não entendi o comando.")
        return ""
    except sr.RequestError:
        print("Erro ao conectar com o serviço de reconhecimento.")
        return ""

def processar_comando(comando):
    if "abrir navegador" in comando:
        falar("Abrindo o navegador...")
        import webbrowser
        webbrowser.open("https://www.google.com")
    elif "fechar" in comando:
        falar("Encerrando assistente. Até logo!")
        exit()
    else:
        # Enviar para o ChatGPT para resposta inteligente
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": comando}]
        )
        falar(resposta["choices"][0]["message"]["content"])

# Loop Principal do Assistente
while True:
    comando_usuario = ouvir_comando()
    processar_comando(comando_usuario)
