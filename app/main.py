from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routers import auth, rbac, goods, orders
from app.infrastructure.db.db_session import engine
from fastapi.responses import RedirectResponse
from app.infrastructure.db.init_db import (create_tables, initial_populate_all_db)


@asynccontextmanager
async def lifespan(application: FastAPI):
    # startup
    create_tables(engine)
    initial_populate_all_db()
    yield
    # shutdown
    print("Приложение завершает работу...")


app = FastAPI(lifespan=lifespan, title="Permission's system API")

app.include_router(auth.router)
app.include_router(rbac.router)
app.include_router(goods.router)
app.include_router(orders.router)


@app.get("/")
def root():
    return RedirectResponse("/docs")
    #Оставим на всякий случай
    # return HTMLResponse('<a href="http://127.0.0.1:8000/docs">Перейти на Swagger</a>')
