import allure
import pytest
import requests

@pytest.fixture
def base_url():
    return "https://reqres.in/api/users/"

@pytest.fixture
def single_user_url(base_url):
    return base_url + "2"

@pytest.fixture
def create_user_payload():
    return {
        "name": "morpheus",
        "job": "leader"
    }

@pytest.fixture
def update_user_payload():
    return {
        "name": "morpheus",
        "job": "zion resident"
    }

@allure.title("Тест на получение информации о пользователе")
def test_single_user(single_user_url):
    with allure.step("Отправка GET-запроса для получения информации о пользователе"):
        response = requests.get(single_user_url)
    
    with allure.step("Проверка статус-кода ответа"):
        assert response.status_code == 200
    
    with allure.step("Проверка заголовка Content-Type"):
        assert response.headers['Content-Type'] == 'application/json; charset=utf-8'
    
    with allure.step("Проверка данных пользователя в ответе"):
        user_data = response.json()["data"]
        expected_fields = {"id", "email", "first_name", "last_name", "avatar"}
        assert set(user_data.keys()) == expected_fields

@allure.title("Тест на создание пользователя")
def test_create_user(base_url, create_user_payload):
    url = base_url
    with allure.step("Отправка POST-запроса для создания пользователя"):
        response = requests.post(url, json=create_user_payload)
    
    with allure.step("Проверка статус-кода ответа"):
        assert response.status_code == 201
    
    with allure.step("Проверка заголовка Content-Type"):
        assert response.headers['Content-Type'] == 'application/json; charset=utf-8'
    
    with allure.step("Проверка данных пользователя в ответе"):
        user_data = response.json()
        assert set(user_data.keys()) == {"id", "name", "job", "createdAt"}
        assert user_data["name"] == create_user_payload["name"]

@allure.title("Тест на обновление информации о пользователе")
def test_update_user(single_user_url, update_user_payload):
    with allure.step("Отправка PUT-запроса для обновления информации о пользователе"):
        response = requests.put(single_user_url, json=update_user_payload)
    
    with allure.step("Проверка статус-кода ответа"):
        assert response.status_code == 200
    
    with allure.step("Проверка заголовка Content-Type"):
        assert response.headers['Content-Type'] == 'application/json; charset=utf-8'
    
    with allure.step("Проверка данных пользователя в ответе"):
        user_data = response.json()
        assert set(user_data.keys()) == {"name", "job", "updatedAt"}
        assert user_data["job"] == update_user_payload["job"]

@allure.title("Тест на удаление пользователя")
def test_delete_user(single_user_url):
    with allure.step("Отправка DELETE-запроса для удаления пользователя"):
        response = requests.delete(single_user_url)
    
    with allure.step("Проверка статус-кода ответа"):
        assert response.status_code == 204
