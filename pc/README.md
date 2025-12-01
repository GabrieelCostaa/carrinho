# PC - Software Python com OpenCV

## 📋 Arquivos

- `line_follower.py`: Script principal do seguidor de linha
- `calibrate_hsv.py`: Ferramenta para calibração de cores
- `test_connection.py`: Teste de conexão com ESP32 e câmera
- `config.py`: Configurações e parâmetros
- `requirements.txt`: Dependências Python

## 🚀 Instalação

```bash
cd pc/
pip install -r requirements.txt
```

## 🎮 Uso

### 1. Testar Conexões
```bash
# Testa ESP32 e câmera
python test_connection.py 192.168.1.100
python test_connection.py 192.168.1.100 http://192.168.1.101:8080/video
```

### 2. Calibrar HSV
```bash
# Calibra detecção de cor da linha
python calibrate_hsv.py
python calibrate_hsv.py --camera http://192.168.1.101:8080/video
```

### 3. Executar Seguidor de Linha
```bash
# Básico (webcam do PC)
python line_follower.py 192.168.1.100

# Com câmera do celular
python line_follower.py 192.168.1.100 --camera http://192.168.1.101:8080/video

# Modo debug
python line_follower.py 192.168.1.100 --debug

# Velocidade customizada
python line_follower.py 192.168.1.100 --speed 60

# ROI customizado (área de interesse)
python line_follower.py 192.168.1.100 --roi 0.4
```

## ⚙️ Configuração

### Editar `config.py`:

```python
# IP do ESP32
ESP32_IP = "192.168.1.100"

# URL da câmera (None = webcam do PC)
CAMERA_URL = "http://192.168.1.101:8080/video"

# Velocidades
BASE_SPEED = 45        # Velocidade padrão
TURN_SPEED = 55        # Velocidade nas curvas
SHARP_TURN_THRESHOLD = 150  # Desvio para curva brusca

# Detecção de linha PRETA
LOWER_BLACK = [0, 0, 0]
UPPER_BLACK = [180, 255, 50]

# Detecção de linha BRANCA (alternativa)
LOWER_WHITE = [0, 0, 200]
UPPER_WHITE = [180, 30, 255]
```

## 🎨 Calibração HSV

### O que é HSV?
- **H** (Hue): Matiz/cor (0-180)
- **S** (Saturation): Saturação (0-255)
- **V** (Value): Brilho (0-255)

### Como calibrar:

1. Execute `python calibrate_hsv.py`
2. Ajuste os trackbars até que apenas a linha apareça em branco
3. Copie os valores mostrados para `config.py`

### Dicas:
- **Linha preta**: V Max baixo (~50)
- **Linha branca**: V Min alto (~200)
- **Iluminação forte**: Ajuste S e V
- **Sombras**: Aumente range de H

## 📊 Como Funciona

### Pipeline de Processamento:

```
1. Captura Frame
   ↓
2. Seleciona ROI (região inferior da imagem)
   ↓
3. Converte BGR → HSV
   ↓
4. Aplica Blur (GaussianBlur)
   ↓
5. Cria Máscara (inRange)
   ↓
6. Operações Morfológicas (erode + dilate)
   ↓
7. Encontra Contornos
   ↓
8. Calcula Centro da Linha
   ↓
9. Calcula Desvio do Centro
   ↓
10. Determina Velocidades dos Motores
    ↓
11. Envia Comando via WebSocket
```

### Lógica de Controle:

```python
if desvio == 0:
    # Centro - segue reto
    left_speed = BASE_SPEED
    right_speed = BASE_SPEED

elif desvio > SHARP_TURN_THRESHOLD:
    # Desvio grande à direita - curva brusca
    left_speed = TURN_SPEED
    right_speed = -TURN_SPEED * 0.3

elif desvio > 0:
    # Desvio pequeno à direita - curva suave
    left_speed = BASE_SPEED
    right_speed = BASE_SPEED * (1 - desvio_normalizado)
```

## 📱 Configurar Câmera do Celular

### IP Webcam (Android):
1. Instale da Play Store
2. Inicie servidor
3. URL: `http://IP:8080/video`

### DroidCam:
1. Instale no celular e PC
2. Conecte via WiFi
3. URL: `http://IP:4747/video`

### iVCam:
1. Instale no celular e PC
2. Use o cliente PC (não precisa URL)

## ⌨️ Controles Durante Execução

| Tecla | Ação |
|-------|------|
| ESC / Q | Sair |
| ESPAÇO | Pausar/Retomar |
| R | Resetar estatísticas |
| + | Aumentar velocidade |
| - | Diminuir velocidade |

## 🎯 Otimizações

### Para Velocidade:
- Reduza resolução da câmera
- Aumente `COMMAND_INTERVAL`
- Use ROI menor
- Desative modo debug

### Para Precisão:
- Aumente resolução da câmera
- Reduza `COMMAND_INTERVAL`
- Use ROI maior
- Calibre HSV cuidadosamente

### Para Estabilidade:
- Reduza `BASE_SPEED`
- Suavize curvas (menor diferença entre motores)
- Aumente área mínima de contorno
- Use blur maior

## 🐛 Debug

### Visualizações no Modo Debug:

- **Frame esquerdo**: Imagem original com ROI e centro da linha
- **Frame direito**: Máscara binária (branco = linha detectada)
- **Info**: Desvio, frames, detecções, velocidade

### Informações Úteis:

```python
# Taxa de detecção
detection_rate = (detection_count / frame_count) * 100

# FPS
fps = frame_count / elapsed_time
```

## 🔧 Parâmetros Ajustáveis

### ROI (Region of Interest):
- `0.1`: Apenas 10% inferior (muito focado)
- `0.3`: 30% inferior (padrão, balanceado)
- `0.5`: 50% inferior (visão ampla)

### Velocidades:
- `20-35`: Muito lento (teste inicial)
- `35-50`: Lento (estável)
- `50-70`: Médio (competição)
- `70-100`: Rápido (arrisca)

### Blur:
- `(3, 3)`: Pouco blur
- `(5, 5)`: Médio (padrão)
- `(7, 7)`: Muito blur

## 📚 Dependências

- **opencv-python**: Processamento de imagem
- **numpy**: Operações numéricas
- **websockets**: Comunicação com ESP32

## 💡 Dicas Avançadas

### Implementar PID:
```python
# Adicione ao line_follower.py
class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0
    
    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        return output
```

### Filtro de Kalman:
Para suavizar detecção e reduzir ruído

### Predição de Trajetória:
Antecipar curvas usando frames anteriores

## 🏆 Checklist de Competição

- [ ] HSV calibrado no ambiente real
- [ ] Velocidade otimizada
- [ ] ROI ajustado
- [ ] Teste em condições similares
- [ ] Bateria do celular carregada
- [ ] Conexão WiFi estável
- [ ] Backup de configurações
- [ ] Plano B (valores alternativos)

---

**Sucesso! 🎯**

