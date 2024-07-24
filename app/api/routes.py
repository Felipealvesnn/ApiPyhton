from fastapi import APIRouter
from app.api import webcam, camRua, AudioEmTexto

router = APIRouter()
router.include_router(webcam.router, prefix="/webcam", tags=["Webcam"])
router.include_router(camRua.router, prefix="/camRua", tags=["CamRua"])
router.include_router(AudioEmTexto.app, prefix="/transcreverAudio", tags=["transcreverAudio"])


