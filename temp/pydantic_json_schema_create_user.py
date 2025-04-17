from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import (CreateUserRequestSchema,
                                        CreateUserResponseSchema)
# Добавили импорт функции validate_json_schema
from tools.assertions.schema import validate_json_schema
from tools.fakers import get_random_email

public_users_client = get_public_users_client()

create_user_request = CreateUserRequestSchema(
    email=get_random_email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string"
)
create_user_response = public_users_client.create_user_api(create_user_request)
# Получаем JSON схему из модели ответа
create_user_response_schema = CreateUserResponseSchema.model_json_schema()

# Проверяем, что JSON ответ от API соответствует ожидаемой JSON схеме
validate_json_schema(instance=create_user_response.json(), schema=create_user_response_schema)
