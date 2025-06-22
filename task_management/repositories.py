from typing import Dict, List, Optional
from uuid import UUID

from models import Todo

# Simulasi database in-memory
# Kunci adalah UUID, nilai adalah objek Todo
_in_memory_todos_db: Dict[UUID, Todo] = {}

# Inisialisasi beberapa data dummy
initial_todos = [
    Todo(
        title="Learn Project Structure",
        description="Understand schemas, models, services, and repositories.",
        completed=False,
        priority=1,
    ),
    Todo(
        title="Implement CRUD Operations",
        description="Apply CREATE, READ, UPDATE, DELETE to the Todo app.",
        completed=False,
        priority=2,
    ),
    Todo(
        title="Explore Error Handling",
        description="Learn how to raise and handle HTTPExceptions.",
        completed=False,
        priority=3,
    ),
]
for todo in initial_todos:
    _in_memory_todos_db[todo.id] = todo


class TodoRepository:
    """Handles direct data access operations for Todo items.
    It interacts with the in-memory database directly.
    """

    # SELECT *
    def get_all(self) -> List[Todo]:
        return list(_in_memory_todos_db.values())

    # SELECT * FROM TABLE WHERE TODO_ID = blablabla
    def get_by_id(self, todo_id: UUID) -> Optional[Todo]:
        return _in_memory_todos_db.get(todo_id)

    # INSERT INTO
    def add(self, todo: Todo) -> Todo:
        # insert
        _in_memory_todos_db[todo.id] = todo
        return todo

    def update(self, todo_id: UUID, updated_data: Dict) -> Optional[Todo]:
        if todo_id not in _in_memory_todos_db:
            return None

        existing_todo = _in_memory_todos_db[todo_id]
        for key, value in updated_data.items():
            if hasattr(existing_todo, key):
                setattr(existing_todo, key, value)
        return existing_todo

    def delete(self, todo_id: UUID) -> bool:
        if todo_id in _in_memory_todos_db:
            del _in_memory_todos_db[todo_id]
            return True
        return False
