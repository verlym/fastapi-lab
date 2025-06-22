# app/schemas.py
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel  # Import SQLModel juga di sini karena schemas berasal dari models


# Base schema untuk Task, berisi field yang umum
class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False # Default untuk pembuatan

# Schema untuk membuat Task (POST request)
# Ini mewarisi dari TaskBase dan tidak menambahkan field baru
class TaskCreate(TaskBase):
    pass

# Schema untuk membaca Task (GET response)
# Ini mewarisi dari TaskBase dan menambahkan field yang dibuat oleh database (id, timestamps)
class TaskRead(TaskBase):
    id: int
    completed: bool = False # Pastikan ini tidak Optional untuk response
    created_at: datetime
    updated_at: Optional[datetime]

# Schema untuk memperbarui Task (PUT/PATCH request)
# Semua field bersifat opsional karena kita mungkin hanya ingin memperbarui sebagian
class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    updated_at: Optional[datetime] = None # Akan diisi otomatis di service/repo