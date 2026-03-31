import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Permisos para que tu Angular se conecte sin problemas
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
    # Obtenemos la llave de Groq
    api_key = os.getenv("GROQ_API_KEY")
    
    # Validamos que la llave exista para no fallar a ciegas
    if not api_key:
        return {"respuesta": "Error del servidor: Falta la API Key de Groq."}

    # URL oficial de Groq (compatible con el formato OpenAI)
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Configuramos el modelo Llama 3 (súper rápido y gratuito)
    payload = {
        "model": "llama3-8b-8192", 
        "messages": [
            {"role": "system", "content": "Eres el asistente virtual de VEN FCC, una tienda universitaria. Sé amigable, breve y ayuda con dudas sobre entregas o pagos."},
            {"role": "user", "content": mensaje.texto}
        ]
    }

    try:
        # Hacemos la petición a Groq
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        # Si Groq responde con éxito (200 OK)
        if response.status_code == 200:
            respuesta_texto = data['choices'][0]['message']['content']
            return {"respuesta": respuesta_texto}
        else:
            # Si Groq nos manda un error (ej. llave inválida)
            error_msg = data.get('error', {}).get('message', 'Error desconocido')
            return {"respuesta": f"Error de Groq: {error_msg}"}
            
    except Exception as e:
        # Si el servidor se queda sin internet o algo crashea
        return {"respuesta": f"Error interno de conexión: {str(e)}"}