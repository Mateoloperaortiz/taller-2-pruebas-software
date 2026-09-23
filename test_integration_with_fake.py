import pytest

from models import Order
from order_service import create_order
from user_repository import FakeUserRepository

pytestmark = pytest.mark.integration


class DummyLogger:
    def log(self, msg: str) -> None:
        pass


class NullNotifier:
    def send(self, to: str, message: str) -> None:
        pass


def test_create_order_integration_with_fake(db, session_factory):
    order = create_order(3, 60, NullNotifier(), DummyLogger(), db, FakeUserRepository())
    order_id = order.id
    db.close()
    with session_factory() as reopened:
        persisted = reopened.get(Order, order_id)
        assert persisted is not None
        assert persisted.status == "CREATED"
        assert persisted.user_email == "user3@fake.local"
        assert persisted.amount == 60


def test_invalid_amount_is_not_persisted(db):
    with pytest.raises(ValueError, match="Invalid amount"):
        create_order(3, 0, NullNotifier(), DummyLogger(), db, FakeUserRepository())
    assert db.query(Order).count() == 0
