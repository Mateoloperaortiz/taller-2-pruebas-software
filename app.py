import os

import requests
from flask import Flask, render_template, request
from sqlalchemy.exc import SQLAlchemyError

from database import Base, SessionLocal, engine
from models import Order
from order_service import create_order
from user_repository import FakeUserRepository, JsonPlaceholderUserRepository


class WebNotifier:
    def send(self, to: str, message: str) -> None:
        # Simulación local: el taller no requiere enviar correos reales.
        print(f"{to}: {message}")


class WebLogger:
    def log(self, message: str) -> None:
        print(message)


def create_app(repository_mode: str | None = None, session_factory=None) -> Flask:
    app = Flask(__name__)
    mode = repository_mode or os.getenv("USER_REPOSITORY", "fake")
    repositories = {
        "fake": FakeUserRepository,
        "real": JsonPlaceholderUserRepository,
    }
    if mode not in repositories:
        raise ValueError("USER_REPOSITORY debe ser real o fake")

    repository = repositories[mode]()
    if session_factory is None:
        Base.metadata.create_all(bind=engine)
        session_factory = SessionLocal

    @app.route("/", methods=["GET", "POST"])
    def index() -> str:
        result = None
        error = None
        with session_factory() as db:
            if request.method == "POST":
                try:
                    user_id = int(request.form.get("user_id", ""))
                    amount = int(request.form.get("amount", ""))
                    if user_id <= 0:
                        raise ValueError("El ID del usuario debe ser positivo")
                    result = create_order(
                        user_id, amount, WebNotifier(), WebLogger(), db, repository
                    )
                except (ValueError, ConnectionError, requests.RequestException) as exc:
                    db.rollback()
                    error = str(exc)
                except SQLAlchemyError:
                    db.rollback()
                    app.logger.exception("No fue posible guardar la orden")
                    error = "No fue posible guardar la orden"
            orders = db.query(Order).order_by(Order.id.desc()).all()
            return render_template(
                "index.html", result=result, orders=orders, error=error, mode=mode
            )

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")))
