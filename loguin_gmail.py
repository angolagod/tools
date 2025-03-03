from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def login_gmail(usuario, senha):
    """Faz login no Gmail automaticamente"""

    # Configurar o WebDriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # Mantém o navegador aberto
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Abrir a página de login do Gmail
    driver.get("https://www.google.com/")
    time.sleep(3)

    # Inserir o email
    email_input = driver.find_element(By.ID, "identifierId")
    email_input.send_keys(usuario)
    email_input.send_keys(Keys.RETURN)
    time.sleep(3)

    # Inserir senha
    senha_input = driver.find_element(By.NAME, "password")
    senha_input.send_keys(senha)
    senha_input.send_keys(Keys.RETURN)
    time.sleep(5)  # Tempo para carregar a página

    print("✅ Login realizado com sucesso!")
    return driver

# Exemplo de uso:
login_gmail("arthurcavilhas@gmail.com", "1016Ru@n")
