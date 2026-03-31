import os
import requests # Necesitamos esta librería
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Mensaje(BaseModel):
    texto: str

@app.post("/api/chat")
def responder_chat(mensaje: Mensaje):
    api_key = os.getenv("GEMINI_API_KEY")
    # URL oficial de Google sin librerías intermedias
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": mensaje.texto}]
        }],
        "system_instruction": {
            "parts": [{"text": "Eres el asistente de la tienda VEN FCC. Sé breve y amable."}]
        }
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        
        if "candidates" in data:
            texto_ia = data["candidates"][0]["content"]["parts"][0]["text"]
            return {"respuesta": texto_ia}
        else:
            return {"respuesta": f"Error de la IA: {str(data)}"}
            
    except Exception as e:
        return {"respuesta": f"Error de conexión: {str(e)}"}