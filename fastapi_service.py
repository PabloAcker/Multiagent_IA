#```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Model for incoming data
class Item(BaseModel):
    name: str
    value: int
    description: str = ''

# In-memory storage for demonstration purposes
items = {}

@app.post('/items/', response_model=Item)
async def create_item(item: Item):
    """Create a new item. If the item already exists, raise an HTTP exception."""
    if item.name in items:
        raise HTTPException(status_code=400, detail='Item already exists')
    items[item.name] = item
    return item

@app.get('/items/{item_name}', response_model=Item)
async def read_item(item_name: str):
    """Retrieve an item by its name. Raise HTTP 404 if not found."""
    if item_name not in items:
        raise HTTPException(status_code=404, detail='Item not found')
    return items[item_name]

@app.get('/items/', response_model=list[Item])
async def read_items():
    """Retrieve a list of all items."""
    return list(items.values())

@app.delete('/items/{item_name}', response_model=Item)
async def delete_item(item_name: str):
    """Delete an item by its name. Raise HTTP 404 if not found."""
    if item_name not in items:
        raise HTTPException(status_code=404, detail='Item not found')
    return items.pop(item_name)
# ```
# To run this FastAPI application, save the code to a file named `main.py` and start the server with the command:
# ```bash
# uvicorn main:app --reload
# ```
# You can then access the API documentation at `http://127.0.0.1:8000/docs`. This service provides a simple API to create, read, delete, and list items, which can be expanded as needed.