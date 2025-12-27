import os
from fastapi.testclient import TestClient
from app.infrastructure.db.db_session import engine
from app.infrastructure.db.init_db import initial_populate_all_db, create_tables
from app.main import app

# Удаляем тестовую sqlite базу перед тестами
db_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(db_dir, "rbac_test.db")
print("База данных sqlite rbac_test.db перед тестами должна быть удалена")
try:
    os.remove(file_path)
except FileNotFoundError:
    # Файл уже отсутствует, ничего делать не нужно
    pass
except PermissionError:
    print("Нет прав на удаление файла.")
assert not os.path.isfile(file_path)
assert os.getenv("DATABASE_URL") == "sqlite:///tests/rbac_test.db"
create_tables(engine)
initial_populate_all_db()

Person = {
    "Super": {"email": "superadmin@example.com", "password": "admin"},
    "Access-Users": {"email": "access.admin@example.com", "password": "access123"},
    "Access-Goods": {"email": "warehouse.manager@example.com", "password": "whmanager"},
}


# Сценарий 1.
# Регистрируется новый пользователь, изменяет свое имя, неудачно пытается получить роль AccessAdmin
# Затем Access Admin создает роль просмотра домена users и предоставляет новому пользователю эту роль
# Новый пользователь просматривает всех пользователей и удаляет свой аккаунт

def test_scenario_1():
    client = TestClient(app)
    # test register new user
    response = client.post("/auth/register", json={"name": "New User", "email": "new@example.com", "password": "1"})
    new_user_id = response.json()['id']
    assert isinstance(new_user_id, int)
    assert response.status_code == 200
    # login new user
    response = client.post("/auth/login", json={"email": "new@example.com", "password": "1"})
    assert response.status_code == 200
    # test update name
    response = client.put("/auth/" + str(new_user_id), json={"name": "New", "email": "new@example.com", "password": "1"})
    assert response.status_code == 200
    # test get role
    response = client.post("/rbac/user_roles", json={"user_id": new_user_id, "role_id": 2})
    assert response.status_code == 403
    # login access admin
    response = client.post("/auth/login", json=Person["Access-Users"])
    assert response.status_code == 200
    # test create new role
    response = client.post("/rbac/roles", json={"name": "Users reading", "description": "Test for new user"})
    new_role_id = response.json()['id']
    assert isinstance(new_role_id, int)
    # test create new rule
    response = client.post("/rbac/rules", json={"role_id": new_role_id, "element_id": 2, "read_permission": True})
    assert response.status_code == 200
    # test assign role to new user
    response = client.post("/rbac/user_roles", json={"user_id": new_user_id, "role_id": new_role_id})
    assert response.status_code == 200
    # login new user
    response = client.post("/auth/login", json={"email": "new@example.com", "password": "1"})
    assert response.status_code == 200
    # test observe user list
    response = client.get("/auth/users_list")
    assert response.status_code == 200
    # test delete own account
    response = client.delete("/auth/" + str(new_user_id))
    assert response.status_code == 200


# Сценарий 2.
# AccessAdmin создает 2 новые роли: ответственного за создание ролей и ответственного за распределение ролей
# Затем Access Admin регистрирует 2 пользователей и закрепляет за ними созданные роли
# Ответственный за создание ролей создает роль чтения домена товаров, и меняет ее
# Ответственный за распределение ролей закрепляет за Access Admin роль аудитора

def test_scenario_2():
    client = TestClient(app)
    # login
    response = client.post("/auth/login", json=Person["Access-Users"])
    assert response.status_code == 200

    # test create new role Roles editor
    response = client.post("/rbac/roles", json={"name": "Roles editor",
                                                "description": "Responsible for roles profiles"})
    editor_role_id = response.json()['id']
    assert isinstance(editor_role_id, int)
    # test create new rule for business element
    response = client.post("/rbac/rules", json={"role_id": editor_role_id, "element_id": 3, "read_permission": True,
                                                "create_permission": True, "update_permission": True,
                                                "delete_permission": True})
    assert response.status_code == 200
    # test create new rule for roles and access role rules
    response = client.post("/rbac/rules", json={"role_id": editor_role_id, "element_id": 4, "read_permission": True,
                                                "create_permission": True, "update_permission": True,
                                                "delete_permission": True})
    assert response.status_code == 200

    # test create new role Roles distributor
    response = client.post("/rbac/roles", json={"name": "Roles distributor",
                                                "description": "Responsible for roles assignment"})
    distributor_role_id = response.json()['id']
    assert isinstance(distributor_role_id, int)
    # test create new rule for user_roles
    response = client.post("/rbac/rules", json={"role_id": distributor_role_id, "element_id": 5, "read_permission": True,
                                                "create_permission": True, "update_permission": True,
                                                "delete_permission": True})
    assert response.status_code == 200

    # test register user for Role editor
    response = client.post("/auth/register", json={"name": "Editor of roles", "email": "editor@example.com",
                                                   "password": "1"})
    editor_id = response.json()['id']
    assert isinstance(editor_id, int)
    # test assign role to Editor
    response = client.post("/rbac/user_roles", json={"user_id": editor_id, "role_id": editor_role_id})
    assert response.status_code == 200

    # test register user for Role distributor
    response = client.post("/auth/register", json={"name": "Distributor of roles",
                                                   "email": "distributor@example.com", "password": "1"})
    distributor_id = response.json()['id']
    assert isinstance(distributor_id, int)
    # test assign role to Distributor
    response = client.post("/rbac/user_roles", json={"user_id": distributor_id, "role_id": distributor_role_id})
    assert response.status_code == 200
    # logout Access Admin
    response = client.post("/auth/logout")
    assert "Logged out" in response.json()["detail"]

    # login editor
    response = client.post("/auth/login", json={"email": "editor@example.com", "password": "1"})
    assert response.status_code == 200

    # test create new role Goods observer
    response = client.post("/rbac/roles", json={"name": "Goods observer",
                                                "description": "Test for new roles in goods"})
    new_role_id = response.json()['id']
    assert isinstance(new_role_id, int)
    # test create new rule for Goods observer
    response = client.post("/rbac/rules",
                           json={"role_id": new_role_id, "element_id": 6, "read_permission": True})
    assert response.status_code == 200
    # test update new rule for user_roles
    response = client.put("/rbac/roles/" + str(new_role_id), json={"name": "Observer in goods",
                                                "description": "The role for observer in goods"})
    assert response.status_code == 200
    # logout editor
    response = client.post("/auth/logout")
    assert "Logged out" in response.json()["detail"]

    # login distributor
    response = client.post("/auth/login", json={"email": "distributor@example.com", "password": "1"})
    assert response.status_code == 200
    # test assign role auditor to Access Admin
    response = client.post("/rbac/user_roles", json={"user_id": 2, "role_id": 7})
    assert response.status_code == 200
    # logout editor
    response = client.post("/auth/logout")
    assert "Logged out" in response.json()["detail"]


def test_users_list_authorized():
    client = TestClient(app)
    # login
    response = client.post("/auth/login", json=Person["Super"])
    assert response.status_code == 200
    # test
    response = client.get("/auth/users_list")
    assert response.status_code == 200


def test_users_list_with_logout():
    client = TestClient(app)
    # login
    response = client.post("/auth/login", json=Person["Super"])
    assert response.status_code == 200
    # logout
    response = client.post("/auth/logout")
    assert "Logged out" in response.json()["detail"]
    # test
    response = client.get("/auth/users_list")
    assert response.status_code == 401


def test_users_list_unauthorized():
    client = TestClient(app)
    # login
    response = client.post("/auth/login", json=Person["Access-Goods"])
    assert response.status_code == 200
    # test
    response = client.get("/auth/users_list")
    assert response.status_code == 403


def test_get_user_authorized():
    client = TestClient(app)
    # login
    response = client.post("/auth/login", json=Person["Access-Goods"])
    assert response.status_code == 200
    # test
    response = client.get("/auth/3")
    assert response.status_code == 200


def test_get_user_unauthorized():
    client = TestClient(app)
    # login
    response = client.post("/auth/login", json=Person["Access-Goods"])
    assert response.status_code == 200
    # test
    response = client.get("/auth/4")
    assert response.status_code == 403


def test_update_user_unauthorized():
    client = TestClient(app)
    # login
    response = client.post("/auth/login", json=Person["Access-Goods"])
    assert response.status_code == 200
    # test
    response = client.put("/auth/4", json={"email": "fake@email.com"})
    assert response.status_code == 403


def test_delete_user_unauthorized():
    client = TestClient(app)
    # login
    response = client.post("/auth/login", json=Person["Access-Goods"])
    assert response.status_code == 200
    # test
    response = client.delete("/auth/4")
    assert response.status_code == 403
