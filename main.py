from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# ¡IMPORTANTE! Esto permite que la web de NerdApp se comunique con tu PC
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción pondremos la URL de la web
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key="TU_API_KEY_DE_GEMINI_AQUI")
model = genai.GenerativeModel('gemini-1.5-flash')

class Consulta(BaseModel):
    texto: str

@app.post("/consultar")
async def consulta_medica(datos: Consulta):
    try:
        prompt = f"Eres un asistente médico experto. Analiza lo siguiente y da un resumen clínico: {datos.texto}"
        response = model.generate_content(prompt)
        return {"respuesta": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)