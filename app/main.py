# app\main.py
# =============================================================
# FastAPI backend para geração de códigos EAN-13
# Autor: HDevSoluções
# =============================================================
from fastapi import APIRouter, Query
from fastapi.middleware.cors import CORSMiddleware
from app.gerador_ean import GeradorEAN13
from typing import List

router = APIRouter()

@router.get("/gerar", summary="Gerar códigos EAN-13", response_model=List[dict])
def gerar_codigos(
    quantidade: int = Query(5, ge=1, le=100),
    prefixo_empresa: str = Query("9999", max_length=4) # Removido min_length
):
    # Preenche com zeros à esquerda até ter no mínimo 3 dígitos (ex: "9" vira "009")
    prefixo_ajustado = prefixo_empresa.zfill(3)
    
    gerador = GeradorEAN13(prefixo_empresa=prefixo_ajustado)
    return gerador.gerar_lote(quantidade)

