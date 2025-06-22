# app/database.py
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from config import DATABASE_URL  # Import DATABASE_URL dari config.py

# Membuat async engine untuk koneksi database
# echo=True akan mencetak semua SQL yang dihasilkan oleh SQLModel ke konsol
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Membuat factory untuk AsyncSession
# class_=AsyncSession: memastikan kita mendapatkan asynchronous session
# expire_on_commit=False: penting untuk ORM async, objek tidak perlu di-refresh setelah commit
AsyncSessionLocal = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# Fungsi ini akan membuat tabel di database berdasarkan SQLModel kita
async def create_db_and_tables():
    print("[DEBUG] --> Database: Creating tables if they don't exist...")
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("[DEBUG] --> Database: Tables created/verified.")

# Fungsi dependency untuk mendapatkan AsyncSession
# Ini akan dipanggil oleh FastAPI untuk setiap request yang membutuhkannya
# Menggunakan 'yield' untuk memastikan session dibuka dan ditutup dengan rapi
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        print("\n[DEBUG] --> DB Session: Opened for a new request.")
        try:
            yield session # Menyediakan session ke endpoint/service
        finally:
            await session.close() # Menutup session setelah request selesai
            print("[DEBUG] --> DB Session: Closed.")