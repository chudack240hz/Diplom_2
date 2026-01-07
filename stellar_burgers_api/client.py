"""API-клиент для использования в тестах"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional

import requests


@dataclass
class StellarBurgersApi:
    """Обертка для HTTP-запросов к API Stellar Burgers"""

    base_url: str = "https://stellarburgers.education-services.ru"
    timeout: int = 10

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        """Выполняет HTTP-запрос к API
        
        Args:
            method: HTTP-метод (GET, POST, DELETE)
            path: Путь к эндпоинту API
            **kwargs: Дополнительные параметры запроса
            
        Returns:
            Ответ от сервера
        """
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)
        response = requests.request(method, url, **kwargs)
        return response

    def register_user(self, payload: Dict[str, Any]) -> requests.Response:
        """Регистрация нового пользователя
        
        Args:
            payload: Словарь с данными пользователя (email, password, name)
            
        Returns:
            Ответ сервера с данными пользователя
        """
        return self._request("POST", "/api/auth/register", json=payload)

    def login(self, payload: Dict[str, Any]) -> requests.Response:
        """Аутентификация пользователя
        
        Args:
            payload: Учетные данные (email и пароль)
            
        Returns:
            Ответ сервера с токеном доступа
        """
        return self._request("POST", "/api/auth/login", json=payload)

    def delete_user(self, token: str) -> requests.Response:
        """Удаление аутентифицированного пользователя
        
        Args:
            token: Токен аутентификации пользователя
            
        Returns:
            Ответ сервера об успешном удалении
        """
        headers = {"Authorization": token}
        return self._request("DELETE", "/api/auth/user", headers=headers)

    def get_ingredients(self) -> requests.Response:
        """Получение списка доступных ингредиентов
        
        Returns:
            Список всех доступных ингредиентов
        """
        return self._request("GET", "/api/ingredients")

    def create_order(
        self,
        ingredients: Iterable[str],
        token: Optional[str] = None,
    ) -> requests.Response:
        """Создание нового заказа
        
        Args:
            ingredients: Список ID ингредиентов
            token: Опциональный токен аутентификации
            
        Returns:
            Ответ сервера с данными заказа
        """
        headers = {"Authorization": token} if token else None
        payload = {"ingredients": list(ingredients)}
        return self._request("POST", "/api/orders", json=payload, headers=headers)
