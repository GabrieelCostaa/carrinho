"""
Carrinho Seguidor de Linha - ESP32 MicroPython
Recebe comandos via WebSocket e controla os motores
"""

import network
import socket
import time
from machine import Pin, PWM
import json
import struct

# Configuração dos pinos do motor (ajuste conforme seu hardware)
# Motor Esquerdo
MOTOR_LEFT_PIN1 = 25
MOTOR_LEFT_PIN2 = 26
MOTOR_LEFT_PWM = 27

# Motor Direito
MOTOR_RIGHT_PIN1 = 32
MOTOR_RIGHT_PIN2 = 33
MOTOR_RIGHT_PWM = 14

# Configuração WiFi
SSID = "SEU_WIFI"  # Altere para seu WiFi
PASSWORD = "SUA_SENHA"  # Altere para sua senha
PORT = 8765

class MotorControl:
    """Classe para controlar os motores do carrinho"""
    
    def __init__(self):
        # Configurar pinos dos motores
        self.left_pin1 = Pin(MOTOR_LEFT_PIN1, Pin.OUT)
        self.left_pin2 = Pin(MOTOR_LEFT_PIN2, Pin.OUT)
        self.left_pwm = PWM(Pin(MOTOR_LEFT_PWM), freq=1000)
        
        self.right_pin1 = Pin(MOTOR_RIGHT_PIN1, Pin.OUT)
        self.right_pin2 = Pin(MOTOR_RIGHT_PIN2, Pin.OUT)
        self.right_pwm = PWM(Pin(MOTOR_RIGHT_PWM), freq=1000)
        
        self.stop()
    
    def set_motor(self, left_speed, right_speed):
        """
        Define a velocidade dos motores
        left_speed: -100 a 100 (negativo = ré)
        right_speed: -100 a 100 (negativo = ré)
        """
        # Motor Esquerdo
        if left_speed > 0:
            self.left_pin1.value(1)
            self.left_pin2.value(0)
            self.left_pwm.duty(int(abs(left_speed) * 10.23))  # 0-1023
        elif left_speed < 0:
            self.left_pin1.value(0)
            self.left_pin2.value(1)
            self.left_pwm.duty(int(abs(left_speed) * 10.23))
        else:
            self.left_pin1.value(0)
            self.left_pin2.value(0)
            self.left_pwm.duty(0)
        
        # Motor Direito
        if right_speed > 0:
            self.right_pin1.value(1)
            self.right_pin2.value(0)
            self.right_pwm.duty(int(abs(right_speed) * 10.23))
        elif right_speed < 0:
            self.right_pin1.value(0)
            self.right_pin2.value(1)
            self.right_pwm.duty(int(abs(right_speed) * 10.23))
        else:
            self.right_pin1.value(0)
            self.right_pin2.value(0)
            self.right_pwm.duty(0)
    
    def forward(self, speed=50):
        """Move para frente"""
        self.set_motor(speed, speed)
    
    def backward(self, speed=50):
        """Move para trás"""
        self.set_motor(-speed, -speed)
    
    def turn_left(self, speed=50):
        """Vira à esquerda"""
        self.set_motor(speed // 2, speed)
    
    def turn_right(self, speed=50):
        """Vira à direita"""
        self.set_motor(speed, speed // 2)
    
    def sharp_left(self, speed=50):
        """Vira bruscamente à esquerda (uma roda para frente, outra para trás)"""
        self.set_motor(-speed // 2, speed)
    
    def sharp_right(self, speed=50):
        """Vira bruscamente à direita"""
        self.set_motor(speed, -speed // 2)
    
    def stop(self):
        """Para o carrinho"""
        self.set_motor(0, 0)

def connect_wifi():
    """Conecta ao WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Conectando ao WiFi...')
        wlan.connect(SSID, PASSWORD)
        
        # Aguarda conexão
        timeout = 30
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            print('.', end='')
        
        if not wlan.isconnected():
            print('\nFalha ao conectar ao WiFi')
            return None
    
    print('\nConectado ao WiFi!')
    print('IP:', wlan.ifconfig()[0])
    return wlan.ifconfig()[0]

def parse_websocket_frame(data):
    """Parse simples de frame WebSocket"""
    if len(data) < 2:
        return None
    
    # Ignora frames de controle
    opcode = data[0] & 0x0F
    if opcode == 0x08:  # Close frame
        return None
    if opcode == 0x09:  # Ping frame
        return 'PING'
    
    # Verifica se tem máscara
    masked = data[1] & 0x80
    payload_length = data[1] & 0x7F
    
    if payload_length == 126:
        mask_start = 4
    elif payload_length == 127:
        mask_start = 10
    else:
        mask_start = 2
    
    if masked:
        mask_key = data[mask_start:mask_start + 4]
        payload_start = mask_start + 4
        payload = bytearray(data[payload_start:payload_start + payload_length])
        
        # Desmascara os dados
        for i in range(len(payload)):
            payload[i] ^= mask_key[i % 4]
        
        return payload.decode('utf-8')
    else:
        return data[mask_start:].decode('utf-8')

def create_websocket_frame(message):
    """Cria um frame WebSocket simples"""
    payload = message.encode('utf-8')
    frame = bytearray()
    frame.append(0x81)  # Text frame, FIN bit set
    
    length = len(payload)
    if length < 126:
        frame.append(length)
    elif length < 65536:
        frame.append(126)
        frame.extend(struct.pack('>H', length))
    else:
        frame.append(127)
        frame.extend(struct.pack('>Q', length))
    
    frame.extend(payload)
    return bytes(frame)

def handle_command(command_str, motor_control):
    """Processa comando recebido"""
    try:
        command = json.loads(command_str)
        action = command.get('action', 'stop')
        speed = command.get('speed', 50)
        
        print(f'Comando recebido: {action} (velocidade: {speed})')
        
        if action == 'forward':
            motor_control.forward(speed)
        elif action == 'backward':
            motor_control.backward(speed)
        elif action == 'left':
            motor_control.turn_left(speed)
        elif action == 'right':
            motor_control.turn_right(speed)
        elif action == 'sharp_left':
            motor_control.sharp_left(speed)
        elif action == 'sharp_right':
            motor_control.sharp_right(speed)
        elif action == 'stop':
            motor_control.stop()
        elif action == 'custom':
            # Permite controle customizado dos motores
            left = command.get('left', 0)
            right = command.get('right', 0)
            motor_control.set_motor(left, right)
        
        return True
    except Exception as e:
        print('Erro ao processar comando:', e)
        return False

def start_websocket_server():
    """Inicia o servidor WebSocket"""
    motor_control = MotorControl()
    
    # Conecta ao WiFi
    ip = connect_wifi()
    if not ip:
        print('Não foi possível iniciar o servidor sem WiFi')
        return
    
    # Cria socket
    addr = socket.getaddrinfo('0.0.0.0', PORT)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    
    print(f'Servidor WebSocket aguardando conexões em ws://{ip}:{PORT}')
    
    while True:
        try:
            client, addr = s.accept()
            print('Cliente conectado:', addr)
            client.settimeout(0.1)
            
            # Handshake WebSocket
            request = client.recv(1024).decode('utf-8')
            if 'Upgrade: websocket' in request:
                # Extrai a chave do WebSocket
                for line in request.split('\r\n'):
                    if line.startswith('Sec-WebSocket-Key:'):
                        key = line.split(': ')[1]
                        break
                
                # Resposta do handshake
                import hashlib
                import binascii
                magic = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
                accept_key = hashlib.sha1((key + magic).encode()).digest()
                accept_key = binascii.b2a_base64(accept_key).strip().decode()
                
                response = (
                    'HTTP/1.1 101 Switching Protocols\r\n'
                    'Upgrade: websocket\r\n'
                    'Connection: Upgrade\r\n'
                    f'Sec-WebSocket-Accept: {accept_key}\r\n'
                    '\r\n'
                )
                client.send(response.encode())
                print('WebSocket handshake completo')
                
                # Loop de mensagens
                while True:
                    try:
                        data = client.recv(1024)
                        if not data:
                            break
                        
                        message = parse_websocket_frame(data)
                        if message == 'PING':
                            # Responde com PONG
                            pong_frame = bytearray([0x8A, 0x00])
                            client.send(bytes(pong_frame))
                        elif message:
                            handle_command(message, motor_control)
                            # Envia confirmação
                            response = create_websocket_frame('{"status": "ok"}')
                            client.send(response)
                    
                    except OSError:
                        # Timeout - continua aguardando
                        time.sleep(0.01)
                    except Exception as e:
                        print('Erro:', e)
                        break
            
            motor_control.stop()
            client.close()
            print('Cliente desconectado')
        
        except Exception as e:
            print('Erro no servidor:', e)
            motor_control.stop()
            time.sleep(1)

# Inicia o servidor
if __name__ == '__main__':
    print('=== Carrinho Seguidor de Linha ===')
    print('Iniciando servidor WebSocket...')
    start_websocket_server()

