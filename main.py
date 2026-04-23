# main.py  
# =============================================================
# FastAPI backend para geração de códigos EAN-13
# Autor: HDevSoluções
# =============================================================
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.main import router as api_router
import uvicorn

app = FastAPI()

# 1. Localiza a pasta raiz do projeto de forma absoluta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Configura os caminhos absolutos para static e templates
static_path = os.path.join(BASE_DIR, "static")
templates_path = os.path.join(BASE_DIR, "templates")

# 3. Inicializa as ferramentas com os caminhos fixos
templates = Jinja2Templates(directory=templates_path)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Inclui as rotas da API
app.include_router(api_router)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)