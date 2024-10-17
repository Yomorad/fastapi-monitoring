from fastapi import FastAPI
from scheduler import start_scheduler
from api import router as api_router

app = FastAPI()

# Событие старта приложения для инициализации планировщика
@app.on_event("startup")
async def startup_event():
    start_scheduler()

# Подключаем маршруты
app.include_router(api_router)
