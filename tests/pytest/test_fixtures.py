import pytest


# Fixture that will be automatically called for each test
@pytest.fixture(autouse=True)
def send_analytics_data():
    print("[AUTOUSE] Sending data to analytics service")


# Fixture for initializing autotest settings at the session level
@pytest.fixture(scope="session")
def settings():
    print("[SESSION] Initializing autotest settings")


# Fixture for creating user data, which will be executed once per test class
@pytest.fixture(scope="class")
def user():
    print("[CLASS] Creating user data once per test class")


# Fixture for initializing the API client, run for each test
@pytest.fixture(scope="function")
def users_client():
    print("[FUNCTION] Creating API client for each autotest")


class TestUserFlow:
    def test_user_can_login(self, settings, user, users_client):
        pass

    def test_user_can_create_course(self, settings, user, users_client):
        pass


class TestAccountFlow:
    def test_user_account(self, settings, user, users_client):
        pass
