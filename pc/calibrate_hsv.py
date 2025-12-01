"""
Ferramenta de calibração HSV
Use este script para encontrar os valores ideais de HSV para detectar a linha
"""

import cv2
import numpy as np
import argparse

def nothing(x):
    """Callback vazio para trackbars"""
    pass

def calibrate_hsv(camera_url=None):
    """
    Abre uma janela com trackbars para ajustar valores HSV em tempo real
    """
    # Abre câmera
    if camera_url:
        cap = cv2.VideoCapture(camera_url)
    else:
        cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Erro ao abrir câmera")
        return
    
    # Cria janela
    window_name = 'Calibracao HSV'
    cv2.namedWindow(window_name)
    
    # Cria trackbars
    cv2.createTrackbar('H Min', window_name, 0, 180, nothing)
    cv2.createTrackbar('H Max', window_name, 180, 180, nothing)
    cv2.createTrackbar('S Min', window_name, 0, 255, nothing)
    cv2.createTrackbar('S Max', window_name, 255, 255, nothing)
    cv2.createTrackbar('V Min', window_name, 0, 255, nothing)
    cv2.createTrackbar('V Max', window_name, 50, 255, nothing)
    
    print("\n=== CALIBRAÇÃO HSV ===")
    print("Ajuste os trackbars até que apenas a linha apareça em branco")
    print("Pressione ESC ou Q para sair e ver os valores")
    print("\nDica: Para linha PRETA, mantenha V Max baixo (~50)")
    print("      Para linha BRANCA, mantenha V Min alto (~200)\n")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Converte para HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Pega valores dos trackbars
        h_min = cv2.getTrackbarPos('H Min', window_name)
        h_max = cv2.getTrackbarPos('H Max', window_name)
        s_min = cv2.getTrackbarPos('S Min', window_name)
        s_max = cv2.getTrackbarPos('S Max', window_name)
        v_min = cv2.getTrackbarPos('V Min', window_name)
        v_max = cv2.getTrackbarPos('V Max', window_name)
        
        # Cria máscara
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(hsv, lower, upper)
        
        # Aplica máscara ao frame
        result = cv2.bitwise_and(frame, frame, mask=mask)
        
        # Empilha imagens para visualização
        mask_3channel = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        combined = np.hstack([frame, mask_3channel, result])
        
        # Adiciona texto com valores atuais
        text = f"HSV: [{h_min}, {s_min}, {v_min}] - [{h_max}, {s_max}, {v_max}]"
        cv2.putText(combined, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, (0, 255, 0), 2)
        
        cv2.imshow(window_name, combined)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break
    
    # Mostra valores finais
    h_min = cv2.getTrackbarPos('H Min', window_name)
    h_max = cv2.getTrackbarPos('H Max', window_name)
    s_min = cv2.getTrackbarPos('S Min', window_name)
    s_max = cv2.getTrackbarPos('S Max', window_name)
    v_min = cv2.getTrackbarPos('V Min', window_name)
    v_max = cv2.getTrackbarPos('V Max', window_name)
    
    print("\n=== VALORES CALIBRADOS ===")
    print(f"LOWER_HSV = [{h_min}, {s_min}, {v_min}]")
    print(f"UPPER_HSV = [{h_max}, {s_max}, {v_max}]")
    print("\nCopie estes valores para o arquivo config.py")
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calibração HSV')
    parser.add_argument('--camera', type=str, default=None,
                       help='URL da câmera IP')
    args = parser.parse_args()
    
    calibrate_hsv(args.camera)

