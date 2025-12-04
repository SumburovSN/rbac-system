from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routers import auth, rbac, goods, orders
from app.infrastructure.db.session import engine
from fastapi.responses import RedirectResponse
from app.infrastructure.db.init_db import (create_tables, populate_users, populate_business_elements, populate_roles,
                                           populate_access_role_rules, populate_user_roles)


@asynccontextmanager
async def lifespan(application: FastAPI):
    # startup
    create_tables(engine)
    populate_users()
    populate_business_elements()
    populate_roles()
    populate_access_role_rules()
    populate_user_roles()
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
#     # return HTMLResponse('<a href="http://127.0.0.1:8000/docs">Перейти на Swagger</a>')