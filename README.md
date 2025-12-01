# 🚗 Carrinho Seguidor de Linha - Visão Computacional

Sistema completo de seguidor de linha usando visão computacional com ESP32, câmera de celular e Python/OpenCV.

## 📋 Descrição do Projeto

Este projeto implementa um carrinho robótico que segue uma linha no chão usando:
- **ESP32**: Recebe comandos via WebSocket e controla os motores
- **Celular**: Funciona como câmera web (ou use webcam do PC)
- **Python + OpenCV**: Processa imagens e detecta a linha
- **WebSocket**: Comunicação em tempo real entre PC e carrinho

## 🎯 Objetivo

Fazer o carrinho seguir uma linha preta/branca no chão por pelo menos 40cm com o melhor tempo possível.

## 📁 Estrutura do Projeto

```
carrinho/
├── esp32/              # Código MicroPython para ESP32
│   ├── main.py         # Servidor WebSocket e controle dos motores
│   └── config.py       # Configurações (WiFi, pinos)
│
├── pc/                 # Software Python para PC
│   ├── line_follower.py    # Script principal
│   ├── calibrate_hsv.py    # Ferramenta de calibração
│   ├── config.py           # Configurações
│   └── requirements.txt    # Dependências Python
│
└── README.md
```

## 🔧 Hardware Necessário

### Carrinho:
- ESP32 (ou ESP8266)
- Driver de motor L298N ou similar
- 2x Motores DC com rodas
- Bateria/Fonte de alimentação
- Chassi do carrinho

### Extras:
- Celular com app de câmera IP (IP Webcam, DroidCam) OU webcam USB
- PC/Notebook com Python 3.7+
- Linha preta em fundo claro (ou vice-versa)

## 📱 Configuração da Câmera do Celular

### Opção 1: IP Webcam (Android)
1. Instale o app "IP Webcam" da Play Store
2. Abra o app e role até o final
3. Clique em "Iniciar servidor"
4. Anote o endereço IP mostrado (ex: `http://192.168.1.100:8080`)
5. Use esta URL: `http://SEU_IP:8080/video`

### Opção 2: DroidCam (Android/iOS)
1. Instale o "DroidCam" no celular e PC
2. Conecte via WiFi
3. Use a URL: `http://SEU_IP:4747/video`

### Opção 3: Webcam do PC
- Não precisa configurar nada, deixe o parâmetro `--camera` vazio

## 🚀 Instalação

### 1. Configurar o ESP32

#### Instalar MicroPython no ESP32:
```bash
# Baixe o firmware em: https://micropython.org/download/esp32/
# Instale esptool
pip install esptool

# Apague flash (substitua PORT pela sua porta, ex: /dev/ttyUSB0 ou COM3)
esptool.py --port PORT erase_flash

# Grave o firmware
esptool.py --port PORT write_flash -z 0x1000 esp32-xxxxx.bin
```

#### Configurar WiFi:
1. Edite `esp32/config.py`:
```python
WIFI_SSID = "SeuWiFi"
WIFI_PASSWORD = "SuaSenha"
```

2. Ajuste os pinos dos motores conforme seu hardware

#### Upload do código:
```bash
# Instale ampy
pip install adafruit-ampy

# Faça upload dos arquivos
ampy --port PORT put esp32/config.py
ampy --port PORT put esp32/main.py
```

#### Iniciar o carrinho:
- Reinicie o ESP32
- Ele se conectará ao WiFi e mostrará o IP no serial monitor
- Anote este IP!

### 2. Configurar o PC

#### Instalar dependências:
```bash
cd pc/
pip install -r requirements.txt
```

#### Configurar parâmetros (opcional):
Edite `pc/config.py` para ajustar:
- IP do ESP32
- URL da câmera
- Velocidades
- Parâmetros de detecção

## 🎮 Como Usar

### 1. Calibrar Detecção de Linha (Importante!)

Antes de usar, calibre os valores HSV para sua linha e iluminação:

```bash
cd pc/

# Se usar webcam do PC:
python calibrate_hsv.py

# Se usar celular como câmera:
python calibrate_hsv.py --camera http://192.168.1.100:8080/video
```

- Ajuste os trackbars até que apenas a linha apareça em branco
- Anote os valores e copie para `config.py`

### 2. Executar o Seguidor de Linha

```bash
cd pc/

# Uso básico com webcam do PC:
python line_follower.py 192.168.1.100

# Com câmera do celular:
python line_follower.py 192.168.1.100 --camera http://192.168.1.101:8080/video

# Com modo debug (visualizações extras):
python line_follower.py 192.168.1.100 --debug

# Ajustando velocidade:
python line_follower.py 192.168.1.100 --speed 60

# Ajustando ROI (região de interesse):
python line_follower.py 192.168.1.100 --roi 0.4
```

### 3. Controles Durante Execução

- **ESC** ou **Q**: Sair
- **ESPAÇO**: Pausar/Retomar
- **R**: Resetar estatísticas
- **+**: Aumentar velocidade base
- **-**: Diminuir velocidade base

## ⚙️ Como Funciona

### Fluxo de Funcionamento:

1. **Câmera captura imagem** → Celular ou webcam
2. **PC processa imagem** → OpenCV detecta linha
3. **Calcula desvio** → Quanto a linha está do centro
4. **Decide ação** → Frente, esquerda, direita
5. **Envia comando** → Via WebSocket para ESP32
6. **ESP32 controla motores** → Ajusta velocidades

### Processamento de Imagem:

```
Frame Original
    ↓
Seleciona ROI (região inferior)
    ↓
Converte para HSV
    ↓
Aplica filtro (detecta cor da linha)
    ↓
Operações morfológicas (limpa ruído)
    ↓
Encontra contornos
    ↓
Calcula centro da linha
    ↓
Calcula desvio do centro
    ↓
Ajusta velocidades dos motores
```

### Lógica de Controle:

- **Linha no centro**: Ambos motores na velocidade base
- **Linha à direita**: Motor esquerdo mais rápido
- **Linha à esquerda**: Motor direito mais rápido
- **Desvio grande**: Curva brusca (pode inverter um motor)
- **Linha não detectada**: Para o carrinho

## 🎯 Dicas para Melhor Desempenho

### Hardware:
- ✅ Use fita isolante preta em chão claro (melhor contraste)
- ✅ Mantenha a linha com ~2-3cm de largura
- ✅ Evite sombras e reflexos
- ✅ Posicione a câmera olhando para baixo (~45°)
- ✅ Fixe bem a câmera para evitar trepidação

### Software:
- ✅ Calibre os valores HSV em cada ambiente
- ✅ Ajuste a velocidade base (comece baixo ~40)
- ✅ Ajuste o ROI para focar na região da linha
- ✅ Use modo debug para visualizar o processamento
- ✅ Teste em diferentes iluminações

### Otimizações para Competição:
- 🏁 Aumente gradualmente a velocidade
- 🏁 Ajuste fino do PID (implemente se necessário)
- 🏁 Reduza o `COMMAND_INTERVAL` para resposta mais rápida
- 🏁 Otimize o ângulo e posição da câmera
- 🏁 Use curvas mais agressivas se a linha tiver curvas fechadas

## 🔍 Troubleshooting

### ESP32 não conecta ao WiFi:
- Verifique SSID e senha em `esp32/config.py`
- Verifique se o roteador está próximo
- Reinicie o ESP32

### Linha não é detectada:
- Execute `calibrate_hsv.py` e ajuste os valores
- Verifique iluminação do ambiente
- Teste com diferentes cores/materiais de linha

### Carrinho não se move:
- Verifique conexão WebSocket
- Teste os motores manualmente
- Verifique pinos configurados em `esp32/config.py`
- Verifique alimentação dos motores

### Câmera do celular não conecta:
- Celular e PC devem estar na mesma rede WiFi
- Verifique firewall do PC
- Teste a URL no navegador primeiro

### Carrinho oscila muito:
- Reduza velocidade base
- Ajuste `SHARP_TURN_THRESHOLD`
- Suavize curvas (reduza diferença entre motores)

### Delay na resposta:
- Reduza `COMMAND_INTERVAL`
- Use câmera com menor resolução
- Otimize processamento (ROI menor)

## 📊 Estrutura de Comandos WebSocket

### Formato JSON:

```json
{
  "action": "forward",
  "speed": 50
}
```

### Ações disponíveis:
- `forward`: Move para frente
- `backward`: Move para trás
- `left`: Curva suave à esquerda
- `right`: Curva suave à direita
- `sharp_left`: Curva brusca à esquerda
- `sharp_right`: Curva brusca à direita
- `stop`: Para
- `custom`: Controle manual dos motores

### Exemplo de controle customizado:
```json
{
  "action": "custom",
  "left": 70,
  "right": 30
}
```

## 🏆 Critérios de Avaliação

- **Nota Mínima (5)**: Percorrer 40cm seguindo a linha
- **Nota Máxima (10)**: Melhor tempo na competição
- **Nota Proporcional**: Baseada no ranking de tempos

### Dicas para Nota Máxima:
1. Otimize a velocidade (rápido mas estável)
2. Minimize oscilações
3. Teste muito antes da competição
4. Ajuste fino em condições similares ao lab
5. Tenha um plano B (configurações alternativas)

## 📚 Conceitos Utilizados

- **Visão Computacional**: OpenCV, processamento de imagem, detecção de contornos
- **Comunicação em Rede**: WebSocket, protocolo cliente-servidor
- **Sistemas Embarcados**: MicroPython, ESP32, controle PWM
- **Controle de Motores**: Driver L298N, controle diferencial
- **Python Assíncrono**: asyncio, websockets

## 🤝 Equipe

- Máximo de 4 alunos por equipe
- Cada membro pode contribuir em diferentes partes (hardware, software, calibração, testes)

## 📝 Licença

Este projeto é para fins educacionais.

## 🆘 Suporte

Em caso de dúvidas:
1. Leia este README completamente
2. Verifique a seção de Troubleshooting
3. Teste cada componente separadamente
4. Consulte o professor/monitor

---

**Boa sorte na competição! 🏁🚗💨**

