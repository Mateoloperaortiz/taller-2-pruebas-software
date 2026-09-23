"""Contratos mínimos que la lógica necesita de sus dependencias."""

from typing import Protocol

from models import Order


class Logger(Protocol):
    def log(self, message: str) -> None: ...


class Notifier(Protocol):
    def send(self, to: str, message: str) -> None: ...


class OrderSession(Protocol):
    def add(self, order: Order) -> None: ...

    def commit(self) -> None: ...


class UserRepository(Protocol):
    def get_user_email(self, user_id: int) -> str: ...
