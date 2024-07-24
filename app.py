# import cv2
# from ultralytics import YOLO
# from flask import Flask, render_template, Response, url_for
# import threading

# # Inicializar o aplicativo Flask
# app = Flask(__name__)

# # Carregar os modelos YOLOv8
# # model = YOLO('motoqueiro.pt')
# model = YOLO('yolov8n.pt')
# modelCapacete = YOLO('bestCapacete.pt')
# model.export(format='onnx')
# modelCapacete.export(format='onnx')

# # Variáveis para controlar o estado das câmeras
# webcam_active = False
# camRua_active = False
# webcam_frames = []
# camRua_frames = []
# frame_lock = threading.Lock()

# # Função para capturar e processar frames da webcam
# def process_webcam():
#     global webcam_active
#     cap = cv2.VideoCapture(0)

#     if not cap.isOpened():
#         print("Erro ao abrir a webcam")
#         return

#     while webcam_active:
#         ret, frame = cap.read()

#         if not ret:
#             print("Erro ao capturar o frame da webcam")
#             break

#         motoqueiro_results = model(frame)
#         results = modelCapacete.predict(frame, conf=0.5, show=True)
#         frame = results[0].plot()

#         # Armazena o frame processado
#         with frame_lock:
#             webcam_frames.append(frame)

#     cap.release()
#     cv2.destroyAllWindows()

# # Função para capturar e processar frames da câmera da rua
# rtsp_url = "rtsp://admin:admin1234@45.179.125.157:554/cam/realmonitor?channel=1&subtype=0"
# def process_CameraRua():
#     global camRua_active
#     cap = cv2.VideoCapture(rtsp_url)

#     if not cap.isOpened():
#         print("Erro ao abrir a câmera da rua")
#         return

#     while camRua_active:
#         ret, frame = cap.read()

#         if not ret:
#             print("Erro ao capturar o frame da câmera da rua")
#             break
#         desired_width, desired_height = 840, 680
#         frame = cv2.resize(frame, (desired_width, desired_height))
#         motoqueiro_results = model(frame)
#         # results = modelCapacete.predict(frame, conf=0.5, show=False)
#         frame = motoqueiro_results[0].plot()

#         # Armazena o frame processado
#         with frame_lock:
#             camRua_frames.append(frame)

#     cap.release()
#     cv2.destroyAllWindows()

# # Rota principal para exibir a página HTML
# @app.route('/')
# def index():
#     video_url = url_for('static', filename='test_video.mp4')
#     return render_template('index.html', video_url=video_url)

# # Rota para exibir a página da webcam
# @app.route('/webcam')
# def webcam():
#     return render_template('webcam.html')

# # Rota para iniciar a captura da webcam
# @app.route('/start_webcam')
# def start_webcam():
#     global webcam_active
#     webcam_active = True
#     threading.Thread(target=process_webcam).start()
#     return ('', 204)

# # Rota para parar a captura da webcam
# @app.route('/stop_webcam')
# def stop_webcam():
#     global webcam_active
#     webcam_active = False
#     return ('', 204)

# # Rota para exibir a página camLive
# @app.route('/camLive')
# def camLive():
#     return render_template('camLive.html')

# # Rota para iniciar a captura da câmera da rua
# @app.route('/start_camRua')
# def start_camRua():
#     global camRua_active
#     camRua_active = True
#     threading.Thread(target=process_CameraRua).start()
#     return ('', 204)

# # Rota para parar a captura da câmera da rua
# @app.route('/stop_camRua')
# def stop_camRua():
#     global camRua_active
#     camRua_active = False
#     return ('', 204)

# # Gerar frames para o feed da webcam
# def generate_webcam_frames():
#     while True:
#         if webcam_frames:
#             with frame_lock:
#                 frame = webcam_frames.pop(0)
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# # Gerar frames para o feed da câmera da rua
# def generate_camRua_frames():
#     while True:
#         if camRua_frames:
#             with frame_lock:
#                 frame = camRua_frames.pop(0)
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# # Rota para o feed da webcam
# @app.route('/webcam_feed')
# def webcam_feed():
#     return Response(generate_webcam_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # Rota para o feed da câmera da rua
# @app.route('/camRua_feed')
# def camRua_feed():
#     return Response(generate_camRua_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
