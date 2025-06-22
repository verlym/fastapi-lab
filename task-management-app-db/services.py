# app/services.py
from typing import Dict, List  # Import List dan Dict untuk type hints   

from fastapi import HTTPException, status  # Untuk menangani HTTP errors

from models import Task  # Database Task model
from repositories import TaskRepository  # Repository kita
from schemas import TaskCreate, TaskRead, TaskUpdate  # Schema untuk API


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(self, task_data: TaskCreate) -> TaskRead:
        """Membuat tugas baru dan menyimpannya ke database."""
        print(f"[DEBUG] --> Service: Creating task: {task_data.title}")
        new_task = Task.model_validate(task_data.model_dump()) # Konversi schema ke DB model
        task_in_db = await self.repository.create(new_task)
        return TaskRead.model_validate(task_in_db.model_dump()) # Konversi DB model ke response schema

    async def get_all_tasks(self) -> List[TaskRead]:
        """Mengambil semua tugas."""
        print("[DEBUG] --> Service: Getting all tasks.")
        tasks = await self.repository.get_all()
        return [TaskRead.model_validate(task.model_dump()) for task in tasks]

    async def get_task_by_id(self, task_id: int) -> TaskRead:
        """Mengambil tugas berdasarkan ID, atau raises 404 jika tidak ditemukan."""
        print(f"[DEBUG] --> Service: Getting task by ID: {task_id}")
        task = await self.repository.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found."
            )
        return TaskRead.model_validate(task.model_dump())

    async def update_task(self, task_id: int, task_update_data: TaskUpdate) -> TaskRead:
        """Memperbarui tugas yang sudah ada, atau raises 404 jika tidak ditemukan."""
        print(f"[DEBUG] --> Service: Updating task ID: {task_id}")
        task_in_db = await self.repository.get_by_id(task_id)
        if not task_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found."
            )
        updated_task = await self.repository.update(task_in_db, Task.model_validate(task_update_data.model_dump(exclude_unset=True)))
        return TaskRead.model_validate(updated_task.model_dump())

    async def delete_task(self, task_id: int) -> Dict[str, str]:
        """Menghapus tugas, atau raises 404 jika tidak ditemukan."""
        print(f"[DEBUG] --> Service: Deleting task ID: {task_id}")
        task_in_db = await self.repository.get_by_id(task_id)
        if not task_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found."
            )
        await self.repository.delete(task_in_db)
        return {"message": f"Task with ID {task_id} deleted successfully."}