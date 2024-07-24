import threading
from fastapi import APIRouter, Response, Depends
from app.core.config import model, modelCapacete, webcam_active, webcam_frames, frame_lock
import cv2

router = APIRouter()


# Função para capturar e processar frames da webcam
def process_webcam():
    global webcam_active
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao abrir a webcam")
        return

    while webcam_active:
        ret, frame = cap.read()

        if not ret:
            print("Erro ao capturar o frame da webcam")
            break

        motoqueiro_results = model(frame)
        results = modelCapacete.predict(frame, conf=0.5, show=True)
        frame = results[0].plot()

        # Armazena o frame processado
        with frame_lock:
            webcam_frames.append(frame)

    cap.release()
    cv2.destroyAllWindows()

@router.get("/start_webcam")
async def start_webcam():
    global webcam_active
    webcam_active = True
    threading.Thread(target=process_webcam).start()
    return Response(status_code=204)

@router.get("/stop_webcam")
async def stop_webcam():
    global webcam_active
    webcam_active = False
    return Response(status_code=204)

# Gerar frames para o feed da webcam
def generate_webcam_frames():
    while True:
        if webcam_frames:
            with frame_lock:
                frame = webcam_frames.pop(0)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@router.get("/webcam_feed")
async def webcam_feed():
    return Response(generate_webcam_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

