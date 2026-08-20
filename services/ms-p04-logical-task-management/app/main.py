from fastapi import FastAPI
from app.api.routes import router
from app.db.database import Base, engine
from app.db import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MS-P04 Logical Task Management",
    version="0.1.0",
    description="Microservicio inicial para la gestión de tareas lógicas del proyecto IBNM.",
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=6300,
        reload=True
    )