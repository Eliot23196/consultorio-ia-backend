from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# Configuración de CORS absoluta para evitar bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración con tu NUEVA API KEY
GEMINI_KEY = "AIzaSyCcHUSRAjYWq2dmvtx9XxZl1ngIxCGEkUE"
genai.configure(api_key=GEMINI_KEY)

# Usamos el modelo Flash que es el más rápido y confiable
model = genai.GenerativeModel('gemini-pro')

class Consulta(BaseModel):
    texto: str

@app.get("/")
def home():
    return {"status": "Backend de EDA Health Activo"}

@app.post("/consultar")
async def consulta_medica(datos: Consulta):
    try:
        # Log en la consola de Render para verificar que llega la petición
        print(f"Nueva consulta recibida: {datos.texto}")
        
        prompt = f"Eres un asistente médico experto. Analiza el siguiente caso de forma breve y profesional: {datos.texto}"
        
        # Generar contenido
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            return {"respuesta": "La IA no devolvió datos. Intenta con síntomas más específicos."}
            
        return {"respuesta": response.text}
        
    except Exception as e:
        # Capturamos el error real para diagnóstico
        error_detalle = str(e)
        print(f"Error en el proceso: {error_detalle}")
        
        # Enviamos el detalle del error a Vercel para que lo veas en el cuadro rojo
        raise HTTPException(status_code=500, detail=f"Fallo de IA: {error_detalle}")

if __name__ == "__main__":
    import uvicorn
    # Puerto dinámico para Render
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
