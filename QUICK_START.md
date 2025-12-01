# 🚀 Guia Rápido de Início

## ⚡ Início Rápido em 5 Passos

### 1️⃣ Preparar o ESP32
```bash
# Edite esp32/config.py com suas credenciais WiFi
# Faça upload para o ESP32
# Anote o IP mostrado no serial monitor
```

### 2️⃣ Instalar Dependências no PC
```bash
cd pc/
pip install -r requirements.txt
```

### 3️⃣ Configurar Câmera do Celular
```
1. Instale "IP Webcam" (Android) ou "DroidCam"
2. Inicie o servidor no app
3. Anote a URL (ex: http://192.168.1.101:8080/video)
```

### 4️⃣ Calibrar Detecção
```bash
# Ajuste os valores HSV para sua linha
python calibrate_hsv.py --camera http://192.168.1.101:8080/video

# Copie os valores para config.py
```

### 5️⃣ Rodar!
```bash
python line_follower.py 192.168.1.100 --camera http://192.168.1.101:8080/video
```

## 🎯 Comandos Essenciais

### Testar Conexão
```bash
python test_connection.py 192.168.1.100
```

### Calibrar HSV
```bash
python calibrate_hsv.py --camera URL_DA_CAMERA
```

### Rodar Seguidor de Linha
```bash
# Básico
python line_follower.py IP_DO_ESP32

# Com câmera do celular
python line_follower.py IP_DO_ESP32 --camera URL_DA_CAMERA

# Com debug ativado
python line_follower.py IP_DO_ESP32 --debug

# Velocidade customizada
python line_follower.py IP_DO_ESP32 --speed 60
```

## ⌨️ Controles

- **ESPAÇO**: Pausar/Retomar
- **ESC ou Q**: Sair
- **+/-**: Ajustar velocidade
- **R**: Resetar estatísticas

## 🔧 Ajustes Importantes

### Para Linha PRETA:
```python
LOWER_BLACK = [0, 0, 0]
UPPER_BLACK = [180, 255, 50]  # V Max baixo
```

### Para Linha BRANCA:
```python
LOWER_WHITE = [0, 0, 200]     # V Min alto
UPPER_WHITE = [180, 30, 255]
```

### Velocidade:
- **Iniciante**: `--speed 35`
- **Normal**: `--speed 45` (padrão)
- **Avançado**: `--speed 60`
- **Competição**: `--speed 70+`

## 🐛 Problemas Comuns

| Problema | Solução |
|----------|---------|
| ESP32 não conecta | Verifique WiFi e reinicie |
| Linha não detectada | Calibre HSV novamente |
| Carrinho oscila | Reduza velocidade |
| Câmera não conecta | PC e celular na mesma rede |

## 📋 Checklist Pré-Competição

- [ ] ESP32 conectando ao WiFi
- [ ] Câmera funcionando
- [ ] Valores HSV calibrados
- [ ] Teste em linha similar à competição
- [ ] Velocidade otimizada
- [ ] Bateria carregada
- [ ] Backup de configurações

## 🏆 Dicas para Ganhar

1. **Teste, teste, teste!**
2. Calibre no ambiente da competição
3. Comece devagar e aumente velocidade
4. Fixe bem a câmera (sem trepidação)
5. Use linha com bom contraste
6. Tenha um plano B

## 📞 Ajuda Rápida

```bash
# Ver ajuda
python line_follower.py --help

# Testar tudo
python test_connection.py IP_ESP32 URL_CAMERA

# Calibrar
python calibrate_hsv.py --camera URL_CAMERA
```

---

**Boa sorte! 🏁**

