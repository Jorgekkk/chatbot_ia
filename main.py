import os
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Configurar IA
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

instrucciones = """
Eres el asistente virtual de VEN FCC, una tienda universitaria. 
Responde dudas sobre entregas (en la explanada) y pagos (Mercado Pago). 
Sé breve, amigable y nunca inventes precios.
"""
modelo = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=instrucciones)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que Angular se conecte
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Mensaje(BaseModel):
    texto: str

@app.post("/api/chat")
def responder_chat(mensaje: Mensaje):
    try:
        respuesta = modelo.generate_content(mensaje.texto)
        return {"respuesta": respuesta.text}
    except Exception as e:
        return {"respuesta": "Ups, tengo un problema de conexión. Intenta de nuevo."}