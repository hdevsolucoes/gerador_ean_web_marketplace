# app\gerador_ean.py
# =============================================================
# Projeto: Gerador EAN-13 para API Web
# Autor: HDevSoluções - Transformando ideias em soluções digitais
# Este arquivo é uma versão adaptada para uso com FastAPI
# =============================================================
from typing import List, Dict
from datetime import datetime

class GeradorEAN13:
    def __init__(self, prefixo_empresa: str = "9999"):
        self.prefixo_brasil = "789"
        self.prefixo_empresa = prefixo_empresa
        self.prefixo_fixo = self.prefixo_brasil + self.prefixo_empresa

    @staticmethod
    def calcular_digito_verificador(codigo_12: str) -> str:
        soma = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(codigo_12))
        return str((10 - (soma % 10)) % 10)

    @staticmethod
    def validar_ean_local(ean13: str) -> bool:
        if len(ean13) != 13 or not ean13.isdigit():
            return False
        codigo_12 = ean13[:12]
        digito_informado = ean13[12]
        digito_calculado = GeradorEAN13.calcular_digito_verificador(codigo_12)
        return digito_informado == digito_calculado

    def gerar_lote(self, quantidade: int) -> List[Dict]:
        try:
            agora = datetime.now()
            # Base baseada no tempo para evitar duplicidade imediata
            base = int(f"{agora.hour:02d}{agora.minute:02d}{agora.second // 6}")
            codigos = []
            
            for i in range(quantidade):
                seq = base + i
                if seq > 99999: # Evita que a sequência ultrapasse 5 dígitos
                    break
                
                sequencia = f"{seq:05d}"
                codigo_12 = self.prefixo_fixo + sequencia
                digito_verificador = self.calcular_digito_verificador(codigo_12)
                ean13 = codigo_12 + digito_verificador
                
                codigos.append({
                    "codigo": ean13,
                    "sequencia": sequencia,
                    "digito_verificador": digito_verificador,
                    "valido_local": self.validar_ean_local(ean13)
                })
            return codigos
        except Exception as e:
            # Retorna erro amigável se algo falhar no cálculo
            return [{"erro": "Falha ao gerar sequência numérica", "detalhe": str(e)}]
