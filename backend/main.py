from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# ==========================
# Load Environment Variables
# ==========================
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
frontend_directory = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase credentials not found in .env file")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ==========================
# FastAPI App
# ==========================
app = FastAPI(
    title="ToDo API",
    description="FastAPI + Supabase ToDo App",
    version="1.0.0"
)

# ==========================
# CORS
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# Pydantic Models
# ==========================

class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


# ==========================
# Health Check
# ==========================

@app.get("/")
def root():
    return FileResponse(os.path.join(frontend_directory, "index.html"))


# ==========================
# Get All Tasks
# ==========================

@app.get("/tasks")
def get_tasks():
    try:
        response = (
            supabase
            .table("tasks")
            .select("*")
            .order("id")
            .execute()
        )

        return response.data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================
# Get Single Task
# ==========================

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    try:
        response = (
            supabase
            .table("tasks")
            .select("*")
            .eq("id", task_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return response.data[0]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================
# Create Task
# ==========================

@app.post("/tasks")
def create_task(task: TaskCreate):
    try:
        response = (
            supabase
            .table("tasks")
            .insert({
                "title": task.title,
                "completed": False
            })
            .execute()
        )

        return {
            "message": "Task created successfully",
            "data": response.data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================
# Update Task
# ==========================

@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task: TaskUpdate
):
    try:

        update_data = {}

        if task.title is not None:
            update_data["title"] = task.title

        if task.completed is not None:
            update_data["completed"] = task.completed

        response = (
            supabase
            .table("tasks")
            .update(update_data)
            .eq("id", task_id)
            .execute()
        )

        return {
            "message": "Task updated successfully",
            "data": response.data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================
# Mark Completed
# ==========================

@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    try:
        response = (
            supabase
            .table("tasks")
            .update({
                "completed": True
            })
            .eq("id", task_id)
            .execute()
        )

        return {
            "message": "Task marked as completed",
            "data": response.data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================
# Delete Task
# ==========================

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        response = (
            supabase
            .table("tasks")
            .delete()
            .eq("id", task_id)
            .execute()
        )

        return {
            "message": "Task deleted successfully",
            "data": response.data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


app.mount("/", StaticFiles(directory=frontend_directory, html=True), name="frontend")


# ==========================
# Run Application
# ==========================
# uvicorn main:app --reload