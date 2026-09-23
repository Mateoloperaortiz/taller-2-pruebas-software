"""Unidad real: ni red ni SQLite; se observa solo la lógica de create_order."""

from unittest.mock import Mock

import pytest

from contracts import Logger, Notifier, OrderSession
from order_service import create_order

pytestmark = pytest.mark.unit


class StubUserRepository:
    def get_user_email(self, user_id: int) -> str:
        return "stub@example.test"


class DummyLogger:
    def log(self, msg: str) -> None:
        pass


class NullNotifier:
    def send(self, to: str, message: str) -> None:
        pass


def test_create_order_with_stub():
    db = Mock(spec=OrderSession)
    notifier = Mock(spec=Notifier)
    logger = Mock(spec=Logger)
    order = create_order(10, 200, notifier, logger, db, StubUserRepository())

    assert order.status == "CREATED"
    assert order.user_email == "stub@example.test"
    assert order.amount == 200
    db.add.assert_called_once_with(order)
    db.commit.assert_called_once_with()
    notifier.send.assert_called_once_with("stub@example.test", "Order created")
    logger.log.assert_called_once_with("Creating order for stub@example.test")


@pytest.mark.parametrize("amount", [0, -1, -200])
def test_invalid_amount_has_no_side_effects(amount):
    db = Mock(spec=OrderSession)
    notifier = Mock(spec=Notifier)
    repository = Mock(spec=StubUserRepository)
    with pytest.raises(ValueError, match="^Invalid amount$"):
        create_order(10, amount, notifier, DummyLogger(), db, repository)
    repository.get_user_email.assert_not_called()
    db.add.assert_not_called()
    db.commit.assert_not_called()
    notifier.send.assert_not_called()


def test_repository_failure_does_not_save_or_notify():
    db = Mock(spec=OrderSession)
    notifier = Mock(spec=Notifier)
    repository = Mock(spec=StubUserRepository)
    repository.get_user_email.side_effect = ConnectionError("User service unavailable")
    with pytest.raises(ConnectionError, match="User service unavailable"):
        create_order(1, 100, notifier, DummyLogger(), db, repository)
    db.add.assert_not_called()
    db.commit.assert_not_called()
    notifier.send.assert_not_called()


def test_commit_failure_does_not_notify():
    db = Mock(spec=OrderSession)
    db.commit.side_effect = RuntimeError("Database unavailable")
    notifier = Mock(spec=Notifier)
    with pytest.raises(RuntimeError, match="Database unavailable"):
        create_order(1, 100, notifier, DummyLogger(), db, StubUserRepository())
    notifier.send.assert_not_called()
