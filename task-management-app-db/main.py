from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_db_and_tables  # Fungsi untuk membuat tabel
from routers import tasks  # Router tasks kita


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n[DEBUG] --> FastAPI App: Startup event - Creating database tables...")
    await create_db_and_tables()
    print("[DEBUG] --> FastAPI App: Startup complete.")
    yield
    print("\n[DEBUG] --> FastAPI App: Shutdown event - Application shutting down.")

app = FastAPI(
    title="Simple Task Management App using DB",
    version="1.0.0",
    description="Task Management App using DB",
    lifespan=lifespan
)

app.include_router(tasks.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Task Management API! Go to /docs for Swagger UI."}