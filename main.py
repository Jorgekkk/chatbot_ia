import os
from google import genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Configuración con la nueva librería
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Mantener tus CORS igual...
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
    try:
        
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=mensaje.texto,
            config={
                "system_instruction": "Eres el asistente de VEN FCC, una tienda universitaria. Sé breve y amigable."
            }
        )
        return {"respuesta": response.text}
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {"respuesta": f"Error: {str(e)}"}