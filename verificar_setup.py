#!/usr/bin/env python3
"""
Script de verificação de setup
Verifica o que está configurado e o que ainda precisa ser feito
"""

import sys
import subprocess
import os

def check_command(command, name):
    """Verifica se um comando está disponível"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def check_python_package(package):
    """Verifica se um pacote Python está instalado"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def main():
    print("=" * 70)
    print("  VERIFICAÇÃO DE SETUP - CARRINHO SEGUIDOR DE LINHA")
    print("=" * 70)
    print()
    
    all_ok = True
    
    # 1. Python
    print("📦 AMBIENTE PYTHON")
    print("-" * 70)
    
    if check_command("python3 --version", "Python 3"):
        version = subprocess.run("python3 --version", shell=True, capture_output=True, text=True)
        print(f"  ✅ Python instalado: {version.stdout.strip()}")
    else:
        print(f"  ❌ Python 3 não encontrado")
        all_ok = False
    
    if check_command("pip3 --version", "pip3"):
        print(f"  ✅ pip instalado")
    else:
        print(f"  ❌ pip3 não encontrado")
        all_ok = False
    
    print()
    
    # 2. Dependências Python
    print("📚 DEPENDÊNCIAS PYTHON")
    print("-" * 70)
    
    packages = {
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'websockets': 'WebSockets'
    }
    
    for pkg, name in packages.items():
        if check_python_package(pkg):
            print(f"  ✅ {name} instalado")
        else:
            print(f"  ❌ {name} não instalado")
            print(f"     → Execute: pip3 install -r pc/requirements.txt")
            all_ok = False
    
    print()
    
    # 3. Ferramentas para ESP32
    print("🔧 FERRAMENTAS PARA ESP32")
    print("-" * 70)
    
    if check_command("esptool.py --version", "esptool"):
        print(f"  ✅ esptool instalado")
    else:
        print(f"  ⚠️  esptool não instalado (necessário para gravar ESP32)")
        print(f"     → Execute: pip3 install esptool")
    
    if check_command("ampy --version", "ampy"):
        print(f"  ✅ ampy instalado")
    else:
        print(f"  ⚠️  ampy não instalado (necessário para upload de arquivos)")
        print(f"     → Execute: pip3 install adafruit-ampy")
    
    print()
    
    # 4. Git
    print("📝 CONTROLE DE VERSÃO")
    print("-" * 70)
    
    if os.path.exists('.git'):
        print(f"  ✅ Repositório Git inicializado")
        
        # Verifica status do Git
        result = subprocess.run("git status --short", shell=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(f"  ⚠️  Há arquivos não commitados")
        else:
            print(f"  ✅ Nenhuma mudança pendente")
    else:
        print(f"  ❌ Repositório Git não inicializado")
        all_ok = False
    
    print()
    
    # 5. Arquivos de configuração
    print("⚙️  CONFIGURAÇÃO")
    print("-" * 70)
    
    if os.path.exists('esp32/config.py'):
        with open('esp32/config.py', 'r') as f:
            content = f.read()
            if 'SEU_WIFI' in content or 'SUA_SENHA' in content:
                print(f"  ⚠️  esp32/config.py precisa ser configurado")
                print(f"     → Edite WiFi SSID e PASSWORD")
            else:
                print(f"  ✅ esp32/config.py configurado")
    else:
        print(f"  ❌ esp32/config.py não encontrado")
        all_ok = False
    
    if os.path.exists('pc/config.py'):
        print(f"  ✅ pc/config.py existe")
    else:
        print(f"  ❌ pc/config.py não encontrado")
        all_ok = False
    
    print()
    
    # 6. Hardware (não pode verificar automaticamente)
    print("🔌 HARDWARE (manual)")
    print("-" * 70)
    print(f"  ❓ ESP32 conectado via USB?")
    print(f"     → Verifique: ls /dev/cu.*")
    print(f"  ❓ Motores e driver L298N conectados?")
    print(f"  ❓ Câmera do celular configurada?")
    print(f"     → Instale 'IP Webcam' no Android")
    
    print()
    
    # Resumo
    print("=" * 70)
    if all_ok:
        print("  ✅ AMBIENTE CONFIGURADO COM SUCESSO!")
        print()
        print("  PRÓXIMOS PASSOS:")
        print("  1. Configure WiFi em esp32/config.py")
        print("  2. Conecte o ESP32 via USB")
        print("  3. Faça upload do código: ampy --port PORT put esp32/main.py")
        print("  4. Configure câmera do celular")
        print("  5. Execute: python3 pc/test_connection.py IP_DO_ESP32")
        print()
        print("  📚 Leia: PROXIMOS_PASSOS.md para guia detalhado")
    else:
        print("  ⚠️  ALGUMAS DEPENDÊNCIAS ESTÃO FALTANDO")
        print()
        print("  Execute os comandos sugeridos acima para corrigir")
    print("=" * 70)
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())

