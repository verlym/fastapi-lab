# app/routers/tasks.py
from typing import Annotated, Dict, List  # Import Dict dan Annotated

from fastapi import APIRouter, Depends, status  # Import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession  # Untuk get_session

from database import get_session  # Dependency function untuk DB session
from repositories import TaskRepository  # Repository kita
from schemas import TaskCreate, TaskRead, TaskUpdate  # Schemas kita
from services import TaskService  # Service kita

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# --- Dependency Functions (untuk TaskService) ---

# Dependency yang menyediakan TaskRepository
# Ia bergantung pada get_session untuk mendapatkan database session
async def get_task_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> TaskRepository:
    print("\n[DEBUG] --> DI Step: Providing TaskRepository instance.")
    return TaskRepository(session=session)

# Dependency yang menyediakan TaskService
# Ia bergantung pada get_task_repository untuk mendapatkan repository
async def get_task_service(
    repository: Annotated[TaskRepository, Depends(get_task_repository)]
) -> TaskService:
    print("[DEBUG] --> DI Step: Providing TaskService instance.")
    return TaskService(repository=repository)

# --- Task Endpoints (CRUD Operations) ---

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task_create: TaskCreate,
    service: Annotated[TaskService, Depends(get_task_service)] # Suntikkan TaskService
):
    """Membuat tugas baru.
    """
    print(f"\n[DEBUG] --> Endpoint: Creating new task with title: {task_create.title}")
    return await service.create_task(task_create)

@router.get("/", response_model=List[TaskRead])
async def get_all_existing_tasks(
    service: Annotated[TaskService, Depends(get_task_service)] # Suntikkan TaskService
):
    """Mengambil semua tugas yang ada.
    """
    print("\n[DEBUG] --> Endpoint: Getting all tasks.")
    return await service.get_all_tasks()

@router.get("/{task_id}", response_model=TaskRead)
async def get_existing_task_by_id(
    task_id: int,
    service: Annotated[TaskService, Depends(get_task_service)] # Suntikkan TaskService
):
    """Mengambil tugas berdasarkan ID.
    """
    print(f"\n[DEBUG] --> Endpoint: Getting task by ID: {task_id}")
    return await service.get_task_by_id(task_id)

@router.put("/{task_id}", response_model=TaskRead)
async def update_existing_task(
    task_id: int,
    task_update: TaskUpdate,
    service: Annotated[TaskService, Depends(get_task_service)] # Suntikkan TaskService
):
    """Memperbarui tugas yang sudah ada.
    """
    print(f"\n[DEBUG] --> Endpoint: Updating task with ID: {task_id}")
    return await service.update_task(task_id, task_update)

@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
async def delete_existing_task(
    task_id: int,
    service: Annotated[TaskService, Depends(get_task_service)] # Suntikkan TaskService
) -> Dict[str, str]: # Mengembalikan Dict untuk pesan sukses
    """Menghapus tugas.
    """
    print(f"\n[DEBUG] --> Endpoint: Deleting task with ID: {task_id}")
    return await service.delete_task(task_id)