import httpx


# Данные для входа в систему
login_payload = {
    "email": "user@example.com",
    "password": "string"
}

# Выполняем запрос на аутентификацию
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()

print("Status Code:", login_response.status_code)
print(25 * '-')

login_response_access_token = login_response_data['token']['accessToken']

# Формируем headers для /users/me
me_headers = {
    "Authorization": f"Bearer {login_response_access_token}"
}

me_response = httpx.get("http://localhost:8000/api/v1/users/me", headers=me_headers)
me_response_data = me_response.json()

print("Me response:", me_response_data)
print("Status Code:", me_response.status_code)
