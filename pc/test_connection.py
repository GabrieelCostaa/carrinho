"""
Script para testar a conexão com o ESP32
Use este script para verificar se tudo está funcionando antes de rodar o seguidor de linha
"""

import asyncio
import websockets
import json
import sys

async def test_esp32(esp32_ip, port=8765):
    """Testa conexão e comandos básicos com o ESP32"""
    
    uri = f"ws://{esp32_ip}:{port}"
    print(f"🔌 Tentando conectar ao ESP32 em {uri}...")
    
    try:
        async with websockets.connect(uri, timeout=5) as websocket:
            print("✅ Conectado com sucesso!\n")
            
            # Testa comandos básicos
            commands = [
                {"action": "forward", "speed": 40},
                {"action": "stop"},
                {"action": "left", "speed": 40},
                {"action": "stop"},
                {"action": "right", "speed": 40},
                {"action": "stop"},
                {"action": "backward", "speed": 40},
                {"action": "stop"},
            ]
            
            print("🧪 Testando comandos básicos...\n")
            
            for i, cmd in enumerate(commands, 1):
                print(f"  [{i}/{len(commands)}] Enviando: {cmd}")
                
                # Envia comando
                await websocket.send(json.dumps(cmd))
                
                # Aguarda resposta
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=2)
                    print(f"  ✓ Resposta: {response}")
                except asyncio.TimeoutError:
                    print(f"  ⚠ Timeout - sem resposta")
                
                # Aguarda 1 segundo entre comandos
                await asyncio.sleep(1)
            
            print("\n✅ Teste concluído com sucesso!")
            print("O carrinho está pronto para usar!")
            
    except asyncio.TimeoutError:
        print("❌ Erro: Timeout ao conectar")
        print("Verifique:")
        print("  - O ESP32 está ligado?")
        print("  - O IP está correto?")
        print("  - ESP32 e PC estão na mesma rede?")
        return False
    
    except ConnectionRefusedError:
        print("❌ Erro: Conexão recusada")
        print("Verifique se o servidor WebSocket está rodando no ESP32")
        return False
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

async def test_camera(camera_url=None):
    """Testa conexão com a câmera"""
    import cv2
    
    print("\n📸 Testando câmera...")
    
    if camera_url:
        print(f"   URL: {camera_url}")
        cap = cv2.VideoCapture(camera_url)
    else:
        print("   Usando webcam padrão do PC")
        cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Erro ao abrir câmera")
        return False
    
    # Captura alguns frames
    success_count = 0
    for i in range(5):
        ret, frame = cap.read()
        if ret:
            success_count += 1
    
    cap.release()
    
    if success_count >= 3:
        print(f"✅ Câmera OK ({success_count}/5 frames capturados)")
        return True
    else:
        print(f"❌ Problemas na câmera ({success_count}/5 frames capturados)")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("  TESTE DE CONEXÃO - CARRINHO SEGUIDOR DE LINHA")
    print("=" * 60)
    print()
    
    if len(sys.argv) < 2:
        print("Uso: python test_connection.py <IP_DO_ESP32> [URL_CAMERA]")
        print("\nExemplo:")
        print("  python test_connection.py 192.168.1.100")
        print("  python test_connection.py 192.168.1.100 http://192.168.1.101:8080/video")
        sys.exit(1)
    
    esp32_ip = sys.argv[1]
    camera_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Testa câmera
    camera_ok = asyncio.run(test_camera(camera_url))
    
    # Testa ESP32
    esp32_ok = asyncio.run(test_esp32(esp32_ip))
    
    # Resultado final
    print("\n" + "=" * 60)
    print("  RESULTADO DO TESTE")
    print("=" * 60)
    print(f"Câmera: {'✅ OK' if camera_ok else '❌ FALHOU'}")
    print(f"ESP32:  {'✅ OK' if esp32_ok else '❌ FALHOU'}")
    
    if camera_ok and esp32_ok:
        print("\n🎉 Tudo pronto! Você pode rodar o line_follower.py")
    else:
        print("\n⚠️  Corrija os problemas acima antes de prosseguir")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTestecancelado pelo usuário")

