from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api.routes import router

app = FastAPI()

# Montar a rota para arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="app/templates")

app.include_router(router)

@app.get("/")
async def index(request: Request):
    video_url = request.url_for('static', path='test_video.mp4')
    return templates.TemplateResponse("index.html", {"request": request, "video_url": video_url})

@app.get("/webcam")
async def webcam(request: Request):
    return templates.TemplateResponse("webcam.html", {"request": request})

@app.get("/camLive")
async def camLive(request: Request):
    return templates.TemplateResponse("camLive.html", {"request": request})
