from fastapi import FastAPI, Security, HTTPException, Depends
from .models import TodoItem, TodoCreate, get_next_id
from .utils import VerifyToken 
from typing import List

app = FastAPI()
auth = VerifyToken() # Get a new instance

# Simulated database
db: List[TodoItem] = []

@app.get("/api/todos/")
def get_todos():
    return db



@app.post("/api/todos/", response_model=TodoItem, dependencies=[Depends(auth.verify)])
def create_todo(todo: TodoCreate):
    new_todo = TodoItem(id=get_next_id(db), **todo.model_dump())
    db.append(new_todo)
    return new_todo

@app.put("/api/todos/{todo_id}", dependencies=[Depends(auth.verify)])
def update_todo(todo_id: int, todo: TodoCreate):
    # Find the index of the todo item by id
    index = next((i for i, item in enumerate(db) if item.id == todo_id), None)
    
    if index is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Create a new TodoItem with the same id but updated data
    updated_todo = TodoItem(id=todo_id, **todo.model_dump())
    
    # Replace the old todo item with the updated one
    db[index] = updated_todo
    
    return updated_todo

from fastapi import HTTPException, Depends

@app.delete("/api/todos/{todo_id}", dependencies=[Depends(auth.verify)])
def delete_todo(todo_id: int):
    # Find the index of the todo item by id
    index = next((i for i, item in enumerate(db) if item.id == todo_id), None)
    
    if index is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Remove the todo item from the db list by index
    db.pop(index)
    return {"message": "Todo deleted successfully"}


@app.get("/api/access-token")
def public():
    return auth.get_access_token()

@app.get("/api/private")
def private(auth_result: str = Security(auth.verify)):
    return {"status": "success", "msg": "Hello from a private endpoint! You need to be authenticated to see this.", "data": auth_result}



