from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from db import Task
from model import TaskBody
from typing import List, Dict, Union

app = FastAPI()

@app.on_event('startup')
async def connect_db():
    client = AsyncIOMotorClient('mongodb://localhost:27017')

    await init_beanie(database=client.god, document_models=[Task])

@app.get('/')
def hello_world() -> str:
    print("I am hereee")
    return "hello_world"

@app.post('/task', status_code=201)
async def create_task(task_body: TaskBody) -> Dict[str, str]:
    task = Task(**task_body.model_dump())
    await task.insert()
    return {
        "message": f"Task {task.name} create successfully"
    }

@app.get('/task')
async def view_all_task() -> Dict[str, List[Task]]:
    all_task = await Task.find().to_list()
    return {
        "task": all_task
    }

@app.get('/task/{ids}')
async def get_task(ids: str) -> Union[Task, Dict[str, str]]:
    try:
        return await Task.get(ids)
    except Exception as e:
        return {
            "message": "Task not found"
        }
    
@app.put('/task/{ids}', status_code=202)
async def update_task(ids: str, task_body: TaskBody) -> Dict[str, str]:
    task = await Task.get(ids)
    task.name = task_body.name
    task.hasDone = task_body.hasDone
    task.dueDate = task_body.dueDate
    task.priority = task_body.priority
    await task.save()
    return {
        "message": f"Task {task.id} updated successfully"
    }

@app.delete('/task/{ids}')
async def delete_task(ids: str) -> Dict[str, str]:
    task = await Task.get(ids)
    await task.delete()
    return {
        "message": f"Task {task.id} deleted successfully"
    }
