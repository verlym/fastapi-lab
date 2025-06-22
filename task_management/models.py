import uuid
from datetime import date
from typing import Optional


class Todo:
    """Represents a core Todo item within our application's business logic.
    This is separate from Pydantic schemas which are for API input/output.
    """

    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        completed: bool = False,
        priority: int = 3,  # 1=High, 2=Medium, 3=Low
        due_date: Optional[date] = None,
        # Generate a unique ID if not provided (for new todos)
        id: Optional[uuid.UUID] = None,
    ):
        self.id: uuid.UUID = id if id else uuid.uuid4()
        self.title = title
        self.description = description
        self.completed = completed
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        """Converts the Todo object to a dictionary, useful for storage and Pydantic conversion."""
        return {
            "id": str(self.id),  # Convert UUID to string for easy JSON serialization
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
        }

    @staticmethod
    def from_dict(data: dict):
        """Creates a Todo object from a dictionary."""
        return Todo(
            id=uuid.UUID(data["id"]) if "id" in data and data["id"] else None,
            title=data["title"],
            description=data.get("description"),
            completed=data.get("completed", False),
            priority=data.get("priority", 3),
            due_date=date.fromisoformat(data["due_date"]) if data.get("due_date") else None,
        )
