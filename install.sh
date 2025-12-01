#!/bin/bash

# Script de instalação rápida
# Uso: bash install.sh

echo "=========================================="
echo "  CARRINHO SEGUIDOR DE LINHA"
echo "  Instalação de Dependências"
echo "=========================================="
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "   Instale Python 3.7+ e tente novamente"
    exit 1
fi

echo "✓ Python encontrado: $(python3 --version)"

# Verifica se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado!"
    echo "   Instale pip e tente novamente"
    exit 1
fi

echo "✓ pip encontrado: $(pip3 --version)"
echo ""

# Cria ambiente virtual (opcional mas recomendado)
read -p "Deseja criar um ambiente virtual? (s/n): " create_venv

if [ "$create_venv" = "s" ] || [ "$create_venv" = "S" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
    
    echo "Ativando ambiente virtual..."
    source venv/bin/activate
    
    echo "✓ Ambiente virtual criado e ativado"
    echo ""
fi

# Instala dependências
echo "Instalando dependências..."
cd pc/
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "  ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
    echo "=========================================="
    echo ""
    echo "Próximos passos:"
    echo ""
    echo "1. Configure o ESP32:"
    echo "   - Edite esp32/config.py com suas credenciais WiFi"
    echo "   - Faça upload dos arquivos para o ESP32"
    echo ""
    echo "2. Configure a câmera do celular:"
    echo "   - Instale 'IP Webcam' ou 'DroidCam'"
    echo "   - Anote o URL (ex: http://192.168.1.101:8080/video)"
    echo ""
    echo "3. Teste a conexão:"
    echo "   python test_connection.py IP_DO_ESP32 URL_DA_CAMERA"
    echo ""
    echo "4. Calibre a detecção:"
    echo "   python calibrate_hsv.py --camera URL_DA_CAMERA"
    echo ""
    echo "5. Execute o seguidor de linha:"
    echo "   python line_follower.py IP_DO_ESP32 --camera URL_DA_CAMERA"
    echo ""
    echo "📚 Leia o README.md para mais informações!"
    echo ""
    
    if [ "$create_venv" = "s" ] || [ "$create_venv" = "S" ]; then
        echo "⚠️  Para usar o ambiente virtual, execute:"
        echo "   source venv/bin/activate"
        echo ""
    fi
else
    echo ""
    echo "❌ Erro na instalação das dependências"
    echo "   Verifique a conexão com a internet e tente novamente"
    exit 1
fi

