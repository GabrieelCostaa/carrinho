# 🚀 PRÓXIMOS PASSOS - Configuração Personalizada

## ✅ O que já está pronto:
- ✅ Código completo criado
- ✅ Git configurado e com commit
- ✅ Python 3.12.6 instalado
- ✅ Pip instalado
- ✅ Dependências instaladas (OpenCV, NumPy, WebSockets)

---

## 📋 CHECKLIST DE PRÓXIMOS PASSOS

### 1️⃣ CONFIGURAR ESP32 (Hardware)

#### O que você precisa:
- [ ] ESP32 ou ESP8266
- [ ] Cabo USB para conectar o ESP32 ao computador
- [ ] Driver de motor L298N
- [ ] 2x Motores DC com rodas
- [ ] Bateria/fonte para os motores
- [ ] Fios jumper

#### Passos:

**A) Instalar MicroPython no ESP32:**

```bash
# 1. Instale o esptool
pip3 install esptool

# 2. Baixe o firmware MicroPython para ESP32
# Acesse: https://micropython.org/download/esp32/
# Baixe o arquivo .bin mais recente

# 3. Conecte o ESP32 via USB e descubra a porta
ls /dev/cu.*
# Procure por algo como: /dev/cu.usbserial-XXXX

# 4. Apague a flash (substitua PORT pela porta encontrada)
esptool.py --port /dev/cu.usbserial-XXXX erase_flash

# 5. Grave o firmware (substitua esp32-xxxxx.bin pelo arquivo baixado)
esptool.py --port /dev/cu.usbserial-XXXX write_flash -z 0x1000 esp32-xxxxx.bin
```

**B) Configurar WiFi:**

```bash
# 1. Edite o arquivo de configuração
nano esp32/config.py

# 2. Altere as credenciais WiFi:
WIFI_SSID = "SuaRedeWiFi"          # ← SEU WIFI AQUI
WIFI_PASSWORD = "SuaSenhaWiFi"     # ← SUA SENHA AQUI

# 3. Configure os pinos dos motores conforme seu hardware
# (os valores padrão funcionam para L298N comum)
```

**C) Upload do código para ESP32:**

```bash
# 1. Instale ampy
pip3 install adafruit-ampy

# 2. Faça upload dos arquivos (substitua PORT)
ampy --port /dev/cu.usbserial-XXXX put esp32/config.py
ampy --port /dev/cu.usbserial-XXXX put esp32/main.py

# 3. Reinicie o ESP32 (desconecte e reconecte USB)

# 4. Veja o IP do ESP32 no monitor serial
screen /dev/cu.usbserial-XXXX 115200
# Pressione CTRL+A depois K para sair
```

**📝 ANOTE O IP DO ESP32:** `192.168.1.___`

---

### 2️⃣ CONFIGURAR CÂMERA DO CELULAR

#### Opção A: IP Webcam (Android - RECOMENDADO)

1. **Instale o app:**
   - Abra Google Play Store
   - Procure por "IP Webcam"
   - Instale o app gratuito

2. **Configure:**
   - Abra o app
   - Role até "Resolução do vídeo" → escolha **640x480**
   - Role até "Qualidade do JPEG" → deixe em **50-70%**
   - Role até o final e clique em **"Iniciar servidor"**

3. **Anote a URL:**
   - O app mostrará algo como: `http://192.168.1.101:8080`
   - **Sua URL será:** `http://192.168.1.101:8080/video`

**📝 ANOTE A URL DA CÂMERA:** `http://192.168.1.___:8080/video`

#### Opção B: Usar webcam do computador

- Não precisa configurar nada
- O sistema usará automaticamente a webcam do Mac

---

### 3️⃣ TESTAR CONEXÕES

```bash
cd "/Users/gabrielcosta/Documents/vs code/carrinho/pc"

# Teste básico (sem câmera do celular - usa webcam do Mac)
python3 test_connection.py IP_DO_ESP32

# Teste completo (com câmera do celular)
python3 test_connection.py IP_DO_ESP32 URL_DA_CAMERA

# Exemplo:
python3 test_connection.py 192.168.1.100 http://192.168.1.101:8080/video
```

**Resultado esperado:**
```
✅ Conectado ao ESP32
✅ Câmera OK
🎉 Tudo pronto!
```

---

### 4️⃣ CALIBRAR DETECÇÃO DE LINHA

```bash
cd "/Users/gabrielcosta/Documents/vs code/carrinho/pc"

# Com webcam do Mac
python3 calibrate_hsv.py

# Com câmera do celular
python3 calibrate_hsv.py --camera http://192.168.1.101:8080/video
```

**Como calibrar:**
1. A janela mostrará 3 imagens lado a lado
2. Ajuste os trackbars na parte superior até que:
   - **Imagem do meio mostre APENAS a linha em BRANCO**
   - Todo o resto deve ficar PRETO
3. Anote os valores finais mostrados no terminal
4. Copie para o arquivo `pc/config.py`

**Para linha PRETA:**
- V Max deve ficar baixo (~50)

**Para linha BRANCA:**
- V Min deve ficar alto (~200)

---

### 5️⃣ EXECUTAR O SEGUIDOR DE LINHA! 🎉

```bash
cd "/Users/gabrielcosta/Documents/vs code/carrinho/pc"

# Modo básico (webcam do Mac)
python3 line_follower.py IP_DO_ESP32

# Modo completo (câmera do celular)
python3 line_follower.py IP_DO_ESP32 --camera URL_DA_CAMERA

# Exemplo real:
python3 line_follower.py 192.168.1.100 --camera http://192.168.1.101:8080/video

# Com modo debug (para ver o processamento)
python3 line_follower.py 192.168.1.100 --camera http://192.168.1.101:8080/video --debug

# Com velocidade personalizada
python3 line_follower.py 192.168.1.100 --camera http://192.168.1.101:8080/video --speed 60
```

**Controles durante execução:**
- **ESPAÇO** = Pausar/Retomar
- **ESC ou Q** = Sair
- **+** = Aumentar velocidade
- **-** = Diminuir velocidade
- **R** = Resetar estatísticas

---

## 🎯 RESUMO DOS COMANDOS RÁPIDOS

```bash
# 1. Testar conexão
cd "/Users/gabrielcosta/Documents/vs code/carrinho/pc"
python3 test_connection.py 192.168.1.100

# 2. Calibrar
python3 calibrate_hsv.py

# 3. Executar
python3 line_follower.py 192.168.1.100
```

---

## 📝 INFORMAÇÕES QUE VOCÊ PRECISA ANOTAR

Preencha conforme você configura:

```
IP DO ESP32:        192.168.1.___
Porta Serial:       /dev/cu.usbserial-___
URL da Câmera:      http://192.168.1.___:8080/video

HSV Calibrado:
  LOWER: [___, ___, ___]
  UPPER: [___, ___, ___]
```

---

## 🔧 SE DER ALGUM PROBLEMA

### ESP32 não conecta ao WiFi
```bash
# Verifique o monitor serial
screen /dev/cu.usbserial-XXXX 115200
# Veja se aparece "Conectado ao WiFi!" e o IP
```

### Não acha a porta do ESP32
```bash
# Liste todas as portas USB
ls /dev/cu.*
# Procure por: cu.usbserial, cu.SLAB_USBtoUART, ou cu.wchusbserial
```

### Câmera do celular não conecta
- Verifique se celular e Mac estão na mesma rede WiFi
- Teste a URL no navegador do Mac: `http://192.168.1.101:8080`
- Se funcionar, adicione `/video` no final

### Linha não é detectada
- Execute `python3 calibrate_hsv.py`
- Ajuste os valores HSV até ver apenas a linha
- Copie os valores para `pc/config.py`

---

## 📚 DOCUMENTAÇÃO ADICIONAL

- **Dúvidas gerais:** Leia `README.md`
- **Problemas específicos:** Veja `EXEMPLOS.md` > Troubleshooting
- **Entender arquitetura:** Leia `ARQUITETURA.md`
- **Guia rápido:** Veja `QUICK_START.md`

---

## ✅ CHECKLIST FINAL

- [ ] ESP32 com MicroPython instalado
- [ ] Código enviado para o ESP32
- [ ] ESP32 conectando ao WiFi (IP anotado)
- [ ] Câmera configurada (celular ou webcam)
- [ ] Teste de conexão passou
- [ ] HSV calibrado
- [ ] Line follower executando

---

## 🎓 VOCÊ ESTÁ AQUI:

```
[✅] Código criado
[✅] Git configurado
[✅] Python instalado
[✅] Dependências instaladas
[⏳] Configurar ESP32          ← PRÓXIMO PASSO
[ ] Configurar câmera
[ ] Testar conexões
[ ] Calibrar detecção
[ ] Executar!
```

---

## 🚀 COMECE AGORA!

**Se você tem o ESP32 em mãos:**
→ Vá para o passo 1️⃣ (Configurar ESP32)

**Se ainda não tem o hardware:**
→ Monte o carrinho primeiro, depois volte aqui

**Quer testar só o software de visão?**
→ Pule para o passo 4️⃣ (Calibrar) usando sua webcam

---

**BOA SORTE! 🏆🚗💨**

*Leia COMECE_AQUI.txt para mais informações*

