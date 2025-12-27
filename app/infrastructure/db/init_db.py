from app.api.schemas.rbac import BusinessElementCreate, RoleCreate, AccessRoleRuleCreate, UserRoleCreate
from app.infrastructure.db.db_session import SessionLocal
from app.infrastructure.db import base
from app.api.dependencies import (get_user_service, get_business_element_service, get_role_service,
                                  get_access_rule_service, get_user_role_service)
from app.infrastructure.repositories.role_repo import RoleRepositoryImpl
from app.infrastructure.repositories.business_element_repo import BusinessElementRepositoryImpl
# Импорты чтобы SQLAlchemy увидел модели
from app.infrastructure.db.models import user, user_role, role, business_element, access_role_rule


def create_tables(engine):
    # Создаём таблицы (лучше через Alembic, но для учебного ок)
    base.Base.metadata.create_all(bind=engine)


def populate_users():
    users_to_add = [
        ("Superadmin", "superadmin@example.com", "admin"),

        ("Access Admin", "access.admin@example.com", "access123"),

        ("Warehouse Manager", "warehouse.manager@example.com", "whmanager"),
        ("Warehouse Viewer", "warehouse.viewer@example.com", "whviewer"),

        ("Procurement Manager", "procurement.manager@example.com", "procmanager"),
        ("Procurement Viewer", "procurement.viewer@example.com", "procviewer"),

        ("Auditor", "auditor@example.com", "audit123"),
    ]

    with SessionLocal() as db:
        service = get_user_service(db)
        for name, email, password in users_to_add:
            try:
                service.register(name, email, password)
            except ValueError:
                pass  # пользователь уже есть


def populate_business_elements():
    elements_to_add = [
        ("all", "Все базы данных"),
        ("users", "Список пользователей"),
        ("business_elements", "Блоки приложения для доступа"),
        # ("roles", "Пользовательские роли"), # объединены с user_roles
        ("access_role_rules", "Правила доступа роли к блоку приложения"),
        ("user_roles", "Назначение роли (предоставление права доступа к блоку приложения"),
        ("goods", "Склад, получение товаров и распределение их по магазинам"),
        ("orders", "Заказ товаров и работа с поставщиками"),
    ]

    with SessionLocal() as db:
        service = get_business_element_service(db)
        for code, name in elements_to_add:
            try:
                service.create(BusinessElementCreate(code=code, name=name))
            except ValueError:
                pass  # элемент уже есть


def populate_roles():
    roles_to_add = [
        ("Superadmin", "Администратор базы данных (полный доступ ко всем таблицам и ролям)"),
        ("AccessAdmin", "Администратор прав доступа (может управлять пользователями и ролями)"),

        ("WarehouseManager", "Менеджер склада (полный доступ к товарам на складе)"),
        ("WarehouseViewer", "Просмотр склада (только чтение товаров)"),

        ("ProcurementManager", "Менеджер закупок (полный CRUD по заказам)"),
        ("ProcurementViewer", "Просмотр заказов (только чтение)"),

        ("Auditor", "Аудитор (чтение всех данных без возможности изменения)")
    ]

    with SessionLocal() as db:
        service = get_role_service(db)
        for name, description in roles_to_add:
            try:
                service.create(RoleCreate(name=name, description=description))
            except ValueError:
                pass  # элемент уже есть


def populate_access_role_rules():
    # Список из формата:
    # (role_code, element_code, read, create, update, delete)
    # в формат:
    # (role_id, element_id, read, create, update, delete)
    rules_to_add = [
        # ---------------- SUPERADMIN ----------------
        ("Superadmin", "all", True, True, True, True),

        # ---------------- ADMIN ----------------------
        ("AccessAdmin", "users", True, True, True, True),
        ("AccessAdmin", "user_roles", True, True, True, True),
        ("AccessAdmin", "business_elements", True, True, True, True),
        ("AccessAdmin", "access_role_rules", True, True, True, True),

        # ---------------- WAREHOUSE ------------------
        ("WarehouseManager", "goods", True, True, True, True),

        # ---------------- PROCUREMENT ----------------
        ("ProcurementManager", "orders", True, True, True, True),

        # ---------------- VIEWER ---------------------
        ("WarehouseViewer", "goods", True, False, False, False),
        ("ProcurementViewer", "orders", True, False, False, False),
        ("Auditor", "goods", True, False, False, False),
        ("Auditor", "orders", True, False, False, False)
    ]

    with SessionLocal() as db:
        rule_service = get_access_rule_service(db)

        for role_name, element_code, r, c, u, d in rules_to_add:
            try:
                role_repo = RoleRepositoryImpl(db)
                role = role_repo.get_by_name(role_name)
                el_repo = BusinessElementRepositoryImpl(db)
                element = el_repo.get_by_code(element_code)

                # создаём правило
                rule_service.create(AccessRoleRuleCreate(
                    role_id=role.id,
                    element_id=element.id,
                    read_permission=r,
                    create_permission=c,
                    update_permission=u,
                    delete_permission=d,)
                )

            except ValueError:
                pass  # правило уже существует


def populate_user_roles():
    user_roles_to_add = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]
    with SessionLocal() as db:
        service = get_user_role_service(db)

        for user_id, role_id in user_roles_to_add:
            try:
                # user_role = UserRoleCreate
                service.create(UserRoleCreate(user_id=user_id, role_id=role_id))
            except ValueError:
                pass  # правило уже существует

def initial_populate_all_db():
    populate_users()
    populate_business_elements()
    populate_roles()
    populate_access_role_rules()
    populate_user_roles()