import socket

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base


@pytest.fixture(autouse=True)
def block_network_for_local_tests(request, monkeypatch):
    """Una prueba local falla de inmediato si intenta abrir una conexión de red."""
    if request.node.get_closest_marker("external") is None:
        def blocked(*args, **kwargs):
            raise AssertionError("Esta prueba no debe usar la red")

        monkeypatch.setattr(socket.socket, "connect", blocked)
        monkeypatch.setattr(socket.socket, "connect_ex", blocked)


@pytest.fixture
def session_factory(tmp_path):
    test_engine = create_engine(f"sqlite:///{tmp_path / 'test_orders.db'}")
    Base.metadata.create_all(test_engine)
    yield sessionmaker(bind=test_engine, expire_on_commit=False)
    test_engine.dispose()


@pytest.fixture
def db(session_factory):
    with session_factory() as session:
        yield session
