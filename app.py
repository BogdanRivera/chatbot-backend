from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
from transformers import pipeline

pipe = pipeline("text-generation", model="bogdanrivera/legal_oaxaca_llama3-1_8B_unsloth")

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


class ChatMessage(BaseModel):
    message: str


@app.get("/api/message")
async def get_message():
    return {"message": "¡Hola desde el backend de FastAPI!"}

@app.post("/api/chat")
async def chat(request: ChatMessage):
    user_message = request.message
    print(f"Mensaje recibido: {user_message}") 
    
    messages = [
        {"role": "user", "content": user_message},
    ]


    raw_output = pipe(messages, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    
    bot_response = ""


    try:
        last_message = raw_output[0]['generated_text'][-1]
        if last_message['role'] == 'assistant':
            bot_response = last_message['content']
        else:
            bot_response = "El modelo no generó una respuesta de asistente."
            
    except (IndexError, KeyError, TypeError) as e:
        print(f"Error al procesar la respuesta del modelo: {e}")
        bot_response = "Hubo un error al procesar la respuesta del modelo."

    print(f"Respuesta del bot: {bot_response}")
    return {"response": bot_response}