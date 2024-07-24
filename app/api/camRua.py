import threading
from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
from app.core.config import model, camRua_active, camRua_frames, frame_lock
import cv2

router = APIRouter()

# Função para capturar e processar frames da câmera da rua
rtsp_url = "rtsp://admin:admin1234@45.179.125.157:554/cam/realmonitor?channel=1&subtype=0"
def process_CameraRua():
    global camRua_active
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Erro ao abrir a câmera da rua")
        return

    while camRua_active:
        ret, frame = cap.read()

        if not ret:
            print("Erro ao capturar o frame da câmera da rua")
            break
        desired_width, desired_height = 840, 680
        frame = cv2.resize(frame, (desired_width, desired_height))
        motoqueiro_results = model(frame)
        # results = modelCapacete.predict(frame, conf=0.5, show=False)
        frame = motoqueiro_results[0].plot()

        # Armazena o frame processado
        with frame_lock:
            camRua_frames.append(frame)

    cap.release()
    cv2.destroyAllWindows()

@router.get("/start_camRua")
async def start_camRua():
    global camRua_active
    camRua_active = True
    threading.Thread(target=process_CameraRua).start()
    return Response(status_code=204)

@router.get("/stop_camRua")
async def stop_camRua():
    global camRua_active
    camRua_active = False
    return Response(status_code=204)

# Gerar frames para o feed da câmera da rua
def generate_camRua_frames():
    while True:
        if camRua_frames:
            with frame_lock:
                frame = camRua_frames.pop(0)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@router.get("/camRua_feed")
async def camRua_feed():
    return StreamingResponse(generate_camRua_frames(), media_type='multipart/x-mixed-replace; boundary=frame')
