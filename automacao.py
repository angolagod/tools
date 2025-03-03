import os
import pyautogui
import time

def abrir_programa(programa):
    os.system(f"start {programa}")

def fechar_janela():
    pyautogui.hotkey("alt", "f4")

def ajustar_volume(nivel):
    """ Define o volume do sistema (0 a 100) """
    os.system(f"nircmd.exe setsysvolume {nivel * 65535 // 100}")

def desligar_pc():
    """ Desliga o computador """
    os.system("shutdown /s /t 10")

# Teste: Abrir o Google Chrome
abrir_programa("chrome.exe")
time.sleep(5)
fechar_janela()
