# Sistema de Cálculo Emergético — APS

Aplicação web para análise de sustentabilidade com base na **Teoria da Emergia (Emergy Analysis)**. Permite importar matrizes de Inventário de Ciclo de Vida (LCI) em formato CSV, calcular os três indicadores emergéticos principais e visualizar os fluxos em um diagrama de rede interativo.

---

## Funcionalidades

- **Importação de LCI via CSV** com suporte a delimitadores `,`, `;` e `\t`
- **Cálculo automático** de EYR, ELR e ESI
- **Diagrama de fluxo interativo** (Vis.js) com zoom e drag nos nós
- **Validação e sanitização** do arquivo CSV com mensagens de erro descritivas

---

## Indicadores Calculados

| Indicador | Nome completo | Fórmula | Interpretação |
|-----------|--------------|---------|---------------|
| **EYR** | Emergy Yield Ratio | `Y / F` | Retorno emergético líquido para a sociedade. Quanto maior, melhor. |
| **ELR** | Environmental Loading Ratio | `(N + F) / R` | Estresse imposto ao meio ambiente. Quanto menor, melhor. |
| **ESI** | Emergy Sustainability Index | `EYR / ELR` | Sustentabilidade geral. ESI > 10 indica processo altamente sustentável. |

> Onde: **R** = Recursos Renováveis, **N** = Recursos Não Renováveis, **F** = Insumos Econômicos (Comprados), **Y** = R + N + F

---

## Estrutura do Projeto

```
.
├── index.html   # Frontend (HTML + Tailwind CSS + Vis.js)
└── main.py      # Backend (FastAPI + Pandas)
```

---

## Requisitos

- Python 3.9+
- Dependências Python:

```bash
pip install fastapi uvicorn pandas python-multipart
```

---

## Como Executar

```bash
uvicorn main:app --reload
```

Acesse `http://localhost:8000` no navegador e abra o `index.html` (ou sirva-o via servidor estático apontando para a mesma origem do backend).

---

## Formato do Arquivo CSV

O arquivo deve conter obrigatoriamente as colunas: `id`, `processo`, `tipo`, `quantidade` e `transformidade`.

A coluna `tipo` aceita os valores:

| Valor | Categoria |
|-------|-----------|
| `R` | Recurso Renovável |
| `N` | Recurso Não Renovável |
| `F` | Insumo Econômico (Comprado) |

**Exemplo:**

```csv
id,processo,tipo,quantidade,transformidade
1,Chuva,R,5000,1.5
2,Combustível,N,200,500.0
3,Trabalho,F,10,5000.0
```

> O cálculo de emergia por linha é feito por: `emergia = quantidade × transformidade` (resultado em **sej** — solar emjoules).

---

## Endpoint da API

### `POST /api/processar-lci`

Recebe um arquivo CSV via `multipart/form-data` e retorna os indicadores calculados e a estrutura do grafo.

**Resposta (200):**

```json
{
  "indicadores": {
    "EYR": 1.23,
    "ELR": 4.56,
    "ESI": 0.27
  },
  "rede": {
    "nodes": [...],
    "edges": [...]
  }
}
```

**Resposta de erro (400/500):**

```json
{
  "erro": "Descrição do problema encontrado."
}
```

---

## Tecnologias Utilizadas

| Camada | Tecnologia |
|--------|-----------|
| Frontend | HTML5, Tailwind CSS, Vis.js |
| Backend | Python, FastAPI, Pandas |
| Visualização | Vis Network (grafo interativo) |

---

## Contexto Acadêmico

Projeto desenvolvido como Atividade Prática Supervisionada (APS) para a disciplina de Engenharia de Software — curso de Ciência da Computação, UNIP.
