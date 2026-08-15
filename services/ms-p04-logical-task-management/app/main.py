from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="MS-P04 Logical Task Management",
    version="0.1.0",
    description="Microservicio inicial para la gestión de tareas lógicas del proyecto IBNM.",
)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "ms-p04-logical-task-management",
    }

app.include_router(router)