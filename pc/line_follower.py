"""
Sistema de Seguidor de Linha usando Visão Computacional
Conecta-se a um celular como webcam e envia comandos via WebSocket para o ESP32
"""

import cv2
import numpy as np
import asyncio
import websockets
import json
import argparse
from urllib.parse import urlparse

class LineFollower:
    """Classe principal para detecção e seguimento de linha"""
    
    def __init__(self, esp32_ip, camera_url=None, debug=False):
        self.esp32_ip = esp32_ip
        self.camera_url = camera_url
        self.debug = debug
        self.websocket = None
        self.running = False
        
        # Parâmetros de processamento de imagem
        self.roi_height = 0.3  # Região de interesse (30% inferior da imagem)
        self.blur_kernel = (5, 5)
        
        # Limites HSV para linha preta (ajuste conforme necessário)
        self.lower_black = np.array([0, 0, 0])
        self.upper_black = np.array([180, 255, 50])
        
        # Parâmetros de controle
        self.base_speed = 45
        self.turn_speed = 55
        self.sharp_turn_threshold = 150  # pixels de desvio para curva brusca
        
        # Estatísticas
        self.frame_count = 0
        self.detection_count = 0
        
    async def connect_websocket(self):
        """Conecta ao servidor WebSocket do ESP32"""
        uri = f"ws://{self.esp32_ip}:8765"
        try:
            self.websocket = await websockets.connect(uri)
            print(f"✓ Conectado ao ESP32 em {uri}")
            return True
        except Exception as e:
            print(f"✗ Erro ao conectar ao ESP32: {e}")
            return False
    
    async def send_command(self, action, speed=None, left=None, right=None):
        """Envia comando para o carrinho via WebSocket"""
        if not self.websocket:
            return False
        
        try:
            command = {"action": action}
            
            if speed is not None:
                command["speed"] = speed
            
            if left is not None and right is not None:
                command["action"] = "custom"
                command["left"] = left
                command["right"] = right
            
            await self.websocket.send(json.dumps(command))
            
            # Aguarda confirmação
            response = await asyncio.wait_for(self.websocket.recv(), timeout=0.5)
            return True
        
        except asyncio.TimeoutError:
            print("⚠ Timeout ao aguardar resposta do ESP32")
            return False
        except Exception as e:
            print(f"✗ Erro ao enviar comando: {e}")
            return False
    
    def process_frame(self, frame):
        """
        Processa um frame para detectar a linha
        Retorna: (frame processado, centro da linha, ângulo de desvio)
        """
        height, width = frame.shape[:2]
        
        # Define região de interesse (ROI) - parte inferior da imagem
        roi_y = int(height * (1 - self.roi_height))
        roi = frame[roi_y:height, 0:width]
        
        # Converte para HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Aplica blur para reduzir ruído
        blurred = cv2.GaussianBlur(hsv, self.blur_kernel, 0)
        
        # Cria máscara para detectar linha preta
        mask = cv2.inRange(blurred, self.lower_black, self.upper_black)
        
        # Operações morfológicas para limpar a máscara
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)
        
        # Encontra contornos
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        line_center = None
        deviation = 0
        
        if contours:
            # Pega o maior contorno (assume que é a linha)
            largest_contour = max(contours, key=cv2.contourArea)
            
            if cv2.contourArea(largest_contour) > 100:  # Filtra contornos muito pequenos
                # Calcula o centro do contorno
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    
                    # Ajusta coordenadas para o frame completo
                    line_center = (cx, cy + roi_y)
                    
                    # Calcula desvio do centro
                    frame_center = width // 2
                    deviation = cx - (width // 2)
                    
                    # Desenha informações no frame (se debug)
                    if self.debug:
                        # Desenha contorno
                        cv2.drawContours(roi, [largest_contour], -1, (0, 255, 0), 2)
                        
                        # Desenha centro da linha
                        cv2.circle(roi, (cx, cy), 5, (0, 0, 255), -1)
                        
                        # Desenha linha central do frame
                        cv2.line(roi, (width // 2, 0), (width // 2, roi.shape[0]), (255, 0, 0), 2)
                        
                        # Adiciona texto com informações
                        cv2.putText(roi, f"Desvio: {deviation}px", (10, 30),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Monta frame de debug
        if self.debug:
            # Cria visualização com frame original, ROI e máscara
            debug_frame = frame.copy()
            
            # Desenha retângulo da ROI
            cv2.rectangle(debug_frame, (0, roi_y), (width, height), (0, 255, 0), 2)
            
            # Desenha centro da linha no frame completo
            if line_center:
                cv2.circle(debug_frame, line_center, 8, (0, 0, 255), -1)
                cv2.line(debug_frame, (width // 2, 0), (width // 2, height), (255, 0, 0), 2)
            
            # Converte máscara para BGR para concatenar
            mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            
            # Redimensiona para visualização lado a lado
            combined = np.hstack([debug_frame, cv2.resize(mask_bgr, (width, height))])
            
            return combined, line_center, deviation
        
        return frame, line_center, deviation
    
    def calculate_motor_speeds(self, deviation):
        """
        Calcula velocidades dos motores baseado no desvio da linha
        Retorna: (velocidade_esquerda, velocidade_direita)
        """
        if deviation == 0:
            # Linha no centro - segue em frente
            return self.base_speed, self.base_speed
        
        # Normaliza o desvio (-1 a 1)
        # Assume largura de frame de ~640px, ajuste se necessário
        normalized_deviation = max(-1, min(1, deviation / 320))
        
        if abs(deviation) > self.sharp_turn_threshold:
            # Curva brusca - reduz velocidade de um motor ou inverte
            if deviation > 0:
                # Linha à direita - vira para direita
                left_speed = self.turn_speed
                right_speed = -int(self.turn_speed * 0.3)
            else:
                # Linha à esquerda - vira para esquerda
                left_speed = -int(self.turn_speed * 0.3)
                right_speed = self.turn_speed
        else:
            # Curva suave - ajusta proporcionalmente
            if deviation > 0:
                # Linha à direita
                left_speed = self.base_speed
                right_speed = int(self.base_speed * (1 - abs(normalized_deviation) * 0.8))
            else:
                # Linha à esquerda
                left_speed = int(self.base_speed * (1 - abs(normalized_deviation) * 0.8))
                right_speed = self.base_speed
        
        return left_speed, right_speed
    
    async def follow_line(self):
        """Loop principal de seguimento de linha"""
        # Conecta ao WebSocket
        if not await self.connect_websocket():
            return
        
        # Abre conexão com câmera
        if self.camera_url:
            cap = cv2.VideoCapture(self.camera_url)
        else:
            # Usa câmera padrão do PC
            cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Erro ao abrir câmera")
            return
        
        print("✓ Câmera conectada")
        print("\nControles:")
        print("  ESC ou Q - Sair")
        print("  ESPAÇO - Pausar/Retomar")
        print("  R - Resetar estatísticas")
        print("  + - Aumentar velocidade base")
        print("  - - Diminuir velocidade base")
        
        self.running = True
        paused = False
        last_command_time = 0
        command_interval = 0.05  # Envia comandos a cada 50ms
        
        try:
            while self.running:
                ret, frame = cap.read()
                if not ret:
                    print("✗ Erro ao capturar frame")
                    break
                
                self.frame_count += 1
                
                # Processa frame
                processed_frame, line_center, deviation = self.process_frame(frame)
                
                # Envia comando se não estiver pausado
                if not paused and line_center:
                    self.detection_count += 1
                    
                    # Controla taxa de envio de comandos
                    import time
                    current_time = time.time()
                    if current_time - last_command_time >= command_interval:
                        left_speed, right_speed = self.calculate_motor_speeds(deviation)
                        await self.send_command("custom", left=left_speed, right=right_speed)
                        last_command_time = current_time
                
                elif not paused and not line_center:
                    # Linha não detectada - para
                    await self.send_command("stop")
                
                # Adiciona informações na tela
                info_frame = processed_frame.copy()
                status_text = "PAUSADO" if paused else "ATIVO"
                status_color = (0, 165, 255) if paused else (0, 255, 0)
                
                cv2.putText(info_frame, status_text, (10, 30),
                          cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
                
                cv2.putText(info_frame, f"Frames: {self.frame_count}", (10, 60),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                cv2.putText(info_frame, f"Deteccoes: {self.detection_count}", (10, 85),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                cv2.putText(info_frame, f"Velocidade: {self.base_speed}", (10, 110),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                if line_center:
                    cv2.putText(info_frame, "Linha: DETECTADA", (10, 135),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                else:
                    cv2.putText(info_frame, "Linha: NAO DETECTADA", (10, 135),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                
                # Mostra frame
                cv2.imshow('Line Follower', info_frame)
                
                # Processa teclas
                key = cv2.waitKey(1) & 0xFF
                
                if key == 27 or key == ord('q'):  # ESC ou Q
                    print("\nEncerrando...")
                    break
                elif key == ord(' '):  # ESPAÇO
                    paused = not paused
                    if paused:
                        await self.send_command("stop")
                        print("⏸ Pausado")
                    else:
                        print("▶ Retomado")
                elif key == ord('r'):  # R
                    self.frame_count = 0
                    self.detection_count = 0
                    print("↻ Estatísticas resetadas")
                elif key == ord('+') or key == ord('='):  # +
                    self.base_speed = min(100, self.base_speed + 5)
                    print(f"⬆ Velocidade: {self.base_speed}")
                elif key == ord('-') or key == ord('_'):  # -
                    self.base_speed = max(20, self.base_speed - 5)
                    print(f"⬇ Velocidade: {self.base_speed}")
                
                # Pequeno delay para não sobrecarregar
                await asyncio.sleep(0.01)
        
        finally:
            # Para o carrinho
            await self.send_command("stop")
            
            # Libera recursos
            cap.release()
            cv2.destroyAllWindows()
            
            if self.websocket:
                await self.websocket.close()
            
            print("\n=== Estatísticas ===")
            print(f"Total de frames: {self.frame_count}")
            print(f"Linha detectada: {self.detection_count} frames")
            if self.frame_count > 0:
                detection_rate = (self.detection_count / self.frame_count) * 100
                print(f"Taxa de detecção: {detection_rate:.1f}%")

def parse_arguments():
    """Parse argumentos da linha de comando"""
    parser = argparse.ArgumentParser(description='Seguidor de Linha com Visão Computacional')
    
    parser.add_argument('esp32_ip', type=str,
                      help='Endereço IP do ESP32 (ex: 192.168.1.100)')
    
    parser.add_argument('--camera', type=str, default=None,
                      help='URL da câmera IP/celular (ex: http://192.168.1.101:8080/video)')
    
    parser.add_argument('--debug', action='store_true',
                      help='Ativa modo debug com visualizações extras')
    
    parser.add_argument('--speed', type=int, default=45,
                      help='Velocidade base (20-100, padrão: 45)')
    
    parser.add_argument('--roi', type=float, default=0.3,
                      help='Altura da região de interesse (0.1-0.5, padrão: 0.3)')
    
    return parser.parse_args()

async def main():
    """Função principal"""
    print("=" * 50)
    print("  SEGUIDOR DE LINHA - VISÃO COMPUTACIONAL")
    print("=" * 50)
    print()
    
    args = parse_arguments()
    
    # Cria objeto LineFollower
    follower = LineFollower(
        esp32_ip=args.esp32_ip,
        camera_url=args.camera,
        debug=args.debug
    )
    
    # Ajusta parâmetros
    follower.base_speed = max(20, min(100, args.speed))
    follower.roi_height = max(0.1, min(0.5, args.roi))
    
    print(f"ESP32 IP: {args.esp32_ip}")
    print(f"Câmera: {args.camera if args.camera else 'Webcam padrão'}")
    print(f"Velocidade base: {follower.base_speed}")
    print(f"ROI: {int(follower.roi_height * 100)}% inferior")
    print(f"Debug: {'Ativado' if args.debug else 'Desativado'}")
    print()
    
    # Inicia seguimento
    await follower.follow_line()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n✓ Programa encerrado pelo usuário")
    except Exception as e:
        print(f"\n✗ Erro: {e}")

