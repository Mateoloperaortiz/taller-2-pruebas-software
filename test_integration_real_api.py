import pytest

from models import Order
from order_service import create_order
from user_repository import JsonPlaceholderUserRepository

pytestmark = [pytest.mark.external, pytest.mark.integration]


class DummyLogger:
    def log(self, msg: str) -> None:
        pass


class NullNotifier:
    def send(self, to: str, message: str) -> None:
        pass


def test_create_order_integration_real_api(db, session_factory):
    order = create_order(
        1, 50, NullNotifier(), DummyLogger(), db, JsonPlaceholderUserRepository()
    )
    order_id = order.id
    db.close()
    with session_factory() as reopened:
        persisted = reopened.get(Order, order_id)
        assert persisted is not None
        assert persisted.status == "CREATED"
        assert persisted.user_email == "Sincere@april.biz"
        assert persisted.amount == 50
