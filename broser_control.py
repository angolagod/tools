from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/abrir/{programa}")
def abrir(programa: str):
    os.system(f"start {programa}")
    return {"status": "OK", "message": f"{programa} aberto com sucesso"}

@app.get("/desligar")
def desligar():
    os.system("shutdown /s /t 10")
    return {"status": "OK", "message": "PC será desligado em 10 segundos"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
