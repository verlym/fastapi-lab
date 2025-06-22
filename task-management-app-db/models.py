# app/models.py
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel  # Import dari sqlmodel


# Model Task kita, merepresentasikan tabel 'task' di database
class Task(SQLModel, table=True): # table=True berarti ini akan dipetakan ke database table
    id: Optional[int] = Field(default=None, primary_key=True) # Unique ID, auto-incremented
    title: str = Field(index=True) # Judul tugas, akan diindeks untuk pencarian cepat
    description: Optional[str] = Field(default=None) # Optional description
    completed: bool = Field(default=False) # Task status, defaultnya belum selesai
    created_at: datetime = Field(default_factory=datetime.now) # Creation timestamp, defaultnya waktu sekarang
    updated_at: Optional[datetime] = Field(default_factory=datetime.now) # Update timestamp, akan diupdate