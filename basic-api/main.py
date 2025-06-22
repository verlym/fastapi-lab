from typing import Annotated, Optional
from fastapi import FastAPI, Path, Query, status, HTTPException

#simulasi database
fake_db = {
    "items": {
        1: {"name": "Laptop", "price": 1200},
        2: {"name": "Mouse", "price": 25},
        3: {"name": "Keyboard", "price": 75},
    },
    "users": {
        101: {"username": "alice", "email": "alice@example.com"},
        102: {"username": "bob", "email": "bob@example.com"},
    }
}

app = FastAPI(
    title="FastAPI Simple App",
    description="A simple FastAPI application to demonstrate core endpoint.",
    version="0.1.0",
    docs_url="/swagger", #docs
    redoc_url="/redoc",
)

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict: A dictionary with a welcome message.
    """
    return {"message": "Hello, Verly!"}

@app.get("/status", status_code=status.HTTP_200_OK)
async def get_api_status():
    """
    Get the status of the API.

    Returns:
        dict: A dictionary indicating that the API is up and running.
    """
    return {"status": "up", "version": app.version}

@app.get("/data", status_code=status.HTTP_200_OK)
async def get_data():
    """
    Get data from the fake database.

    Returns:
        dict: A dictionary containing the data from the fake database.
    """
    return fake_db

#Path Parameter
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int):
    """
    Get user information by user ID.

    Args:
        user_id (int): The unique identifier of the user.

    Returns:
        dict: A dictionary containing user information.
    """
    user = fake_db["users"].get(user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.get("/items/{item_id_str}", status_code=status.HTTP_200_OK)
async def get_item_by_string_id(item_id_str: str):
    """
    Get item information by item ID (string).

    Args:
        item_id_str (str): The string representation of the item ID.

    Returns:
        dict: A dictionary containing item information.
    """
    item_id = int(item_id_str)
    item = fake_db["items"].get(item_id)
    if item:
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    

@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(
    product_id: Annotated[int, Path(
        title="Id of product",
        description="Must be an integer between 1 - 100",
        ge=1,
        le=100
    )]
):
    item = fake_db["items"].get(product_id)
    if item:
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


#Query Parameter

@app.get("/search-products/", status_code=status.HTTP_200_OK)
async def search_product(
    query: str,
    limit: Optional[str],
    skip: Annotated[int, Query(description="Number of items to skip for pagination", ge=0)] = 0,
    exact_match: bool = False
):
    """
    Search for products based on a query.

    Args:
        query (str): The search query.
        limit (Optional[str]): The maximum number of results to return.
        skip (Annotated[int, Query(description="Number of items to skip for pagination", ge=0)]): The number of items to skip for pagination.
        exact_match (bool): Whether to perform an exact match search.

    Returns:
        dict: A dictionary containing the search results.
    """
    search_results = {}
    for item_id, item in fake_db["items"].items():
        if query in item["name"]:
            search_results[item_id] = item
    return {"query": query, "limit": limit, "skip": skip, "exact_match": exact_match, "results": search_results}