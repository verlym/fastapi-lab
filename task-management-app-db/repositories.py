# app/repositories.py
from datetime import datetime
from typing import List, Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession  # Pastikan ini AsyncSession

from models import Task  # Import model Task kita


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task_data: Task) -> Task:
        """Menambahkan tugas baru ke database."""
        print(f"[DEBUG] --> Repository: Creating task with title: {task_data.title}")
        self.session.add(task_data) # Menambahkan objek Task ke session
        await self.session.commit() # Menyimpan perubahan ke database
        await self.session.refresh(task_data) # Memuat ulang objek dengan ID yang dihasilkan database
        return task_data

    async def get_all(self) -> List[Task]:
        """Mengambil semua tugas dari database."""
        print("[DEBUG] --> Repository: Getting all tasks.")
        statement = select(Task) # Membuat query untuk memilih semua Task
        results = await self.session.exec(statement) # Mengeksekusi query secara asynchronous
        tasks = list(results.all()) # Mengambil semua hasil
        return tasks

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        """Mengambil tugas berdasarkan ID."""
        print(f"[DEBUG] --> Repository: Getting task with ID: {task_id}")
        statement = select(Task).where(Task.id == task_id) # Query dengan kondisi WHERE
        result = await self.session.exec(statement)
        task = result.first() # Mengambil hasil pertama
        return task

    async def update(self, task: Task, task_update_data: Task) -> Task:
        """Memperbarui tugas yang sudah ada."""
        print(f"[DEBUG] --> Repository: Updating task with ID: {task.id}")
        # Mengisi data dari task_update_data ke objek task yang sudah ada
        for key, value in task_update_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        task.updated_at = datetime.now() # Update timestamp
        self.session.add(task) # 'add' juga digunakan untuk update di SQLModel
        await self.session.commit()
        await self.session.refresh(task) # Memuat ulang untuk memastikan data terbaru
        return task

    async def delete(self, task: Task) -> None:
        """Menghapus tugas dari database."""
        print(f"[DEBUG] --> Repository: Deleting task with ID: {task.id}")
        await self.session.delete(task) # Menghapus objek dari session
        await self.session.commit() # Menyimpan perubahan ke database