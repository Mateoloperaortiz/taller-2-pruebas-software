import os

import requests


class JsonPlaceholderUserRepository:
    def get_user_email(self, user_id: int) -> str:
        # Paso 7: activa la misma excepción propuesta por el enunciado.
        # Se conserva la implementación real para reproducir ambos escenarios.
        if os.getenv("SIMULATE_USER_API_FAILURE") == "1":
            raise ConnectionError("User service unavailable")

        response = requests.get(
            f"https://jsonplaceholder.typicode.com/users/{user_id}", timeout=5
        )
        response.raise_for_status()
        return response.json()["email"]


class FakeUserRepository:
    def get_user_email(self, user_id: int) -> str:
        return f"user{user_id}@fake.local"
