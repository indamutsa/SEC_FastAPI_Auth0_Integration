from pydantic import BaseModel

class TodoCreate(BaseModel):
    name: str
    completed: bool = False

class TodoItem(TodoCreate):
    id: int

def get_next_id(db):
    """Generate a new ID for a todo item."""
    return max([item.id for item in db], default=0) + 1