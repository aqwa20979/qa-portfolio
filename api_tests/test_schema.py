import requests

def test_post_schema_check(base_url):
    """Проверка схемы ответа: все ли поля на месте и правильного типа"""
    response = requests.get(f"{base_url}/posts/1")
    assert response.status_code == 200
    
    data = response.json()
    
    assert "id" in data, "Поле 'id' отсутствует"
    assert "title" in data, "Поле 'title' отсутствует"
    assert "body" in data, "Поле 'body' отсутствует"
    assert "userId" in data, "Поле 'userId' отсутствует"
    
    assert isinstance(data["id"], int), "id должен быть числом"
    assert isinstance(data["title"], str), "title должен быть строкой"
    assert isinstance(data["body"], str), "body должен быть строкой"
    assert isinstance(data["userId"], int), "userId должен быть числом"
    
    assert data["id"] > 0, "id должен быть положительным числом"
    assert len(data["title"]) > 0, "title не должен быть пустым"