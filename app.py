from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Definimos la "forma" que tendrá el mensaje que nos envíe el frontend
class ChatMessage(BaseModel):
    message: str

# Mantenemos nuestro endpoint de prueba
@app.get("/api/message")
async def get_message():
    return {"message": "¡Hola desde el backend de FastAPI!"}

# 3. Creamos nuestro nuevo endpoint para el chat
@app.post("/api/chat")
async def chat(request: ChatMessage):
    # Por ahora, la lógica es simple:
    # Recibimos el mensaje del usuario y devolvemos una respuesta fija.
    user_message = request.message
    print(f"Mensaje recibido: {user_message}") # Útil para ver en la terminal del backend

    bot_response = "He recibido tu mensaje. Próximamente tendré una respuesta más inteligente."
    
    return {"response": bot_response}