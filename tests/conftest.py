"""Общие фикстуры для тестов"""

from __future__ import annotations

from typing import Callable, Dict, List
from uuid import uuid4

import pytest

from stellar_burgers_api import StellarBurgersApi


@pytest.fixture(scope="session")
def api_client() -> StellarBurgersApi:
    """Единый экземпляр API-клиента на всю сессию тестирования"""
    return StellarBurgersApi()


@pytest.fixture
def unique_user_data() -> Callable[..., Dict[str, str]]:
    """Генератор случайных данных пользователя для тестов"""

    def _factory(**overrides: str) -> Dict[str, str]:
        suffix = uuid4().hex[:8]
        data: Dict[str, str] = {
            "email": f"autotest_{suffix}@example.com",
            "password": "P@ssw0rd123",
            "name": f"TestUser{suffix}",
        }
        data.update(overrides)
        return data

    return _factory


@pytest.fixture
def registered_user(api_client: StellarBurgersApi, unique_user_data) -> Dict[str, str]:
    """Фикстура для создания временного пользователя"""
    payload = unique_user_data()
    response = api_client.register_user(payload)
    response.raise_for_status()
    body = response.json()
    token = body.get("accessToken")
    yield {
        "payload": payload,
        "accessToken": token,
        "refreshToken": body.get("refreshToken"),
    }
    if token:
        api_client.delete_user(token)


@pytest.fixture(scope="session")
def ingredient_ids(api_client: StellarBurgersApi) -> List[str]:
    """Кэшированный список ID доступных ингредиентов"""
    response = api_client.get_ingredients()
    response.raise_for_status()
    data = response.json()["data"]
    ids = [item["_id"] for item in data]
    assert ids, "Ожидалось, что API вернет хотя бы один идентификатор ингредиента"
    return ids


@pytest.fixture
def random_ingredients(ingredient_ids: List[str]) -> List[str]:
    """Возвращает список из первых двух доступных ID ингредиентов"""
    assert len(ingredient_ids) >= 2, "API вернуло недостаточное количество идентификаторов ингредиентов для тестов"
    return ingredient_ids[:2]
