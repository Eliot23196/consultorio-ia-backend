from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# Configuración Maestra de CORS para Proyectos EDA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Aquí pegamos tu llave
GEMINI_KEY = "AIzaSyDRxCBDmECFeNHUG8gWCReGDwPix5zLmRs"
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class Consulta(BaseModel):
    texto: str

@app.get("/")
def home():
    return {"status": "Backend de EDA Health Activo"}

@app.post("/consultar")
async def consulta_medica(datos: Consulta):
    try:
        prompt = f"Eres un asistente médico experto. Analiza el siguiente caso: {datos.texto}"
        response = model.generate_content(prompt)
        return {"respuesta": response.text}
    except Exception as e:
        print(f"Error detectado: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la conexión con la IA")

if __name__ == "__main__":
    import uvicorn
    # Render asigna el puerto automáticamente
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
