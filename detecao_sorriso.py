import cv2
import mediapipe as mp
import math

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Configurar o modelo Face Mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Inicializar a captura de vídeo - tenta encontrar uma câmera disponível
def find_available_camera():
    """Tenta encontrar uma câmera disponível, começando da 0"""
    for camera_index in range(3):  # Tenta índices 0, 1 e 2
        cap = cv2.VideoCapture(camera_index)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Camera encontrada no indice {camera_index}")
                return cap
            cap.release()
    print("ERRO: Nenhuma camera disponivel!")
    return None

webcam = find_available_camera()
if webcam is None:
    print("Nao foi possivel abrir a camera. Encerrando...")
    exit(1)

# Threshold para detectar sorriso (ajuste conforme necessário)
# Valores maiores = mais fácil detectar sorriso
SMILE_THRESHOLD = 0.03  # Distância normalizada entre os cantos da boca

print("Pressione 'q' para sair")
print("Pressione 'r' para recalibrar o threshold")

calibrated = False
base_distance = 0.0

while True:
    ret, frame = webcam.read()
    if not ret:
        print("Erro ao ler frame da camera")
        break
    
    # Converter BGR para RGB (MediaPipe usa RGB)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Processar o frame
    result = face_mesh.process(rgb)
    
    # Obter dimensões do frame
    height, width, channels = frame.shape
    
    # Verificar se detectou face
    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            # Pontos dos cantos da boca no MediaPipe Face Mesh
            # Ponto 61: canto esquerdo da boca
            # Ponto 291: canto direito da boca
            point1 = face_landmarks.landmark[61]   # Canto esquerdo
            point2 = face_landmarks.landmark[291]  # Canto direito
            
            # Converter coordenadas normalizadas para pixels
            x1 = int(point1.x * width)
            y1 = int(point1.y * height)
            x2 = int(point2.x * width)
            y2 = int(point2.y * height)
            
            # Calcular distância euclidiana entre os cantos da boca
            distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
            
            # Normalizar a distância (dividir pela largura do frame para normalizar)
            normalized_distance = distance / width
            
            # Calibrar na primeira detecção (distância base quando não está sorrindo)
            if not calibrated:
                base_distance = normalized_distance
                calibrated = True
                print(f"Calibrado! Distância base: {base_distance:.4f}")
            
            # Determinar se está sorrindo
            # Quando sorrimos, a distância entre os cantos da boca aumenta
            distance_diff = normalized_distance - base_distance
            is_smiling = distance_diff > SMILE_THRESHOLD
            
            # Desenhar os pontos dos cantos da boca
            cv2.circle(frame, (x1, y1), 5, (0, 0, 255), -1)  # Canto esquerdo (vermelho)
            cv2.circle(frame, (x2, y2), 5, (0, 255, 0), -1)  # Canto direito (verde)
            
            # Desenhar linha entre os cantos
            cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
            
            # Mostrar informações na tela
            status_text = "SORRINDO!" if is_smiling else "Não sorrindo"
            color = (0, 255, 0) if is_smiling else (0, 0, 255)
            
            # Desenhar texto com fundo para melhor legibilidade
            cv2.rectangle(frame, (10, 10), (300, 100), (0, 0, 0), -1)
            cv2.putText(frame, status_text, (20, 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(frame, f"Distancia: {distance_diff:.4f}", (20, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    else:
        # Se não detectou face, resetar calibração
        calibrated = False
        cv2.putText(frame, "Face nao detectada", (20, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Exibir o frame
    cv2.imshow("Detecao de Sorriso", frame)
    
    # Sair com 'q' ou ESC
    key = cv2.waitKey(10) & 0xFF
    if key == ord('q') or key == 27:  # 27 é ESC
        break
    elif key == ord('r'):
        # Recalibrar
        calibrated = False
        print("Recalibrando...")

# Limpar recursos
webcam.release()
cv2.destroyAllWindows()
face_mesh.close()

