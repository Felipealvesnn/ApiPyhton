import speech_recognition as sr
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import whisper
from pydub import AudioSegment
import io

app = APIRouter()


@app.post("/")
async def transcribe_audio(file: UploadFile = File(...)):
    recognizer = sr.Recognizer()

    try:
        # Convert the audio file to WAV format using pydub
        audio_content = await file.read()
        # modelo = whisper.load_model("base")

        # resposta = modelo.transcribe("Gravando.m4a")
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_content))
        audio_segment = audio_segment.set_frame_rate(16000)  # Ensure a standard frame rate
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)

        # Use the audio file for speech recognition
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)

            # Use Google's speech recognition service
            text = recognizer.recognize_google(audio_data, language="pt-BR")
            return JSONResponse(content={"text": text})
    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="Google Speech Recognition não conseguiu entender o áudio")
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao solicitar resultados do serviço Google Speech Recognition; {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo de áudio: {e}")


