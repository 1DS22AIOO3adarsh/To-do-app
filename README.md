# To-Do App

A simple full-stack To-Do application built with a FastAPI backend, Supabase database, and HTML/CSS/JavaScript frontend.

## Features

- Create tasks
- View all tasks
- Mark tasks as completed
- Edit tasks
- Delete tasks
- Store tasks in Supabase
- Serve the frontend through FastAPI

## Project Structure

- `main.py` - FastAPI application and API routes
- `requirements.txt` - Backend dependencies
- `.env` - Supabase credentials
- `index.html` - Main frontend page
- `app.js` - Frontend logic
- `style.css` - Application styling

## Requirements

- Python 3.10 or newer
- Supabase project
- Supabase `tasks` table

## Environment Variables

Create a file named `.env` with the following content:

SUPABASE_URL=your_supabase_project_url  
SUPABASE_KEY=your_supabase_api_key

The `.env` file is ignored by Git and should never be committed.

## Database Setup

Create a `tasks` table in Supabase with these columns:

- `id` - integer, primary key, auto-increment
- `title` - text
- `completed` - boolean, default `false`
- `created_at` - timestamp, default `now()`

## Installation

Open a terminal in the project directory and run:

`python -m venv myenv`

Activate the virtual environment:

Linux/macOS: `source myenv/bin/activate`

Windows: `myenv\Scripts\activate`

Install the dependencies:

`pip install -r backend/requirements.txt`

## Running the Application

Start the backend:

`cd backend`

`uvicorn main:app --reload`

The application will be available at:

`http://localhost:8000/`

The API documentation is available at:

`http://localhost:8000/docs`

## API Endpoints

- `GET /tasks` - Get all tasks
- `GET /tasks/{task_id}` - Get one task
- `POST /tasks` - Create a task
- `PUT /tasks/{task_id}` - Update a task
- `PATCH /tasks/{task_id}/complete` - Mark a task as completed
- `DELETE /tasks/{task_id}` - Delete a task

## Frontend-Only Development

To serve the frontend separately, run:

`cd frontend`

`python -m http.server 5500`

Then open:

`http://localhost:5500/`

## License

This project is for learning and personal use.
