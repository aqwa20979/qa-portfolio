import requests

def test_get_post(base_url):
    """Получить существующий пост - проверка статуса и данных"""
    response = requests.get(f"{base_url}/posts/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_get_nonexistent_post(base_url):
    """Получить несуществующий пост - должен вернуть 404"""
    response = requests.get(f"{base_url}/posts/999")
    assert response.status_code == 404

def test_create_post(base_url):
    """Создать новый пост"""
    new_post = {
        "title": "Мой новый пост",
        "body": "Текст поста",
        "userId": 1
    }        
    response = requests.post(f"{base_url}/posts", json=new_post)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Мой новый пост"

def test_delete_post(base_url):
    """Удалить пост"""
    response = requests.delete(f"{base_url}/posts/999")    
    assert response.status_code == 200

def test_delete_nonexistent_post(base_url):
    """Удалить несуществующий пост - API возвращает 200"""
    response = requests.delete(f"{base_url}/posts/999")
    assert response.status_code == 200
    