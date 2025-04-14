from clients.private_http_builder import AuthenticationUserDict
from clients.users.private_users_client import get_private_users_client
from clients.users.public_users_client import get_public_users_client, CreateUserRequestDict
from tools.fakers import get_random_email


public_users_client = get_public_users_client()

create_user_request = CreateUserRequestDict(
    email=get_random_email(),
    password="string",
    lastName="string",
    firstName="string",
    middleName="string"
)

create_user_response = public_users_client.create_user(create_user_request)
print('Create user data: ', create_user_response)

authentication_user = AuthenticationUserDict(
    email=create_user_request["email"],
    password=create_user_request["password"]
)

private_user_client = get_private_users_client(authentication_user)

get_user_response = private_user_client.get_user(create_user_response['user']['id'])
print('Get user data: ', get_user_response)
