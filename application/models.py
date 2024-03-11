from pydantic import BaseModel

class TodoItem(BaseModel):
    name: str
    completed: bool = False
