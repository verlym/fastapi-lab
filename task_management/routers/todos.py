from typing import Annotated, List
from uuid import UUID  # Import UUID for type hinting

from fastapi import APIRouter, Depends, Path, status  # Import APIRouter, Depends
from repositories import TodoRepository  # Only for Dependency Injection
from schemas import TodoCreate, TodoResponse, TodoUpdate  # Import Pydantic schemas
from services import TodoService  # Import TodoService

router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
)


def get_todo_service() -> TodoService:
    repo = TodoRepository()
    service = TodoService(repo)
    return service


# CREATE (POST)
@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo_endpoint(
    todo_create: TodoCreate,  # Request body uses TodoCreate schema
    service: Annotated[TodoService, Depends(get_todo_service)],  # Inject TodoService
):
    """**Create Todo:** Adds a new todo item.
    - Accepts `TodoCreate` schema as request body.
    - Returns `201 Created` and the created `TodoResponse`.
    """
    todo = service.create_todo(todo_create)
    return TodoResponse.model_validate(todo.to_dict())  # Convert core model to response schema


# READ All (GET)
@router.get("/", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
async def get_all_todos_endpoint(service: Annotated[TodoService, Depends(get_todo_service)]):
    """**Get All Todos:** Retrieves a list of all available todo items.
    - Returns a list of `TodoResponse` objects.
    """
    todos = service.get_all_todos()
    return [TodoResponse.model_validate(todo.to_dict()) for todo in todos]  # Convert core models to response schemas


# UPDATE (PUT)
@router.put("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def update_todo_endpoint(
    todo_id: Annotated[UUID, Path(description="The UUID of the todo item to update.")],
    todo_update: TodoUpdate,  # Request body uses TodoUpdate schema
    service: Annotated[TodoService, Depends(get_todo_service)],
):
    """**Update Todo:** Updates an existing todo item's details.
    - Returns `200 OK` and the updated `TodoResponse`.
    - Returns `404 Not Found` if the todo does not exist.
    """
    todo = service.update_todo(todo_id, todo_update)
    return TodoResponse.model_validate(todo.to_dict())


# DELETE (DELETE)
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_endpoint(
    todo_id: Annotated[UUID, Path(description="The UUID of the todo item to delete.")],
    service: Annotated[TodoService, Depends(get_todo_service)],
):
    """**Delete Todo:** Deletes a specific todo item by its UUID.
    - Returns `204 No Content` on successful deletion.
    - Returns `404 Not Found` if the todo does not exist.
    """
    service.delete_todo(todo_id)
    return  # 204 No Content returns no body
