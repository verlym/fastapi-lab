from fastapi import FastAPI
from routers import todos

app = FastAPI(
    title="Task Management App",
    description="A Simple Task Management/Todo App",
    version="1.0.0",
    docs_url="/documentation",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Management App!"}


@app.get("/health")
def health_check():
    return {"status": "ok", "version": app.version}


app.include_router(todos.router)
