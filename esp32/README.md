# ESP32 - Código MicroPython

## 📋 Arquivos

- `main.py`: Servidor WebSocket e controle dos motores
- `config.py`: Configurações (WiFi, pinos dos motores)

## 🔧 Configuração dos Pinos

Edite `config.py` conforme seu hardware:

### Exemplo para L298N:
```python
# Motor Esquerdo
MOTOR_LEFT_PIN1 = 25    # IN1
MOTOR_LEFT_PIN2 = 26    # IN2
MOTOR_LEFT_PWM = 27     # ENA

# Motor Direito
MOTOR_RIGHT_PIN1 = 32   # IN3
MOTOR_RIGHT_PIN2 = 33   # IN4
MOTOR_RIGHT_PWM = 14    # ENB
```

### Conexões L298N:
```
ESP32         L298N
-------------------------
GPIO 25   →   IN1
GPIO 26   →   IN2
GPIO 27   →   ENA (PWM)
GPIO 32   →   IN3
GPIO 33   →   IN4
GPIO 14   →   ENB (PWM)
GND       →   GND
```

## 📤 Upload para ESP32

### Método 1: Usando ampy
```bash
pip install adafruit-ampy

# Upload
ampy --port /dev/ttyUSB0 put config.py
ampy --port /dev/ttyUSB0 put main.py

# Verificar
ampy --port /dev/ttyUSB0 ls
```

### Método 2: Usando Thonny
1. Abra Thonny IDE
2. Configure interpretador para MicroPython (ESP32)
3. Abra os arquivos e clique em "Save" → "MicroPython device"

### Método 3: Usando rshell
```bash
pip install rshell

rshell -p /dev/ttyUSB0
> cp config.py /pyboard/
> cp main.py /pyboard/
```

## 🔌 Instalar MicroPython

### 1. Baixar Firmware
```
https://micropython.org/download/esp32/
```

### 2. Instalar esptool
```bash
pip install esptool
```

### 3. Apagar Flash
```bash
esptool.py --port /dev/ttyUSB0 erase_flash
```

### 4. Gravar Firmware
```bash
esptool.py --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-xxxxx.bin
```

## 🔍 Debug

### Ver saída serial:
```bash
# Linux/Mac
screen /dev/ttyUSB0 115200

# Windows
putty -serial COM3 -seriospeed 115200

# Ou use Thonny IDE
```

### Testar WiFi:
```python
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('SSID', 'PASSWORD')
print(wlan.ifconfig())
```

### Testar Motores:
```python
from machine import Pin, PWM

# Motor teste
pin1 = Pin(25, Pin.OUT)
pin2 = Pin(26, Pin.OUT)
pwm = PWM(Pin(27), freq=1000)

pin1.value(1)
pin2.value(0)
pwm.duty(512)  # 50% velocidade
```

## 🌐 Protocolo WebSocket

### Comandos Aceitos:
```json
{"action": "forward", "speed": 50}
{"action": "backward", "speed": 50}
{"action": "left", "speed": 50}
{"action": "right", "speed": 50}
{"action": "stop"}
{"action": "custom", "left": 70, "right": 30}
```

### Resposta:
```json
{"status": "ok"}
```

## ⚡ Dicas

- Use cabo USB de qualidade (dados, não apenas carga)
- Mantenha ESP32 próximo ao roteador durante testes
- Anote o IP mostrado no boot
- Verifique alimentação adequada dos motores
- Use diodos flyback nos motores para proteção

## 🐛 Troubleshooting

### ESP32 não conecta ao WiFi
- Verifique SSID e senha
- Reinicie o roteador
- Teste WiFi com outro dispositivo

### Motores não giram
- Verifique alimentação (motores precisam fonte separada)
- Teste pinos individualmente
- Verifique conexões soltas

### WebSocket não conecta
- Verifique firewall do PC
- Teste ping para o IP do ESP32
- Reinicie o ESP32

