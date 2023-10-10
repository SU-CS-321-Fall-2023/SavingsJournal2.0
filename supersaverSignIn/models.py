from pydantic import BaseModel, ValidationError
from typing import Optional, List

class Goal(BaseModel):  # each goal will have the username
    title: str
    amount: int
    deadline: str
    notes: Optional[str] = None
    username: str
    # status: str


class User(BaseModel):
    username: str
    email: Optional[str] = None
    password: str
    goals: Optional[List] = None  # goals as jsons