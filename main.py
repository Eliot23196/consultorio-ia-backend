from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# Configuración de CORS absoluta
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de API KEY y Modelo
# Sugerencia: En Render, añade GEMINI_KEY en "Environment Variables"
GEMINI_KEY = os.environ.get("GEMINI_KEY", "AIzaSyCcHUSRAjYWq2dmvtx9XxZl1ngIxCGEkUE")
genai.configure(api_key=GEMINI_KEY)

# Actualizado a 1.5-flash para mejor compatibilidad
model = genai.GenerativeModel('gemini-1.5-flash')

class Consulta(BaseModel):
    texto: str

@app.get("/")
def home():
    return {"status": "Backend de EDA Health Activo"}

@app.post("/consultar")
async def consulta_medica(datos: Consulta):
    try:
        print(f"Nueva consulta recibida: {datos.texto}")
        
        # Prompt estructurado para contexto médico
        prompt = f"Eres un asistente médico experto de EDA Health. Analiza de forma breve, profesional y humana el siguiente caso: {datos.texto}"
        
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            return {"respuesta": "La IA no devolvió datos. Intenta con síntomas más específicos."}
            
        return {"respuesta": response.text}
        
    except Exception as e:
        error_detalle = str(e)
        print(f"Error en el proceso: {error_detalle}")
        raise HTTPException(status_code=500, detail=f"Error: {error_detalle}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
