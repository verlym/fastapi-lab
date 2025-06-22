from typing import Annotated, Optional

from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field

# --- In-Memory Databases/Data for Demo ---
in_memory_products_db = {
    1: {
        "id": 1,
        "name": "Laptop",
        "price": 1200.0,
        "description": "Powerful gaming laptop",
        "tax": 10.0,
        "is_available": True,
        "tags": ["electronics", "gaming"],
    },
    2: {
        "id": 2,
        "name": "Mouse",
        "price": 25.0,
        "description": "Wireless ergonomic mouse",
        "tax": 5.0,
        "is_available": True,
        "tags": ["electronics"],
    },
}
next_product_id = 3  # Start IDs from 3 as 1 and 2 are pre-filled

in_memory_users_db = {
    101: {"id": 101, "username": "alice_dev", "email": "alice@example.com", "password_hash": "hashed_alice_pw"},
    102: {"id": 102, "username": "bob_tester", "email": "bob@example.com", "password_hash": "hashed_bob_pw"},
}


# Model Pydantic (Schema)
class ProductInput(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Name of the product")
    description: Optional[str] = Field(None, max_length=250, description="Optional Description")
    price: float = Field(..., gt=0, description="Price of the product, must be greater than 0")
    tax: Optional[float] = Field(None, ge=0, le=100, description="tax percentage")
    is_available: bool = Field(True, description="Status availability (default true)")
    tags: list[str] = Field([], description="List of tags for the product")


class UserRegistration(BaseModel):
    username: str = Field(
        ...,  # mandatory
        min_length=3,
        max_length=20,
        pattern="^[a-zA-Z0-9_]+$",  # Hanya huruf, angka, underscore
        description="Username must be alphanumeric with underscores, 3-20 chars.",
    )
    email: str = Field(..., description="User's email address.")
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long.")
    age: Optional[int] = Field(
        None,
        ge=18,  # Greater than or equal to 18
        le=120,  # Less than or equal to 120
        description="User's age, must be between 18 and 120 (optional).",
    )
    is_subscribed: bool = Field(False, description="Subscription status (default False).")


# Model untuk Response (Product detail, untuk memastikan output konsisten)
class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    is_available: bool = True
    tags: list[str] = []  # Pastikan tipe default cocok jika field optional

    # Pydantic's behaviour to serialize from ORM/dict-like objects
    class Config:
        from_attributes = True  # for Pydantic v2. For Pydantic v1, use orm_mode = True


# Model untuk Response (Public User Profile, menyembunyikan info sensitif)
class UserPublicResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True  # for Pydantic v2. For Pydantic v1, use orm_mode = True


app = FastAPI(
    title="Pydantic Implementation Demo",
    description="Exploring Pydantic models for request bodies, advanced validation, "
    "form data, response models, and non-JSON responses.",
    version="0.1.0",
    docs_url="/documentation",
    redoc_url="/redoc-api-docs",
)


@app.post("/products/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def create_product(product_input: ProductInput):
    """**Create Product:** Membuat produk baru.
    - Menerima `ProductInput` sebagai request body (JSON).
    - Otomatis memvalidasi dan mem-parse JSON menjadi objek Python.
    - Mengembalikan `201 Created` dan objek `ProductResponse`.
    """
    global next_product_id
    product_id = next_product_id

    new_product_data = product_input.model_dump()
    new_product_data["id"] = product_id
    # insert data to database
    in_memory_products_db[product_id] = new_product_data
    next_product_id += 1

    return ProductResponse(**new_product_data)


@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: Annotated[int, Path(ge=1)], product_input: ProductInput):
    """**Update Product:** Memperbarui detail produk.
    - Menerima `product_id` sebagai path parameter (integer).
    - Menerima `ProductInput` sebagai request body (JSON).
    - Memvalidasi dan mem-parse JSON menjadi objek Python.
    - Mengembalikan `200 OK` dengan objek `ProductResponse` yang diperbarui.
    """
    if product_id not in in_memory_products_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Update data produk di "database"
    updated_data = product_input.model_dump(exclude_unset=True)  # Hanya update field yang disertakan di request
    in_memory_products_db[product_id].update(updated_data)

    # Return ProductResponse untuk konsistensi output
    return ProductResponse(**in_memory_products_db[product_id])


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """**Get Product:** Mengambil detail produk berdasarkan ID.
    - Menerima `product_id` sebagai path parameter (integer).
    - Mengembalikan `200 OK` dengan objek `ProductResponse`.
    """
    if product_id not in in_memory_products_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return ProductResponse(**in_memory_products_db[product_id])
