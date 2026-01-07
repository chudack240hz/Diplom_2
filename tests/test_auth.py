"""Тесты для проверки функционала аутентификации и регистрации пользователей"""

from __future__ import annotations

import allure

from stellar_burgers_api import StellarBurgersApi


class TestAuth:
    @allure.epic("Управление пользователями")
    @allure.feature("Регистрация")
    @allure.story("Создание уникального пользователя")
    def test_create_unique_user(self, api_client: StellarBurgersApi, unique_user_data):
        """Проверка успешной регистрации нового пользователя"""
        payload = unique_user_data()
        with allure.step("Регистрация нового пользователя"):
            response = api_client.register_user(payload)
        body = response.json()
        token = body.get("accessToken")
        try:
            assert response.status_code == 200
            assert body.get("success") is True
            assert body.get("user", {}).get("email") == payload["email"]
            assert token and token.startswith("Bearer ")
        finally:
            if token:
                api_client.delete_user(token)


    @allure.epic("Управление пользователями")
    @allure.feature("Регистрация")
    @allure.story("Попытка создания дубликата пользователя")
    def test_create_registered_user_fails(self, api_client: StellarBurgersApi, unique_user_data):
        """Проверка обработки попытки регистрации существующего пользователя
        
        Ожидается ошибка с кодом 403 и соответствующим сообщением
        """
        payload = unique_user_data()
        initial_response = api_client.register_user(payload)
        initial_response.raise_for_status()
        initial_token = initial_response.json().get("accessToken")
        try:
            with allure.step("Попытка повторной регистрации с теми же данными"):
                duplicate_response = api_client.register_user(payload)
            assert duplicate_response.status_code == 403
            assert duplicate_response.json()["message"] == "User already exists"
        finally:
            if initial_token:
                api_client.delete_user(initial_token)


    @allure.epic("Управление пользователями")
    @allure.feature("Регистрация")
    @allure.story("Отсутствие обязательных полей")
    def test_create_user_without_required_field(self, api_client: StellarBurgersApi, unique_user_data):
        """Проверка валидации обязательных полей при регистрации
        
        Удаляется обязательное поле password и проверяется ответ сервера
        """
        payload = unique_user_data()
        payload.pop("password")
        with allure.step("Отправка запроса на регистрацию без пароля"):
            response = api_client.register_user(payload)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"


    @allure.epic("Управление пользователями")
    @allure.feature("Авторизация")
    @allure.story("Вход с валидными учетными данными")
    def test_login_existing_user(self, api_client: StellarBurgersApi, registered_user):
        """Проверка успешной авторизации существующего пользователя"""
        credentials = {
            "email": registered_user["payload"]["email"],
            "password": registered_user["payload"]["password"],
        }
        with allure.step("Вход с валидными учетными данными"):
            response = api_client.login(credentials)
        body = response.json()
        assert response.status_code == 200
        assert body.get("success") is True
        assert body.get("user", {}).get("email") == credentials["email"]
        assert body.get("accessToken")


    @allure.epic("Управление пользователями")
    @allure.feature("Авторизация")
    @allure.story("Вход с неверным паролем")
    def test_login_with_wrong_password(self, api_client: StellarBurgersApi, registered_user):
        """Проверка обработки неверных учетных данных при авторизации"""
        credentials = {
            "email": registered_user["payload"]["email"],
            "password": "WrongPassword123",
        }
        with allure.step("Попытка входа с неверным паролем"):
            response = api_client.login(credentials)
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"
