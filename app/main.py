import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from opentelemetry import trace

from app.algorithms.boyermoore import BoyerMoore
from app.algorithms.bruteforce import BruteForce
from app.algorithms.kmp import KMP
from app.algorithms.rabinkarp import RabinKarp
from app.telemetry import get_logger, get_tracer, record_search, setup_telemetry

# ── Strategy registry ────────────────────────────────────────────────────────
ALGORITHMS = {
    "bruteforce": BruteForce(),
    "kmp": KMP(),
    "rabinkarp": RabinKarp(),
    "boyermoore": BoyerMoore(),
}

ALGO_LABELS = {
    "bruteforce": "Força Bruta (Naive)",
    "kmp": "KMP — Knuth-Morris-Pratt",
    "rabinkarp": "Rabin-Karp",
    "boyermoore": "Boyer-Moore",
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_telemetry()
    yield


app = FastAPI(title="Motor de Busca", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
FRONTEND = Path(__file__).parent.parent / "frontend"
if FRONTEND.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND)), name="static")


@app.get("/")
async def root():
    index = FRONTEND / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return JSONResponse({"status": "ok", "message": "Motor de Busca API"})


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/algorithms")
async def list_algorithms():
    return [{"key": k, "label": v} for k, v in ALGO_LABELS.items()]


@app.post("/search")
async def search(
    file: UploadFile = File(...),
    algorithm: str = Form(...),
    pattern: str = Form(...),
):
    logger = get_logger()
    tracer = get_tracer()

    if algorithm not in ALGORITHMS:
        raise HTTPException(status_code=400, detail=f"Algoritmo desconhecido: {algorithm}")
    if not pattern:
        raise HTTPException(status_code=400, detail="Padrão de busca não pode ser vazio")

    strategy = ALGORITHMS[algorithm]

    with tracer.start_as_current_span("search_request") as span:
        span.set_attribute("algorithm", algorithm)
        span.set_attribute("pattern.length", len(pattern))

        # ── 1. Leitura do arquivo ──────────────────────────
        with tracer.start_as_current_span("load_document"):
            try:
                content_bytes = await file.read()
                text = content_bytes.decode("utf-8", errors="replace")
            except Exception as e:
                raise HTTPException(status_code=422, detail=f"Erro ao ler arquivo: {e}")
            span.set_attribute("document.size_chars", len(text))

        logger.info(
            "Iniciando busca",
            extra={
                "algorithm": ALGO_LABELS.get(algorithm, algorithm),
                "n": len(text),
                "m": len(pattern),
            },
        )

        # ── 2. Execução do algoritmo ───────────────────────
        with tracer.start_as_current_span("execute_algorithm") as alg_span:
            alg_span.set_attribute("algorithm", algorithm)
            result = strategy.execute(text, pattern)

        # ── 3. Telemetria ──────────────────────────────────
        record_search(
            algorithm=algorithm,
            found=result.found,
            duration_ms=result.duration_ms,
            n=result.n,
            m=result.m,
        )

        logger.info(
            "Busca concluída",
            extra={
                "duration_ms": result.duration_ms,
                "occurrences": result.occurrences,
                "found": result.found,
            },
        )

        # ── 4. Formatar resposta ───────────────────────────
        with tracer.start_as_current_span("format_response"):
            # Limit positions to 500 to keep response small
            positions_out = result.positions[:500]

        return {
            "found": result.found,
            "occurrences": result.occurrences,
            "positions": positions_out,
            "positions_truncated": len(result.positions) > 500,
            "duration_ms": result.duration_ms,
            "n": result.n,
            "m": result.m,
            "algorithm": algorithm,
            "algorithm_label": ALGO_LABELS.get(algorithm, algorithm),
        }
