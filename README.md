# FastAPI Starter with uv package amanger

This example include SQLModel also.

After cloning for forking
- Create a virtual invironment:
```
uv venv
```
- Install dependencies using pyproject.toml:
```
uv sync
```

For this example to run correctly it also require a .env file with the following fields:
```
LOG_FILE='fastapi.log'
LOG_NAME='FASTAPI'
API_KEY='<your api key>'
DATABASE_PATH="~/project_root/uv_fastapi_starter/db/todo.db"
```
