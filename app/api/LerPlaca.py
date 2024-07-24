from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import google.generativeai as genai
import io
 
app = FastAPI()

# Configure a chave de API do Google Generative AI
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.post("/transcribe")
async def transcribe_image(file: UploadFile = File(...)):
    try:
        # Carregar a imagem enviada
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Usar o modelo para gerar conteúdo a partir da imagem
        response = model.generate_content([f"""poderia me falar qual a placa do veiculo?  """, image], stream=False)
        result = response.resolve()
        
        return JSONResponse(content={"text": result.text})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
