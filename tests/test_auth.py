import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.dependencies import get_user_service, get_current_user, get_permission_service, get_blacklist_service
from app.use_cases.users_service import UserService
from app.use_cases.permission import Permission
from app.use_cases.blacklist_service import TokenBlacklistService
from app.domain.interfaces.security.jwt_provider_impl import JWTTokenProvider


# ==========================
#  MOCKS
# ==========================

class MockUser:
    def __init__(self, id, email, name="Test User"):
        self.id = id
        self.email = email
        self.name = name
        self.is_active = True


class MockUserService:
    def register(self, name, email, password):
        provider = JWTTokenProvider()
        return provider.encode({"sub": 1})

    def login(self, email, password):
        provider = JWTTokenProvider()
        return provider.encode({"sub": 1})

    def get_users_list(self):
        return [MockUser(1, "test@example.com")]

    def get_user(self, user_id: int):
        return MockUser(user_id, "user@example.com")

    def update_user(self, user_id, data):
        return MockUser(user_id, "updated@example.com")

    def delete_user(self, user_id):
        return True


class MockPermission:
    def has_permission(self, user_id, element_code, permission_type):
        return True   # разрешаем всё в тестах


class MockBlacklist(TokenBlacklistService):
    def __init__(self):
        self.data = set()

    def add(self, token, exp):
        self.data.add(token)

    def contains(self, token) -> bool:
        return token in self.data


mock_blacklist = MockBlacklist()


def mock_get_user_service():
    return MockUserService()


def mock_get_permission_service():
    return MockPermission()


def mock_get_current_user():
    return MockUser(id=1, email="x")


def mock_get_blacklist_service():
    return mock_blacklist


# ==========================
#  APPLY DEPENDENCY OVERRIDES
# ==========================

app.dependency_overrides[get_user_service] = mock_get_user_service
app.dependency_overrides[get_permission_service] = mock_get_permission_service
app.dependency_overrides[get_current_user] = mock_get_current_user
app.dependency_overrides[get_blacklist_service] = mock_get_blacklist_service


client = TestClient(app)


# ==========================
#  TESTS
# ==========================

def test_register():
    response = client.post("/auth/register", json={
        "name": "John",
        "email": "john@example.com",
        "password": "12345"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login():
    response = client.post("/auth/login", json={
        "email": "john@example.com",
        "password": "12345"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token


def test_users_list_authorized():
    token = JWTTokenProvider().encode({"sub": 1})

    response = client.get(
        "/auth/users_list",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_logout_blacklists_token():
    token = JWTTokenProvider().encode({"sub": 1})

    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert mock_blacklist.contains(token)


def test_blacklisted_token_rejected():
    token = JWTTokenProvider().encode({"sub": 1})
    mock_blacklist.add(token, 9999999999)

    response = client.get(
        "/auth/users_list",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401
