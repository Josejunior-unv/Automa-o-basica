import pyautogui

# Obtém as coordenadas atuais do cursor
pyautogui.sleep(2)  # Aguarda 2 segundos para o usuário posicionar o cursor
x, y = pyautogui.position()
print(f"Coordenadas: X={x}, Y={y}")
