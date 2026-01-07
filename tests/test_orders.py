"""Тесты для проверки функционала работы с заказами"""

from __future__ import annotations

import allure

from stellar_burgers_api import StellarBurgersApi


class TestOrders:
    @allure.epic("Заказы")
    @allure.feature("Создание")
    @allure.story("Авторизованный пользователь")
    def test_create_order_with_authorization(self, api_client: StellarBurgersApi, registered_user, random_ingredients):
        """Проверка создания заказа авторизованным пользователем"""
        token = registered_user["accessToken"]
        with allure.step("Создание заказа с токеном авторизации и валидными ингредиентами"):
            response = api_client.create_order(random_ingredients, token=token)
        body = response.json()
        assert response.status_code == 200
        assert body.get("success") is True
        assert body.get("order", {}).get("owner", {}).get("email") == registered_user["payload"]["email"]
        assert body.get("order", {}).get("name")


    @allure.epic("Заказы")
    @allure.feature("Создание")
    @allure.story("Неавторизованный пользователь")
    def test_create_order_without_authorization(self, api_client: StellarBurgersApi, random_ingredients):
        """Проверка создания заказа неавторизованным пользователем"""
        with allure.step("Создание заказа без токена авторизации, но с валидными ингредиентами"):
            response = api_client.create_order(random_ingredients)
        body = response.json()
        assert response.status_code == 200
        assert body.get("success") is True
        assert body.get("order", {}).get("number") > 0


    @allure.epic("Заказы")
    @allure.feature("Создание")
    @allure.story("Отсутствие ингредиентов")
    def test_create_order_without_ingredients(self, api_client: StellarBurgersApi, registered_user):
        """Проверка обработки попытки создания заказа без ингредиентов"""
        with allure.step("Создание заказа с пустым списком ингредиентов"):
            response = api_client.create_order([], token=registered_user["accessToken"])
        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"


    @allure.epic("Заказы")
    @allure.feature("Создание")
    @allure.story("Невалидные ингредиенты")
    def test_create_order_with_invalid_ingredient_hash(self, api_client: StellarBurgersApi):
        """Проверка обработки невалидного хеша ингредиента"""
        with allure.step("Создание заказа с невалидным хешем ингредиента"):
            response = api_client.create_order(["invalididhash"])
        assert response.status_code == 500
        assert "Internal Server Error" in response.text
