from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Input(BaseModel):
    tema: str

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/gerar")
def gerar_conteudo(data: Input):
    return {
        "conteudo": f"Conteúdo estratégico sobre: {data.tema}"
    }
