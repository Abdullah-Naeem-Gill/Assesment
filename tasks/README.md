# Task Management

A task management api

## API Endpoints

### Public Endpoints (No Authentication Required)
- `POST /tasks` - Create Task
- `GET /tasks` - Get tasks (list)
- `GET /tasks` - Get task by id
- `PUT /tasks` - Update task by id
- `DELETE /tasks` - Delete task by id
- `GET /tasks/statistics` - Get statistics


## Installation

### Local Development


1. **Clone the repository**
   ```bash
   N/A
   ```

2. **Install dependencies**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```


3. **Run the service**
   ```bash
   uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```
