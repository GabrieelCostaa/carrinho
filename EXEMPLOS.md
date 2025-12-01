# 💡 Exemplos Práticos de Uso

## 📱 Exemplo 1: Configuração Inicial

### Passo 1: Configurar WiFi no ESP32

```python
# Edite: esp32/config.py
WIFI_SSID = "MinhaRedeWiFi"
WIFI_PASSWORD = "minha_senha_123"
```

### Passo 2: Upload para ESP32

```bash
# Instale a ferramenta
pip install adafruit-ampy

# Faça upload (substitua /dev/ttyUSB0 pela sua porta)
ampy --port /dev/ttyUSB0 put esp32/config.py
ampy --port /dev/ttyUSB0 put esp32/main.py

# Verifique
ampy --port /dev/ttyUSB0 ls
```

### Passo 3: Veja o IP do ESP32

```bash
# Abra monitor serial
screen /dev/ttyUSB0 115200

# Saída esperada:
# Conectando ao WiFi...
# ...
# Conectado ao WiFi!
# IP: 192.168.1.100
# Servidor WebSocket aguardando conexões em ws://192.168.1.100:8765
```

**Anote o IP: `192.168.1.100`** ✍️

---

## 📸 Exemplo 2: Configurar Câmera do Celular

### IP Webcam (Android)

1. **Instale o app** "IP Webcam" da Play Store

2. **Configure as opções:**
   - Resolução: 640x480 (suficiente e mais rápido)
   - Qualidade: 50-70%
   - Orientação: Paisagem

3. **Inicie o servidor:**
   - Role até o final do app
   - Clique em "Iniciar servidor"
   - Você verá: `http://192.168.1.101:8080`

4. **Teste no navegador:**
   ```
   http://192.168.1.101:8080/video
   ```
   Você deve ver o vídeo da câmera!

5. **URL para usar:**
   ```
   http://192.168.1.101:8080/video
   ```

**Anote a URL** ✍️

---

## 🎨 Exemplo 3: Calibrar Detecção de Linha

### Calibração Passo a Passo

```bash
cd pc/

# Execute o calibrador
python calibrate_hsv.py --camera http://192.168.1.101:8080/video
```

### Ajustando os Trackbars:

**Para LINHA PRETA em fundo claro:**

1. **H Min**: 0
2. **H Max**: 180
3. **S Min**: 0
4. **S Max**: 255
5. **V Min**: 0
6. **V Max**: 40-60 ⬅️ **Ajuste este!**

👁️ **Visualização:**
- Frame esquerdo: imagem original
- Frame centro: máscara binária (ajuste até ver só a linha em branco)
- Frame direito: resultado filtrado

**Valores de exemplo para linha preta:**
```
H Min: 0
H Max: 180
S Min: 0
S Max: 255
V Min: 0
V Max: 50
```

**Copie para `pc/config.py`:**
```python
LOWER_BLACK = [0, 0, 0]
UPPER_BLACK = [180, 255, 50]
```

---

## 🏃 Exemplo 4: Primeiro Teste

### Teste Completo de Conexão

```bash
cd pc/

# Teste conexão com ESP32 e câmera
python test_connection.py 192.168.1.100 http://192.168.1.101:8080/video
```

**Saída esperada:**
```
🔌 Tentando conectar ao ESP32 em ws://192.168.1.100:8765...
✅ Conectado com sucesso!

🧪 Testando comandos básicos...
  [1/8] Enviando: {'action': 'forward', 'speed': 40}
  ✓ Resposta: {"status": "ok"}
  [2/8] Enviando: {'action': 'stop'}
  ✓ Resposta: {"status": "ok"}
  ...

✅ Teste concluído com sucesso!

📸 Testando câmera...
✅ Câmera OK (5/5 frames capturados)

==========================================
  RESULTADO DO TESTE
==========================================
Câmera: ✅ OK
ESP32:  ✅ OK

🎉 Tudo pronto! Você pode rodar o line_follower.py
```

---

## 🚗 Exemplo 5: Executar Seguidor de Linha

### Execução Básica

```bash
cd pc/

python line_follower.py 192.168.1.100 \
  --camera http://192.168.1.101:8080/video \
  --speed 45
```

### Durante a Execução:

**Tela mostrará:**
```
==================================================
  SEGUIDOR DE LINHA - VISÃO COMPUTACIONAL
==================================================

ESP32 IP: 192.168.1.100
Câmera: http://192.168.1.101:8080/video
Velocidade base: 45
ROI: 30% inferior
Debug: Desativado

✓ Conectado ao ESP32 em ws://192.168.1.100:8765
✓ Câmera conectada

Controles:
  ESC ou Q - Sair
  ESPAÇO - Pausar/Retomar
  R - Resetar estatísticas
  + - Aumentar velocidade base
  - - Diminuir velocidade base
```

**Na janela do vídeo:**
```
┌─────────────────────────────────────┐
│ ATIVO                               │
│ Frames: 243                         │
│ Detecções: 201                      │
│ Velocidade: 45                      │
│ Linha: DETECTADA                    │
│                                     │
│        [Vídeo da câmera]            │
│             com linha               │
│         destacada em verde          │
│                                     │
└─────────────────────────────────────┘
```

### Ajustando Durante Execução:

1. **Muito lento?** → Pressione `+` várias vezes
2. **Oscilando muito?** → Pressione `-` para reduzir velocidade
3. **Quer pausar?** → Pressione `ESPAÇO`
4. **Encerrar?** → Pressione `ESC` ou `Q`

---

## 🎯 Exemplo 6: Modo Debug

### Para Ver Processamento Detalhado

```bash
python line_follower.py 192.168.1.100 \
  --camera http://192.168.1.101:8080/video \
  --debug
```

**Visualização no modo debug:**
```
┌──────────────────┬──────────────────┐
│  Frame Original  │  Máscara Binária │
│  + ROI marcada   │  (preto/branco)  │
│  + Centro linha  │                  │
│                  │    ████████      │
│      🔴          │    ████████      │
│       │          │      ████        │
│    ───┼───       │        █         │
│       │          │                  │
└──────────────────┴──────────────────┘
    Desvio: +85px → Vira DIREITA
```

Use para:
- ✅ Verificar se a linha está sendo detectada corretamente
- ✅ Ajustar calibração HSV
- ✅ Ver exatamente o que o algoritmo "enxerga"
- ✅ Debug de problemas de detecção

---

## 📊 Exemplo 7: Cenários de Uso Real

### Cenário 1: Linha Reta Simples

```
Chão:     ████████████████████████████████
Linha:            ████
Carrinho:          🚗

Comportamento:
- Detecção: ✓
- Desvio: ~0px
- Ação: Forward (ambos motores = 45)
- Resultado: Segue reto ━━▶
```

### Cenário 2: Curva Suave à Direita

```
Chão:     ████████████████████████████████
Linha:            ████
                    ████
                      ████
Carrinho:          🚗

Comportamento:
- Detecção: ✓
- Desvio: +50px (linha à direita)
- Ação: Vira direita (left=45, right=30)
- Resultado: Curva suave ━━╮
                           ▼
```

### Cenário 3: Curva Fechada à Esquerda

```
Chão:     ████████████████████████████████
Linha:    ████
          ████
            ████
Carrinho:          🚗

Comportamento:
- Detecção: ✓
- Desvio: -180px (linha muito à esquerda!)
- Ação: Curva brusca (left=-15, right=55)
- Resultado: Giro rápido    ╭━━
                            ▲
```

### Cenário 4: Linha Perdida

```
Chão:     ████████████████████████████████
Linha:    (nenhuma no campo de visão)
Carrinho:          🚗

Comportamento:
- Detecção: ✗
- Desvio: N/A
- Ação: STOP (ambos motores = 0)
- Resultado: Para ■
```

---

## 🏆 Exemplo 8: Configuração para Competição

### Setup Otimizado

```python
# pc/config.py - CONFIGURAÇÃO PARA COMPETIÇÃO

# Velocidades agressivas
BASE_SPEED = 65          # Rápido mas controlado
TURN_SPEED = 75          # Curvas rápidas
SHARP_TURN_THRESHOLD = 120  # Curvas mais sensíveis

# ROI focado
ROI_HEIGHT = 0.25        # Apenas 25% inferior (mais próximo)

# Processamento rápido
BLUR_KERNEL_SIZE = 3     # Menos blur = mais rápido
MIN_CONTOUR_AREA = 80    # Detecta linhas menores
COMMAND_INTERVAL = 0.03  # 33 comandos/segundo

# HSV bem calibrado (exemplo)
LOWER_BLACK = [0, 0, 0]
UPPER_BLACK = [180, 255, 45]

# Câmera otimizada
CAMERA_URL = "http://192.168.1.101:8080/video"
# Configure no app: Resolução 640x480, 30 FPS
```

### Checklist Pré-Competição

```bash
# 1. Teste de conexão
python test_connection.py 192.168.1.100 http://192.168.1.101:8080/video

# 2. Calibração no local
python calibrate_hsv.py --camera http://192.168.1.101:8080/video

# 3. Teste com debug
python line_follower.py 192.168.1.100 \
  --camera http://192.168.1.101:8080/video \
  --debug --speed 45

# 4. Teste de velocidade (sem debug)
python line_follower.py 192.168.1.100 \
  --camera http://192.168.1.101:8080/video \
  --speed 65

# 5. Corrida!
python line_follower.py 192.168.1.100 \
  --camera http://192.168.1.101:8080/video \
  --speed 70
```

---

## 🔧 Exemplo 9: Troubleshooting com Exemplos

### Problema: "Linha não detectada"

**Debug:**
```bash
# 1. Veja o que a câmera está capturando
python calibrate_hsv.py --camera http://192.168.1.101:8080/video
```

**Soluções:**
- ✅ Ajuste V Max (linha preta) ou V Min (linha branca)
- ✅ Verifique iluminação (evite sombras)
- ✅ Melhore contraste da linha

### Problema: "Carrinho oscila muito"

**Debug:**
```bash
# Execute com debug para ver o desvio
python line_follower.py 192.168.1.100 --debug --speed 35
```

**Soluções:**
- ✅ Reduza `BASE_SPEED` (comece com 35)
- ✅ Aumente `SHARP_TURN_THRESHOLD` (de 150 para 200)
- ✅ Fixe melhor a câmera (trepidação causa oscilação)

### Problema: "Delay/lag na resposta"

**Debug:**
```bash
# Verifique FPS e latência no modo debug
python line_follower.py 192.168.1.100 --debug
```

**Soluções:**
- ✅ Reduza resolução da câmera (use 640x480)
- ✅ Reduza `COMMAND_INTERVAL` (de 0.05 para 0.03)
- ✅ Use WiFi 5GHz se possível
- ✅ Aproxime roteador

---

## 📚 Exemplo 10: Controle Manual via Python

### Script para Testar Motores Manualmente

```python
# teste_manual.py
import asyncio
import websockets
import json

async def controlar_carrinho():
    uri = "ws://192.168.1.100:8765"
    
    async with websockets.connect(uri) as websocket:
        print("Conectado! Use as teclas:")
        print("w = frente, s = ré, a = esquerda, d = direita, x = parar")
        
        while True:
            cmd = input("Comando (w/a/s/d/x/q): ").lower()
            
            if cmd == 'q':
                await websocket.send(json.dumps({"action": "stop"}))
                break
            elif cmd == 'w':
                await websocket.send(json.dumps({"action": "forward", "speed": 50}))
            elif cmd == 's':
                await websocket.send(json.dumps({"action": "backward", "speed": 50}))
            elif cmd == 'a':
                await websocket.send(json.dumps({"action": "left", "speed": 50}))
            elif cmd == 'd':
                await websocket.send(json.dumps({"action": "right", "speed": 50}))
            elif cmd == 'x':
                await websocket.send(json.dumps({"action": "stop"}))
            
            response = await websocket.recv()
            print(f"Resposta: {response}")

asyncio.run(controlar_carrinho())
```

**Uso:**
```bash
python teste_manual.py
```

---

## 🎓 Exemplo 11: Logs e Estatísticas

### Ao Encerrar o Programa

```
=== Estatísticas ===
Total de frames: 1543
Linha detectada: 1401 frames
Taxa de detecção: 90.8%

Interpretação:
- 90%+  : Excelente! ✓
- 70-90%: Bom, mas pode melhorar
- <70%  : Recalibre HSV ou melhore iluminação
```

---

**Com estes exemplos, você está pronto para qualquer situação! 🚀**

