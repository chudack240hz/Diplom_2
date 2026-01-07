"""Утилиты для генерации тестовых данных"""

from __future__ import annotations

from typing import Callable, Dict
from uuid import uuid4


def unique_user_data(**overrides: str) -> Dict[str, str]:
    """Генератор случайных данных пользователя для тестов"""
    suffix = uuid4().hex[:8]
    data: Dict[str, str] = {
        "email": f"autotest_{suffix}@example.com",
        "password": "P@ssw0rd123",
        "name": f"TestUser{suffix}",
    }
    data.update(overrides)
    return data
