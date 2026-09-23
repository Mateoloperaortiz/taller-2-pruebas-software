import pytest

from app import create_app
from models import Order

pytestmark = pytest.mark.integration


def test_form_creates_and_displays_persisted_order(session_factory):
    app = create_app("fake", session_factory)
    app.config["TESTING"] = True
    with app.test_client() as client:
        response = client.post("/", data={"user_id": "7", "amount": "78"})
        assert response.status_code == 200
        assert "creada para user7@fake.local" in response.text
    # Otra instancia de Flask y otra sesión conservan los datos.
    with create_app("fake", session_factory).test_client() as client:
        assert "user7@fake.local" in client.get("/").text
    with session_factory() as db:
        order = db.query(Order).one()
        assert (order.user_email, order.amount, order.status) == (
            "user7@fake.local", 78, "CREATED"
        )


@pytest.mark.parametrize("data", [
    {"user_id": "1", "amount": "0"},
    {"user_id": "1", "amount": "-1"},
    {"user_id": "0", "amount": "10"},
    {"user_id": "abc", "amount": "10"},
    {"user_id": "1", "amount": "1.5"},
    {},
])
def test_form_rejects_invalid_values(data, session_factory):
    with create_app("fake", session_factory).test_client() as client:
        response = client.post("/", data=data)
        assert 'role="alert"' in response.text
    with session_factory() as db:
        assert db.query(Order).count() == 0


def test_app_shows_external_failure_without_saving(monkeypatch, session_factory):
    monkeypatch.setenv("SIMULATE_USER_API_FAILURE", "1")
    with create_app("real", session_factory).test_client() as client:
        response = client.post("/", data={"user_id": "1", "amount": "100"})
        assert "User service unavailable" in response.text
    with session_factory() as db:
        assert db.query(Order).count() == 0


def test_fake_works_even_when_real_repository_is_broken(monkeypatch, session_factory):
    monkeypatch.setenv("SIMULATE_USER_API_FAILURE", "1")
    with create_app("fake", session_factory).test_client() as client:
        response = client.post("/", data={"user_id": "3", "amount": "60"})
        assert "creada para user3@fake.local" in response.text


def test_repository_mode_must_be_explicitly_supported(session_factory):
    with pytest.raises(ValueError, match="USER_REPOSITORY"):
        create_app("unknown", session_factory)
