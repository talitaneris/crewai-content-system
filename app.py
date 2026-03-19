import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from anthropic import Anthropic

app = FastAPI()

class Input(BaseModel):
    tema: str

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/gerar")
def gerar_conteudo(data: Input):
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY não configurada")

    try:
        client = Anthropic(api_key=api_key)

        prompt = f"""
Você é uma estrategista de conteúdo para Instagram.

Crie um conteúdo estratégico em português com base no tema abaixo.

Tema: {data.tema}

Regras:
- linguagem direta, forte e clara
- evitar clichês e conteúdo genérico
- gerar identificação e autoridade
- entregar:
1. gancho
2. desenvolvimento
3. fechamento com CTA para visitar o perfil
"""

        response = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=800,
            temperature=0.8,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        texto = ""
        for bloco in response.content:
            if bloco.type == "text":
                texto += bloco.text

        return {"conteudo": texto.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
