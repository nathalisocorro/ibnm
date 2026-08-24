from fastapi import FastAPI
from app.api.routes import router
from app.db import models
from contextlib import asynccontextmanager
import asyncio
from app.messaging.kafka_consumer import consume_policy_proposed

@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer_task = asyncio.create_task(
        consume_policy_proposed()
    )

    yield

    consumer_task.cancel()

    try:
        await consumer_task
    except asyncio.CancelledError:
        pass

app = FastAPI(
    title="MS-P04 Logical Task Management",
    version="0.1.0",
    description="Microservicio para la gestión de tareas lógicas del proyecto IBNM.",
    lifespan=lifespan
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