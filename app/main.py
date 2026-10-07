from fastapi import FastAPI
from app.observability.tracing import setup_tracing
app = FastAPI(
    title="Enterprise MCP Tool Gateway",
    description="Enterprise MCP Tool Gateway and Evaluation Platform",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "project": "Enterprise MCP Tool Gateway",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }