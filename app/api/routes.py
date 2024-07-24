from fastapi import APIRouter
from app.api import webcam, camRua, LerPlaca

router = APIRouter()
router.include_router(webcam.router, prefix="/webcam", tags=["Webcam"])
router.include_router(LerPlaca.app, prefix="/lerplaca", tags=["lerplaca"])
router.include_router(camRua.router, prefix="/camRua", tags=["CamRua"])
# router.include_router(AudioEmTexto.app, prefix="/transcreverAudio", tags=["transcreverAudio"])


