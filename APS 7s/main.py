from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import io

app = FastAPI(title="Sistema de Cálculo Emergético LCI")

# Configuração de CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CalculadoraEmergia:
    """Implementação do padrão Strategy para o cálculo dos indicadores de sustentabilidade."""
    @staticmethod
    def calcular_indicadores(r: float, n: float, f: float):
        y = r + n + f
        eyr = y / f if f > 0 else 0
        elr = (f + n) / r if r > 0 else 0
        esi = eyr / elr if elr > 0 else 0
        return {"EYR": round(eyr, 2), "ELR": round(elr, 2), "ESI": round(esi, 2)}

@app.post("/api/processar-lci")
async def processar_lci(file: UploadFile = File(...)):
    try:
        content = await file.read()

        # Leitura do arquivo com suporte a múltiplos delimitadores
        df = pd.read_csv(io.StringIO(content.decode('utf-8', errors='ignore')), sep=r';|,|\t', engine='python')

        # Sanitização de cabeçalhos: remoção de espaços, aspas residuais e conversão para minúsculas
        df.columns = df.columns.str.strip().str.replace('"', '').str.lower()

        # Validação estrutural do arquivo submetido
        colunas_obrigatorias = ['tipo', 'quantidade', 'transformidade']
        for col in colunas_obrigatorias:
            if col not in df.columns:
                return JSONResponse(
                    status_code=400,
                    content={"erro": f"Inconsistência de dados: A coluna obrigatória '{col}' não foi localizada no arquivo submetido. Verifique a grafia e a estrutura do documento."}
                )

        # Conversão forçada para numérico (mitiga erros de tipagem devido a aspas residuais nos valores)
        df['quantidade'] = pd.to_numeric(df['quantidade'].astype(str).str.replace('"', ''), errors='coerce')
        df['transformidade'] = pd.to_numeric(df['transformidade'].astype(str).str.replace('"', ''), errors='coerce')

        # Aplicação da álgebra emergética
        df['emergia'] = df['quantidade'] * df['transformidade']

        # Agrupamento por categoria LCI
        somas = df.groupby('tipo')['emergia'].sum().to_dict()
        r = somas.get('r', 0) + somas.get('R', 0)
        n = somas.get('n', 0) + somas.get('N', 0)
        f = somas.get('f', 0) + somas.get('F', 0)

        indicadores = CalculadoraEmergia.calcular_indicadores(r, n, f)

        # Estruturação topológica para a renderização de grafos (Vis.js)
        nodes = [
            {"id": 1, "label": "Recursos Renováveis (R)", "color": "#22c55e"},
            {"id": 2, "label": "Não Renováveis (N)", "color": "#f59e0b"},
            {"id": 3, "label": "Insumos Econômicos (F)", "color": "#ef4444"},
            {"id": 4, "label": "Processo Produtivo", "color": "#3b82f6"}
        ]
        edges = [
            {"from": 1, "to": 4, "label": f"{r:.2e} sej", "arrows": "to"},
            {"from": 2, "to": 4, "label": f"{n:.2e} sej", "arrows": "to"},
            {"from": 3, "to": 4, "label": f"{f:.2e} sej", "arrows": "to"}
        ]

        return {
            "indicadores": indicadores,
            "rede": {"nodes": nodes, "edges": edges}
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"erro": f"Erro interno de processamento. O arquivo pode conter caracteres inválidos ou corrompidos. Detalhe técnico: {str(e)}"}
        )