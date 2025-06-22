from typing import List
from uuid import UUID

from fastapi import HTTPException, status  # Untuk raise HTTPExceptions
from models import Todo  # Import core Todo model
from repositories import TodoRepository  # Import TodoRepository
from schemas import TodoCreate, TodoUpdate  # Import Pydantic schemas


class TodoService:
    """Handles the business logic for Todo items.
    It orchestrates operations by interacting with the TodoRepository.
    """

    def __init__(self, repository: TodoRepository):
        self.repository = repository

    def get_all_todos(self) -> List[Todo]:
        """Retrieves all Todo items."""
        return self.repository.get_all()

    def get_todo_by_id(self, todo_id: UUID) -> Todo:
        """Retrieves a single Todo item by its ID.
        Raises HTTPException if the todo is not found.
        """
        todo = self.repository.get_by_id(todo_id)
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID {todo_id} not found.")
        return todo

    def create_todo(self, todo_create: TodoCreate) -> Todo:
        """Creates a new Todo item."""
        # Convert Pydantic schema to core Todo model
        new_todo = Todo(
            title=todo_create.title,
            description=todo_create.description,
            priority=todo_create.priority,
            due_date=todo_create.due_date,
        )
        return self.repository.add(new_todo)

    def update_todo(self, todo_id: UUID, todo_update: TodoUpdate) -> Todo:
        """Updates an existing Todo item.
        Raises HTTPException if the todo is not found.
        """
        existing_todo = self.repository.get_by_id(todo_id)
        if not existing_todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID {todo_id} not found.")

        # Convert Pydantic TodoUpdate schema to a dictionary of provided fields
        # Pydantic v2: todo_update.model_dump(exclude_unset=True)
        # Pydantic v1: todo_update.dict(exclude_unset=True)
        updated_data = todo_update.model_dump(exclude_unset=True)

        # Perform the update via repository
        updated_todo = self.repository.update(todo_id, updated_data)
        if not updated_todo:  # Should not happen if get_by_id already passed
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update todo.")
        return updated_todo

    def delete_todo(self, todo_id: UUID) -> None:
        """Deletes a Todo item.
        Raises HTTPException if the todo is not found.
        """
        if not self.repository.delete(todo_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID {todo_id} not found.")
