"""Nombre original del taller: en realidad es integración con SQLite y red."""

import pytest

from order_service import create_order
from user_repository import JsonPlaceholderUserRepository

pytestmark = [pytest.mark.external, pytest.mark.integration]


class DummyLogger:
    def log(self, msg: str) -> None:
        pass


class NullNotifier:
    def send(self, to: str, message: str) -> None:
        pass


def test_create_order_with_real_api(db):
    order = create_order(
        1, 100, NullNotifier(), DummyLogger(), db, JsonPlaceholderUserRepository()
    )
    assert order.status == "CREATED"
    assert order.user_email == "Sincere@april.biz"
