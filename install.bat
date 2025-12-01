@echo off
REM Script de instalação para Windows
REM Uso: install.bat

echo ==========================================
echo   CARRINHO SEGUIDOR DE LINHA
echo   Instalação de Dependências
echo ==========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python não encontrado!
    echo   Instale Python 3.7+ do site python.org
    pause
    exit /b 1
)

echo + Python encontrado
python --version

REM Verifica se pip está instalado
pip --version >nul 2>&1
if errorlevel 1 (
    echo X pip não encontrado!
    echo   Reinstale Python com a opção pip
    pause
    exit /b 1
)

echo + pip encontrado
pip --version
echo.

REM Pergunta sobre ambiente virtual
set /p create_venv="Deseja criar um ambiente virtual? (s/n): "

if /i "%create_venv%"=="s" (
    echo Criando ambiente virtual...
    python -m venv venv
    
    echo Ativando ambiente virtual...
    call venv\Scripts\activate.bat
    
    echo + Ambiente virtual criado e ativado
    echo.
)

REM Instala dependências
echo Instalando dependências...
cd pc
pip install -r requirements.txt

if errorlevel 0 (
    echo.
    echo ==========================================
    echo   + INSTALAÇÃO CONCLUÍDA COM SUCESSO!
    echo ==========================================
    echo.
    echo Próximos passos:
    echo.
    echo 1. Configure o ESP32:
    echo    - Edite esp32\config.py com suas credenciais WiFi
    echo    - Faça upload dos arquivos para o ESP32
    echo.
    echo 2. Configure a câmera do celular:
    echo    - Instale 'IP Webcam' ou 'DroidCam'
    echo    - Anote o URL (ex: http://192.168.1.101:8080/video)
    echo.
    echo 3. Teste a conexão:
    echo    python test_connection.py IP_DO_ESP32 URL_DA_CAMERA
    echo.
    echo 4. Calibre a detecção:
    echo    python calibrate_hsv.py --camera URL_DA_CAMERA
    echo.
    echo 5. Execute o seguidor de linha:
    echo    python line_follower.py IP_DO_ESP32 --camera URL_DA_CAMERA
    echo.
    echo Leia o README.md para mais informações!
    echo.
    
    if /i "%create_venv%"=="s" (
        echo IMPORTANTE: Para usar o ambiente virtual, execute:
        echo    venv\Scripts\activate
        echo.
    )
) else (
    echo.
    echo X Erro na instalação das dependências
    echo   Verifique a conexão com a internet e tente novamente
    pause
    exit /b 1
)

pause

