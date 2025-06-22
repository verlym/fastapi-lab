from datetime import date
from typing import Literal, Optional

from pydantic import UUID4, BaseModel, Field  # UUID4 for Pydantic type hint for UUID


# Schema for creating a new Todo item (Request Body for POST)
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Title of the todo item")
    description: Optional[str] = Field(None, max_length=500, description="Optional detailed description of the todo")
    priority: Literal[1, 2, 3] = Field(3, description="Priority of the todo: 1 (High), 2 (Medium), 3 (Low)")
    due_date: Optional[date] = Field(None, description="Optional due date for the todo (YYYY-MM-DD format)")

    # Example for documentation
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, coffee beans",
                "priority": 1,
                "due_date": "2025-07-01",
            }
        }


# Schema for updating an existing Todo item (Request Body for PUT/PATCH)
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100, description="New title of the todo item")
    description: Optional[str] = Field(None, max_length=500, description="New detailed description of the todo")
    completed: Optional[bool] = Field(None, description="New completion status of the todo item")
    priority: Optional[Literal[1, 2, 3]] = Field(None, description="New priority of the todo")
    due_date: Optional[date] = Field(None, description="New due date for the todo (YYYY-MM-DD format)")

    # Example for documentation
    class Config:
        json_schema_extra = {"example": {"title": "Finish Project Report", "completed": True, "priority": 1}}


# Schema for Todo item responses (includes 'id' and matches core Todo model attributes)
class TodoResponse(BaseModel):
    id: UUID4  # Pydantic type for UUID
    title: str
    description: Optional[str] = None
    completed: bool
    priority: Literal[1, 2, 3]
    due_date: Optional[date]

    # Pydantic v2: To allow the model to be created from attributes of an object (e.g., ORM models) or dictionaries.
    # Pydantic v1: Use 'orm_mode = True'
    class Config:
        from_attributes = True
