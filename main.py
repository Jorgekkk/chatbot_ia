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
    
    # CAMBIO 1: Cambiamos 'v1beta' por 'v1' y el nombre del modelo a 'gemini-1.5-flash'
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # CAMBIO 2: Simplificamos el payload (quitamos system_instruction por ahora para asegurar conexión)
    payload = {
        "contents": [{
            "parts": [{"text": f"Responde como asistente de la tienda VEN FCC de forma breve: {mensaje.texto}"}]
        }]
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        # Depuración: Si falla, esto nos dirá qué dice Google ahora
        if "candidates" in data and len(data["candidates"]) > 0:
            texto_ia = data["candidates"][0]["content"]["parts"][0]["text"]
            return {"respuesta": texto_ia}
        else:
            return {"respuesta": f"Error detallado de Google: {str(data)}"}
            
    except Exception as e:
        return {"respuesta": f"Error de conexión: {str(e)}"}