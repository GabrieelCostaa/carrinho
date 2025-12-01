"""
Arquivo de configuração para ajuste fino do sistema
"""

# Configuração da câmera
# Exemplos de URLs para apps de câmera IP:
# - IP Webcam (Android): "http://192.168.1.100:8080/video"
# - DroidCam: "http://192.168.1.100:4747/video"
# - iVCam: usar cliente específico
CAMERA_URL = None  # None para usar webcam do PC

# Configuração do ESP32
ESP32_IP = "192.168.1.100"  # Altere para o IP do seu ESP32
ESP32_PORT = 8765

# Parâmetros de processamento de imagem
ROI_HEIGHT = 0.3  # Altura da região de interesse (0.1 a 0.5)
BLUR_KERNEL_SIZE = 5  # Tamanho do kernel de blur (ímpar)

# Limites HSV para detecção de linha preta
# Formato: [H, S, V]
LOWER_BLACK = [0, 0, 0]
UPPER_BLACK = [180, 255, 50]

# Limites HSV para linha branca (alternativa)
LOWER_WHITE = [0, 0, 200]
UPPER_WHITE = [180, 30, 255]

# Parâmetros de controle do carrinho
BASE_SPEED = 45  # Velocidade base (0-100)
TURN_SPEED = 55  # Velocidade nas curvas
SHARP_TURN_THRESHOLD = 150  # Pixels de desvio para curva brusca

# Parâmetros de processamento
MIN_CONTOUR_AREA = 100  # Área mínima do contorno para ser considerado
COMMAND_INTERVAL = 0.05  # Intervalo entre comandos (segundos)

# Modo debug
DEBUG_MODE = False  # True para mostrar visualizações extras

