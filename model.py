import datetime

from pydantic import BaseModel


class TaskBody(BaseModel):
    name: str
    hasDone: bool
    dueDate: datetime.date
    priority: int