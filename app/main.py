from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routers import auth, rbac, goods, orders
from app.config import COOKIES_MAX_AGE
from app.infrastructure.db.db_session import engine
from fastapi.responses import RedirectResponse
from app.infrastructure.db.init_db import (create_tables, populate_users, populate_business_elements, populate_roles,
                                           populate_access_role_rules, populate_user_roles, initial_populate_all_db)
from fastapi.openapi.utils import get_openapi


@asynccontextmanager
async def lifespan(application: FastAPI):
    # startup
    create_tables(engine)
    # populate_users()
    # populate_business_elements()
    # populate_roles()
    # populate_access_role_rules()
    # populate_user_roles()
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
#     # return HTMLResponse('<a href="http://127.0.0.1:8000/docs">Перейти на Swagger</a>')


# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#
#     schema = get_openapi(
#         title="Auth API",
#         version="1.0.0",
#         routes=app.routes,
#     )
#
#     schema["components"]["securitySchemes"] = {
#         "SessionCookieAuth": {
#             "type": "apiKey",
#             "in": "cookie",
#             "name": "session_id",
#         }
#     }
#
#     # применяем защиту по умолчанию
#     for path in schema["paths"].values():
#         for method in path.values():
#             method.setdefault("security", [{"SessionCookieAuth": []}])
#
#     app.openapi_schema = schema
#     return schema

# app.openapi = custom_openapi