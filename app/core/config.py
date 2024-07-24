from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from ultralytics import YOLO
import threading

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Carregar os modelos YOLOv8
model = YOLO('yolov8n.pt')
modelCapacete = YOLO('bestCapacete.pt')

# Variáveis para controlar o estado das câmeras
webcam_active = False
camRua_active = False
webcam_frames = []
camRua_frames = []
frame_lock = threading.Lock()
