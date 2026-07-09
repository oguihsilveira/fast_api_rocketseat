import uvicorn # Complexidade: Uvicorn / Servidor python
from fastapi import FastAPI

app = FastAPI()

@app.get("/saudar/{nome}")
# Complexidade: Async / Assincronismo
async def saudar(nome: str): # Complexidade: Tipagem
    print(type(nome))
    return {"mensagem": f"Olá, {nome}"}

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=3001,
        reload=True
    )

# --------------------
# 1. Servidor
# 2. Tipagem
# #. Assincronismo
# 4. Documentação