from beanie import Document
import datetime


class Task(Document):
    name: str
    hasDone: bool
    dueDate: datetime.date
    priority: int

    class Settings:
        bson_encoders = {
            datetime.date: lambda o: datetime.datetime.combine(
                o, datetime.datetime.min.time()
            )
        }