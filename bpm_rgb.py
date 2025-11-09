import cv2
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
import time

# --- Filtro passa-faixa (0.7–4 Hz → ~42–240 bpm)
def bandpass_filter(signal, fs, low=0.7, high=4.0, order=3):
    nyq = 0.5 * fs
    b, a = butter(order, [low/nyq, high/nyq], btype='band')
    return filtfilt(b, a, signal)

# --- Inicializa webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Não consegui acessar a webcam.")

# --- Detector de rosto (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# --- Parâmetros
signal = []
timestamps = []
fps_est = 30
start_time = time.time()

print("Pressione 'q' para sair.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        roi = frame[y:y+h//2, x+w//4:x+3*w//4]  # metade superior do rosto
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # média dos canais RGB (apenas verde tende a dar melhor SNR)
        green_mean = np.mean(roi[:, :, 1])
        signal.append(green_mean)
        timestamps.append(time.time() - start_time)

        # Atualiza FPS estimado
        if len(timestamps) > 2:
            fps_est = len(timestamps) / (timestamps[-1] - timestamps[0])

        # A cada 5 s calcula BPM
        if len(signal) > fps_est * 5:
            sig = np.array(signal[-int(fps_est*5):])
            sig = bandpass_filter(sig, fs=fps_est)
            sig = (sig - np.mean(sig)) / np.std(sig)
            peaks, _ = find_peaks(sig, distance=fps_est/2)
            if len(peaks) > 1:
                periodo = np.mean(np.diff(peaks)) / fps_est
                bpm = 60 / periodo
                cv2.putText(frame, f"Pulso estimado: {bpm:.1f} BPM",
                            (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Deteccao de Pulso - Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
