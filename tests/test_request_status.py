import requests

BASE_URL = "https://api.example.com"


def test_user_cannot_change_status(user_token):
    """
    Проверяем бизнес-правило:
    пользователь не может самостоятельно менять статус заявки.
    """

    headers = {
        "Authorization": f"Bearer {user_token}",
        "Content-Type": "application/json"
    }

    # Шаг 1. Создаем заявку
    create_payload = {
        "name": "Ivan Petrov",
        "phone": "+79991234567",
        "email": "ivan@test.com",
        "age": 25
    }

    create_response = requests.post(
        f"{BASE_URL}/requests",
        json=create_payload,
        headers=headers
    )

    assert create_response.status_code == 201

    request_data = create_response.json()

    request_id = request_data["id"]

    # Проверяем смысл результата
    assert request_data["status"] == "new"
    assert request_data["name"] == create_payload["name"]

    # Шаг 2. Пытаемся изменить статус обычным пользователем
    update_response = requests.patch(
        f"{BASE_URL}/requests/{request_id}",
        json={"status": "done"},
        headers=headers
    )

    assert update_response.status_code in [403, 422]

    # Шаг 3. Получаем заявку повторно
    get_response = requests.get(
        f"{BASE_URL}/requests/{request_id}",
        headers=headers
    )

    assert get_response.status_code == 200

    updated_request = get_response.json()

    # Главное: статус НЕ изменился
    assert updated_request["status"] == "new"

    # Дополнительно убеждаемся,
    # что заявка та же самая
    assert updated_request["id"] == request_id
