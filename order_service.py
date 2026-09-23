from contracts import Logger, Notifier, OrderSession, UserRepository
from models import Order


def create_order(
    user_id: int,
    amount: int,
    notifier: Notifier,
    logger: Logger,
    db: OrderSession,
    user_repository: UserRepository,
) -> Order:
    """Valida, consulta el usuario, guarda la orden y notifica su creación."""
    if amount <= 0:
        raise ValueError("Invalid amount")

    email = user_repository.get_user_email(user_id)
    logger.log(f"Creating order for {email}")
    order = Order(user_email=email, amount=amount, status="CREATED")
    db.add(order)
    db.commit()
    notifier.send(email, "Order created")
    return order
