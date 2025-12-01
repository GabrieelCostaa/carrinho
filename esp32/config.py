"""
Arquivo de configuração para o ESP32
Edite os valores conforme seu hardware
"""

# Configurações WiFi
WIFI_SSID = "PUC-ACD"
WIFI_PASSWORD = ""  # Rede sem senha (aberta)

# Configurações do servidor WebSocket
WEBSOCKET_PORT = 8765

# Configuração dos pinos do motor (L298N ou similar)
# Motor Esquerdo
MOTOR_LEFT_PIN1 = 25
MOTOR_LEFT_PIN2 = 26
MOTOR_LEFT_PWM = 27

# Motor Direito
MOTOR_RIGHT_PIN1 = 32
MOTOR_RIGHT_PIN2 = 33
MOTOR_RIGHT_PWM = 14

# Frequência PWM (Hz)
PWM_FREQUENCY = 1000

# Velocidade padrão (0-100)
DEFAULT_SPEED = 50

