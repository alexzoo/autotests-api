# API Testing Framework Architecture - Полное руководство

## Содержание

1. [Обзор архитектуры](#обзор-архитектуры)
2. [Технологический стек](#технологический-стек)
3. [Структура проекта](#структура-проекта)
4. [Базовые компоненты](#базовые-компоненты)
5. [Система конфигурации](#система-конфигурации)
6. [HTTP Builders](#http-builders)
7. [Схемы данных (Pydantic)](#схемы-данных-pydantic)
8. [Специализированные клиенты](#специализированные-клиенты)
9. [Система фикстур](#система-фикстур)
10. [Assertions и валидация](#assertions-и-валидация)
11. [Allure интеграция](#allure-интеграция)
12. [Coverage tracking](#coverage-tracking)
13. [Утилиты и инструменты](#утилиты-и-инструменты)
14. [Примеры тестов](#примеры-тестов)
15. [Конфигурационные файлы](#конфигурационные-файлы)
16. [Команды и workflow](#команды-и-workflow)
17. [Расширение фреймворка](#расширение-фреймворка)

---

## Обзор архитектуры

Этот фреймворк автотестов API построен на многослойной архитектуре, обеспечивающей:

- **Модульность** - каждый компонент отвечает за свою задачу
- **Переиспользование** - базовые компоненты используются во всех доменах
- **Масштабируемость** - легко добавлять новые домены и функциональность
- **Отчётность** - интеграция с Allure для детальных отчётов
- **Покрытие API** - автоматическое отслеживание покрытия эндпоинтов

### Основные принципы:

1. **Разделение ответственности** - HTTP клиенты, API клиенты, схемы данных
2. **Автоматизация** - логирование, отчёты, валидация схем
3. **Тестируемость** - фикстуры для всех компонентов
4. **Читаемость** - Allure аннотации, понятная структура тестов

---

## Технологический стек

### Основные зависимости:

```txt
allure-pytest==2.13.5          # Продвинутые отчёты с шагами и аттачментами
email_validator==2.2.0         # Валидация email адресов в pydantic
Faker==36.2.2                  # Генерация случайных тестовых данных
httpx==0.28.1                  # Современный асинхронный HTTP клиент
jsonschema==4.23.0             # Валидация JSON схем ответов API
pydantic==2.10.6               # Валидация и сериализация данных
pydantic-settings==2.8.1       # Управление конфигурацией через переменные окружения
pytest==8.3.5                  # Основной фреймворк тестирования
pytest-rerunfailures==15.0     # Автоматический перезапуск упавших тестов
pytest-xdist==3.6.1           # Параллельное выполнение тестов
swagger-coverage-tool==0.27.0  # Отслеживание покрытия API эндпоинтов
```

### Инструменты разработки:

```txt
ruff                           # Быстрый линтер и форматтер для Python
python-dotenv                  # Загрузка переменных окружения из .env файла
```

### Назначение библиотек:

- **pytest** - фундамент фреймворка, управление тестами, фикстурами, маркерами
- **httpx** - HTTP клиент с поддержкой event hooks для логирования и отладки
- **pydantic** - типизированные модели данных с автоматической валидацией
- **allure-pytest** - красивые отчёты с шагами, аттачментами и группировкой
- **swagger-coverage** - измерение покрытия API для выявления непротестированных эндпоинтов
- **Faker** - генерация реалистичных тестовых данных
- **ruff** - современная замена flake8, black, isort в одном инструменте

---

## Структура проекта

```
api-test-framework/
├── clients/                   # API клиенты и HTTP строители
│   ├── __init__.py
│   ├── api_client.py         # Базовый API клиент с Allure интеграцией
│   ├── api_coverage.py       # Настройка трекера покрытия API
│   ├── public_http_builder.py # HTTP клиент без аутентификации
│   ├── private_http_builder.py # HTTP клиент с Bearer токеном
│   ├── event_hooks.py        # Хуки для логирования и cURL генерации
│   ├── errors_schema.py      # Общие схемы ошибок API
│   ├── authentication/       # Домен: аутентификация
│   │   ├── __init__.py
│   │   ├── authentication_client.py  # Клиент для логина/refresh
│   │   └── authentication_schema.py  # Схемы токенов и запросов
│   ├── users/               # Домен: пользователи
│   │   ├── __init__.py
│   │   ├── public_users_client.py    # Публичные операции (регистрация)
│   │   ├── private_users_client.py   # Приватные операции (профиль)
│   │   └── users_schema.py           # Схемы пользователей
│   ├── courses/             # Домен: курсы
│   │   ├── __init__.py
│   │   ├── courses_client.py
│   │   └── courses_schema.py
│   ├── exercises/           # Домен: упражнения
│   │   ├── __init__.py
│   │   ├── exercises_client.py
│   │   └── exercises_schema.py
│   └── files/              # Домен: файлы
│       ├── __init__.py
│       ├── files_client.py
│       └── files_schema.py
├── fixtures/                # Pytest фикстуры для инъекции зависимостей
│   ├── __init__.py
│   ├── allure.py           # Настройки Allure отчётов
│   ├── authentication.py   # Фикстуры клиентов аутентификации
│   ├── users.py           # Фикстуры пользователей и их данных
│   ├── courses.py         # Фикстуры курсов
│   ├── exercises.py       # Фикстуры упражнений
│   └── files.py           # Фикстуры файлов
├── tests/                  # Тестовые модули
│   ├── __init__.py
│   ├── authentication/     # Тесты аутентификации
│   │   └── test_authentication.py
│   ├── users/             # Тесты пользователей
│   │   └── test_users.py
│   ├── courses/           # Тесты курсов
│   │   └── test_courses.py
│   ├── exercises/         # Тесты упражнений
│   │   └── test_exercises.py
│   └── files/            # Тесты файлов
│       └── test_files.py
├── tools/                 # Утилиты и вспомогательные модули
│   ├── __init__.py
│   ├── allure/           # Константы для Allure аннотаций
│   │   ├── __init__.py
│   │   ├── epics.py      # Эпики (высокоуровневые группы функций)
│   │   ├── features.py   # Фичи (группы тестов)
│   │   ├── stories.py    # Истории (типы операций)
│   │   ├── tag.py        # Теги для фильтрации тестов
│   │   └── environment.py # Переменные окружения для отчётов
│   ├── assertions/       # Кастомные проверки
│   │   ├── __init__.py
│   │   ├── base.py       # Базовые assertions (статус код, равенство)
│   │   ├── schema.py     # Валидация JSON схем
│   │   ├── authentication.py # Проверки аутентификации
│   │   ├── users.py      # Проверки пользователей
│   │   ├── courses.py    # Проверки курсов
│   │   ├── exercises.py  # Проверки упражнений
│   │   └── files.py      # Проверки файлов
│   ├── http/            # HTTP утилиты
│   │   ├── __init__.py
│   │   └── curl.py      # Генерация cURL команд из httpx Request
│   ├── fakers.py        # Обёртки над Faker для генерации тестовых данных
│   ├── logger.py        # Настройка логирования
│   └── routes.py        # Константы API маршрутов
├── testdata/            # Статические тестовые данные
│   └── files/
│       └── image.png    # Файл для тестирования загрузки
├── config.py            # Конфигурация приложения (pydantic-settings)
├── conftest.py         # Настройка pytest плагинов
├── pytest.ini         # Настройки pytest и маркеры
├── pyproject.toml      # Настройки ruff линтера
├── requirements.txt    # Python зависимости
├── .env.example       # Пример файла переменных окружения
├── CLAUDE.md          # Инструкции для Claude Code
└── README.md          # Документация проекта
```

### Принципы организации:

1. **Доменное разделение** - каждый API домен в отдельной папке
2. **Разделение публичного/приватного API** - разные клиенты для разных уровней доступа
3. **Модульность фикстур** - каждый домен имеет свои фикстуры
4. **Централизованные утилиты** - общие инструменты в папке tools
5. **Конфигурация в одном месте** - все настройки в config.py

---

## Базовые компоненты

### API Client (clients/api_client.py)

Базовый класс для всех API клиентов, предоставляющий стандартизированные HTTP методы с автоматической интеграцией Allure.

```python
from typing import Any
import allure
from httpx import URL, Client, QueryParams, Response
from httpx._types import RequestData, RequestFiles

class APIClient:
    def __init__(self, client: Client):
        """
        Базовый API клиент, принимающий настроенный httpx.Client.
        
        :param client: Экземпляр httpx.Client с настройками (URL, timeout, headers, hooks)
        """
        self.client = client

    @allure.step("Make GET request to {url}")
    def get(self, url: URL | str, params: QueryParams | None = None) -> Response:
        """
        Выполняет GET запрос с автоматическим логированием в Allure.
        
        :param url: URL эндпоинта
        :param params: Query параметры (?key=value)
        :return: httpx.Response объект
        """
        return self.client.get(url, params=params)

    @allure.step("Make POST request to {url}")
    def post(
        self,
        url: URL | str,
        json: Any | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
    ) -> Response:
        """
        Выполняет POST запрос с поддержкой JSON, form-data и file upload.
        
        :param url: URL эндпоинта
        :param json: Данные в формате JSON
        :param data: Form data (application/x-www-form-urlencoded)
        :param files: Файлы для загрузки
        :return: httpx.Response объект
        """
        return self.client.post(url, json=json, data=data, files=files)

    @allure.step("Make PATCH request to {url}")
    def patch(self, url: URL | str, json: Any | None = None) -> Response:
        """
        Выполняет PATCH запрос для частичного обновления данных.
        
        :param url: URL эндпоинта
        :param json: Данные для обновления в формате JSON
        :return: httpx.Response объект
        """
        return self.client.patch(url, json=json)

    @allure.step("Make DELETE request to {url}")
    def delete(self, url: URL | str) -> Response:
        """
        Выполняет DELETE запрос для удаления данных.
        
        :param url: URL эндпоинта
        :return: httpx.Response объект
        """
        return self.client.delete(url)
```

**Ключевые особенности:**

- **Allure интеграция** - каждый HTTP метод автоматически создаёт шаг в отчёте
- **Типизация** - полная поддержка type hints для лучшего DX
- **Гибкость** - поддержка всех основных HTTP методов
- **Абстракция** - скрывает детали httpx, предоставляя простой интерфейс

---

## Система конфигурации

### Конфигурация через Pydantic Settings (config.py)

Фреймворк использует `pydantic-settings` для управления конфигурацией через переменные окружения и `.env` файлы.

```python
from typing import Self
from pydantic import BaseModel, DirectoryPath, FilePath, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class HTTPClientConfig(BaseModel):
    """Конфигурация HTTP клиента."""
    url: HttpUrl          # Базовый URL API
    timeout: float        # Таймаут запросов в секундах
    
    @property
    def client_url(self) -> str:
        """Возвращает URL как строку для httpx.Client."""
        return str(self.url)

class TestDataConfig(BaseModel):
    """Конфигурация тестовых данных."""
    image_png_file: FilePath  # Путь к тестовому изображению

class Settings(BaseSettings):
    """Главный класс настроек приложения."""
    model_config = SettingsConfigDict(
        extra="allow",                    # Разрешить дополнительные поля
        env_file=".env",                 # Файл с переменными окружения
        env_file_encoding="utf-8",       # Кодировка .env файла
        env_nested_delimiter=".",        # Разделитель для вложенных полей
    )
    
    test_data: TestDataConfig           # Конфигурация тестовых данных
    http_client: HTTPClientConfig       # Конфигурация HTTP клиента
    allure_results_dir: DirectoryPath  # Папка для результатов Allure
    
    @classmethod
    def initialize(cls) -> Self:
        """
        Инициализирует настройки с созданием необходимых директорий.
        
        :return: Настроенный объект Settings
        """
        allure_results_dir = DirectoryPath("./allure-results")
        allure_results_dir.mkdir(exist_ok=True)
        return Settings(allure_results_dir=allure_results_dir)

# Глобальный объект настроек
settings = Settings.initialize()
```

### Пример .env файла:

```env
# HTTP Client Configuration
HTTP_CLIENT.URL=https://api.example.com
HTTP_CLIENT.TIMEOUT=30.0

# Test Data Configuration
TEST_DATA.IMAGE_PNG_FILE=./testdata/files/image.png

# Дополнительные настройки
DEBUG=true
LOG_LEVEL=INFO
```

### Преимущества pydantic-settings:

1. **Типизация** - автоматическая валидация типов данных
2. **Переменные окружения** - автоматическое чтение из ENV и .env файлов
3. **Вложенная структура** - поддержка сложных конфигураций
4. **Валидация** - проверка корректности URL, путей к файлам
5. **IDE поддержка** - автодополнение и проверка типов

---

## HTTP Builders

### Event Hooks (clients/event_hooks.py)

HTTP hooks обеспечивают автоматическое логирование и генерацию cURL команд для каждого запроса.

```python
import allure
from httpx import Request, Response
from tools.http.curl import make_curl_from_request
from tools.logger import get_logger

logger = get_logger("HTTP_CLIENT")

def curl_event_hook(request: Request):
    """
    Генерирует cURL команду и прикрепляет к Allure отчёту.
    
    Автоматически создаёт cURL команду из HTTP запроса и добавляет
    её как аттачмент в Allure отчёт для удобства отладки.
    
    :param request: HTTP запрос httpx
    """
    curl_command = make_curl_from_request(request)
    allure.attach(curl_command, "cURL command", allure.attachment_type.TEXT)

def log_request_event_hook(request: Request):
    """
    Логирует информацию об отправляемом HTTP запросе.
    
    :param request: HTTP запрос httpx
    """
    logger.info(f"Make {request.method} request to {request.url}")

def log_response_event_hook(response: Response):
    """
    Логирует информацию о полученном HTTP ответе.
    
    :param response: HTTP ответ httpx
    """
    logger.info(f"Got response {response.status_code} {response.reason_phrase} from {response.url}")
```

### Публичный HTTP Builder (clients/public_http_builder.py)

Создаёт HTTP клиент без аутентификации для публичных эндпоинтов.

```python
from httpx import Client
from clients.event_hooks import curl_event_hook, log_request_event_hook, log_response_event_hook
from config import settings

def get_public_http_client() -> Client:
    """
    Создаёт экземпляр httpx.Client для публичных API эндпоинтов.
    
    Клиент настроен с:
    - Базовым URL из конфигурации
    - Таймаутом из конфигурации
    - Event hooks для логирования и cURL генерации
    
    :return: Готовый к использованию httpx.Client
    """
    return Client(
        timeout=settings.http_client.timeout,
        base_url=settings.http_client.client_url,
        event_hooks={
            "request": [curl_event_hook, log_request_event_hook],
            "response": [log_response_event_hook]
        },
    )
```

### Приватный HTTP Builder (clients/private_http_builder.py)

Создаёт HTTP клиент с Bearer токеном для защищённых эндпоинтов.

```python
from functools import lru_cache
from httpx import Client
from pydantic import BaseModel
from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema
from clients.event_hooks import curl_event_hook, log_request_event_hook, log_response_event_hook
from config import settings

class AuthenticationUserSchema(BaseModel, frozen=True):
    """
    Схема пользователя для аутентификации.
    
    frozen=True делает объект неизменяемым, что необходимо для lru_cache.
    """
    email: str
    password: str

@lru_cache(maxsize=None)
def get_private_http_client(user: AuthenticationUserSchema) -> Client:
    """
    Создаёт аутентифицированный httpx.Client для приватных API эндпоинтов.
    
    Функция кэшируется для избежания повторных запросов аутентификации
    для одного и того же пользователя в рамках тестовой сессии.
    
    :param user: Данные пользователя для аутентификации
    :return: Аутентифицированный httpx.Client с Bearer токеном
    """
    # Получаем клиент аутентификации
    authentication_client = get_authentication_client()
    
    # Создаём запрос на логин
    login_request = LoginRequestSchema(email=user.email, password=user.password)
    
    # Выполняем аутентификацию
    login_response = authentication_client.login(login_request)
    
    # Создаём клиент с токеном в заголовках
    return Client(
        timeout=settings.http_client.timeout,
        base_url=settings.http_client.client_url,
        headers={"Authorization": f"Bearer {login_response.token.access_token}"},
        event_hooks={
            "request": [curl_event_hook, log_request_event_hook],
            "response": [log_response_event_hook],
        },
    )
```

### Преимущества архитектуры HTTP Builders:

1. **Разделение ответственности** - публичные и приватные клиенты
2. **Кэширование токенов** - избежание повторной аутентификации
3. **Автоматическое логирование** - все запросы автоматически логируются
4. **cURL генерация** - каждый запрос можно воспроизвести вручную
5. **Централизованная конфигурация** - все настройки в одном месте

---

## Схемы данных (Pydantic)

Pydantic схемы обеспечивают типизированную работу с данными API, автоматическую валидацию и сериализацию.

### Схемы аутентификации (clients/authentication/authentication_schema.py)

```python
from pydantic import BaseModel, Field
from tools.fakers import fake

class TokenSchema(BaseModel):
    """Структура токенов аутентификации."""
    token_type: str = Field(alias="tokenType")
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")

class LoginRequestSchema(BaseModel):
    """Структура запроса аутентификации."""
    email: str = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)

class LoginResponseSchema(BaseModel):
    """Структура ответа аутентификации."""
    token: TokenSchema

class RefreshRequestSchema(BaseModel):
    """Структура запроса обновления токена."""
    refresh_token: str = Field(alias="refreshToken", default_factory=fake.sentence)
```

### Схемы пользователей (clients/users/users_schema.py)

```python
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from tools.fakers import fake

class UserSchema(BaseModel):
    """Базовая структура пользователя."""
    model_config = ConfigDict(populate_by_name=True)
    
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName") 
    middle_name: str = Field(alias="middleName")

class CreateUserRequestSchema(BaseModel):
    """Структура запроса создания пользователя."""
    model_config = ConfigDict(populate_by_name=True)
    
    email: EmailStr = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)
    last_name: str = Field(alias="lastName", default_factory=fake.last_name)
    first_name: str = Field(alias="firstName", default_factory=fake.first_name)
    middle_name: str = Field(alias="middleName", default_factory=fake.middle_name)

class CreateUserResponseSchema(BaseModel):
    """Структура ответа создания пользователя."""
    user: UserSchema

class UpdateUserRequestSchema(BaseModel):
    """Структура запроса обновления пользователя."""
    model_config = ConfigDict(populate_by_name=True)
    
    email: EmailStr | None = Field(default_factory=fake.email)
    last_name: str | None = Field(alias="lastName", default_factory=fake.last_name)
    first_name: str | None = Field(alias="firstName", default_factory=fake.first_name)
    middle_name: str | None = Field(alias="middleName", default_factory=fake.middle_name)

class UpdateUserResponseSchema(BaseModel):
    """Структура ответа обновления пользователя."""
    user: UserSchema

class GetUserResponseSchema(BaseModel):
    """Структура ответа получения пользователя."""
    user: UserSchema
```

### Общие схемы ошибок (clients/errors_schema.py)

```python
from pydantic import BaseModel
from typing import List, Optional

class ErrorDetailSchema(BaseModel):
    """Детали ошибки."""
    field: Optional[str] = None
    message: str
    code: Optional[str] = None

class ErrorResponseSchema(BaseModel):
    """Стандартная структура ошибок API."""
    error: str
    message: str
    details: Optional[List[ErrorDetailSchema]] = None
    status_code: int
```

### Ключевые особенности Pydantic схем:

1. **Автоматическая валидация** - проверка типов при создании объектов
2. **Алиасы полей** - поддержка camelCase в API и snake_case в Python
3. **Default factories** - автоматическая генерация тестовых данных
4. **JSON схемы** - автоматическая генерация JSON Schema для валидации ответов
5. **Типизация** - полная поддержка type hints и IDE автодополнения

---

## Специализированные клиенты

### Клиент аутентификации (clients/authentication/authentication_client.py)

```python
import allure
from httpx import Response
from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.authentication.authentication_schema import (
    LoginRequestSchema, LoginResponseSchema, RefreshRequestSchema,
)
from clients.public_http_builder import get_public_http_client
from tools.routes import APIRoutes

class AuthenticationClient(APIClient):
    """Клиент для работы с эндпоинтами аутентификации /api/v1/authentication"""
    
    @allure.step("Authenticate user")
    @tracker.track_coverage_httpx(f"{APIRoutes.AUTHENTICATION}/login")
    def login_api(self, request: LoginRequestSchema) -> Response:
        """
        Выполняет запрос аутентификации пользователя.
        
        :param request: Данные для логина (email, password)
        :return: HTTP ответ с токенами аутентификации
        """
        return self.post(
            f"{APIRoutes.AUTHENTICATION}/login", 
            json=request.model_dump(by_alias=True)
        )
    
    @allure.step("Refresh authentication token")
    @tracker.track_coverage_httpx(f"{APIRoutes.AUTHENTICATION}/refresh")
    def refresh_api(self, request: RefreshRequestSchema) -> Response:
        """
        Выполняет запрос обновления токена аутентификации.
        
        :param request: Данные для refresh (refresh_token)
        :return: HTTP ответ с новыми токенами
        """
        return self.post(
            f"{APIRoutes.AUTHENTICATION}/refresh", 
            json=request.model_dump(by_alias=True)
        )
    
    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        """
        Удобный метод для аутентификации с автоматическим парсингом ответа.
        
        :param request: Данные для логина
        :return: Парсированный ответ с токенами
        """
        response = self.login_api(request)
        return LoginResponseSchema.model_validate_json(response.text)

def get_authentication_client() -> AuthenticationClient:
    """
    Фабричная функция для создания клиента аутентификации.
    
    :return: Настроенный клиент аутентификации
    """
    return AuthenticationClient(client=get_public_http_client())
```

### Публичный клиент пользователей (clients/users/public_users_client.py)

```python
import allure
from httpx import Response
from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.public_http_builder import get_public_http_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.routes import APIRoutes

class PublicUsersClient(APIClient):
    """Клиент для публичных операций с пользователями /api/v1/users"""
    
    @allure.step("Create user")
    @tracker.track_coverage_httpx(APIRoutes.USERS)
    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """
        Выполняет запрос создания нового пользователя.
        
        :param request: Данные нового пользователя
        :return: HTTP ответ с созданным пользователем
        """
        return self.post(APIRoutes.USERS, json=request.model_dump(by_alias=True))
    
    def create_user(self, request: CreateUserRequestSchema) -> CreateUserResponseSchema:
        """
        Удобный метод создания пользователя с парсингом ответа.
        
        :param request: Данные нового пользователя
        :return: Парсированный ответ с созданным пользователем
        """
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)

def get_public_users_client() -> PublicUsersClient:
    """Фабричная функция для создания публичного клиента пользователей."""
    return PublicUsersClient(client=get_public_http_client())
```

### Приватный клиент пользователей (clients/users/private_users_client.py)

```python
import allure
from httpx import Response
from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client
from clients.users.users_schema import (
    UpdateUserRequestSchema, UpdateUserResponseSchema, GetUserResponseSchema
)
from tools.routes import APIRoutes

class PrivateUsersClient(APIClient):
    """Клиент для приватных операций с пользователями (требует аутентификации)"""
    
    @allure.step("Get current user profile")
    @tracker.track_coverage_httpx(f"{APIRoutes.USERS}/me")
    def get_user_me_api(self) -> Response:
        """
        Получает профиль текущего аутентифицированного пользователя.
        
        :return: HTTP ответ с данными пользователя
        """
        return self.get(f"{APIRoutes.USERS}/me")
    
    @allure.step("Update current user profile")
    @tracker.track_coverage_httpx(f"{APIRoutes.USERS}/me")
    def update_user_me_api(self, request: UpdateUserRequestSchema) -> Response:
        """
        Обновляет профиль текущего пользователя.
        
        :param request: Данные для обновления
        :return: HTTP ответ с обновлённым пользователем
        """
        return self.patch(f"{APIRoutes.USERS}/me", json=request.model_dump(by_alias=True, exclude_none=True))
    
    @allure.step("Delete current user profile")
    @tracker.track_coverage_httpx(f"{APIRoutes.USERS}/me")
    def delete_user_me_api(self) -> Response:
        """
        Удаляет профиль текущего пользователя.
        
        :return: HTTP ответ подтверждения удаления
        """
        return self.delete(f"{APIRoutes.USERS}/me")
    
    def get_user_me(self) -> GetUserResponseSchema:
        """Удобный метод получения профиля с парсингом."""
        response = self.get_user_me_api()
        return GetUserResponseSchema.model_validate_json(response.text)
    
    def update_user_me(self, request: UpdateUserRequestSchema) -> UpdateUserResponseSchema:
        """Удобный метод обновления профиля с парсингом."""
        response = self.update_user_me_api(request)
        return UpdateUserResponseSchema.model_validate_json(response.text)

def get_private_users_client(user: AuthenticationUserSchema) -> PrivateUsersClient:
    """
    Фабричная функция для создания приватного клиента пользователей.
    
    :param user: Данные пользователя для аутентификации
    :return: Аутентифицированный клиент пользователей
    """
    return PrivateUsersClient(client=get_private_http_client(user))
```

### Паттерны специализированных клиентов:

1. **Наследование от APIClient** - все клиенты используют базовый функционал
2. **Двухуровневые методы** - `*_api()` возвращает Response, обычные методы - парсированные объекты
3. **Allure интеграция** - каждый метод автоматически становится шагом в отчёте
4. **Coverage tracking** - автоматическое отслеживание покрытия API
5. **Разделение публичного/приватного** - разные клиенты для разных уровней доступа
6. **Фабричные функции** - простое создание настроенных клиентов

---

## Система фикстур

Pytest фикстуры обеспечивают инъекцию зависимостей и управление жизненным циклом тестовых данных.

### Фикстуры аутентификации (fixtures/authentication.py)

```python
import pytest
from clients.authentication.authentication_client import (
    AuthenticationClient, get_authentication_client,
)

@pytest.fixture
def authentication_client() -> AuthenticationClient:
    """
    Предоставляет экземпляр клиента аутентификации.
    
    Создаёт и возвращает новый клиент аутентификации для API тестов.
    Фикстура функционального уровня - создаётся для каждого теста.
    
    :return: Экземпляр AuthenticationClient
    """
    return get_authentication_client()
```

### Фикстуры пользователей (fixtures/users.py)

```python
import pytest
from pydantic import BaseModel, EmailStr
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.private_users_client import PrivateUsersClient, get_private_users_client
from clients.users.public_users_client import PublicUsersClient, get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema

class UserFixture(BaseModel):
    """
    Обёртка для тестового пользователя, содержащая данные запроса и ответа.
    
    Предоставляет удобные свойства для доступа к данным пользователя
    и создания объектов для аутентификации.
    """
    request: CreateUserRequestSchema   # Данные, которые были отправлены при создании
    response: CreateUserResponseSchema # Данные, которые вернул сервер
    
    @property
    def email(self) -> EmailStr:
        """Email пользователя."""
        return self.request.email
    
    @property
    def password(self) -> str:
        """Пароль пользователя."""
        return self.request.password
    
    @property
    def authentication_user(self) -> AuthenticationUserSchema:
        """Объект для аутентификации пользователя."""
        return AuthenticationUserSchema(email=self.email, password=self.password)

@pytest.fixture
def public_users_client() -> PublicUsersClient:
    """
    Предоставляет экземпляр публичного клиента пользователей.
    
    :return: Экземпляр PublicUsersClient
    """
    return get_public_users_client()

@pytest.fixture
def function_user(public_users_client: PublicUsersClient) -> UserFixture:
    """
    Создаёт тестового пользователя для текущей тестовой функции.
    
    Генерирует нового пользователя для каждого теста, который его требует.
    Возвращает объект, содержащий как данные запроса, так и ответа.
    
    :param public_users_client: Клиент для создания пользователя
    :return: UserFixture с данными созданного пользователя
    """
    request = CreateUserRequestSchema()  # Автоматически генерирует тестовые данные
    response = public_users_client.create_user(request)
    return UserFixture(request=request, response=response)

@pytest.fixture
def private_users_client(function_user: UserFixture) -> PrivateUsersClient:
    """
    Предоставляет аутентифицированный приватный клиент пользователей.
    
    Создаёт клиент, используя учётные данные из фикстуры function_user.
    Автоматически выполняет аутентификацию и настраивает Bearer токен.
    
    :param function_user: Фикстура пользователя с учётными данными
    :return: Аутентифицированный экземпляр PrivateUsersClient
    """
    return get_private_users_client(function_user.authentication_user)
```

### Фикстуры Allure (fixtures/allure.py)

```python
import pytest
import allure
from config import settings

@pytest.fixture(scope="session", autouse=True)
def configure_allure():
    """
    Автоматическая настройка Allure для всей тестовой сессии.
    
    Устанавливает переменные окружения для Allure отчётов.
    autouse=True означает, что фикстура применяется автоматически.
    """
    # Настройка переменных окружения для Allure
    allure.environment(
        API_URL=settings.http_client.client_url,
        PYTHON_VERSION="3.12",
        FRAMEWORK="pytest + httpx + pydantic",
        ALLURE_VERSION="2.13.5"
    )
```

### Конфигурация фикстур (conftest.py)

```python
# Автоматическое подключение всех модулей фикстур
pytest_plugins = (
    "fixtures.users",
    "fixtures.files", 
    "fixtures.courses",
    "fixtures.authentication",
    "fixtures.exercises",
    "fixtures.allure",
)
```

### Преимущества системы фикстур:

1. **Автоматическое управление зависимостями** - pytest автоматически создаёт нужные объекты
2. **Изоляция тестов** - каждый тест получает свежие данные
3. **Переиспользование кода** - одна фикстура используется в множестве тестов
4. **Гибкие области видимости** - function, class, module, session
5. **Композиция** - фикстуры могут зависеть друг от друга

---

## Assertions и валидация

### Базовые assertions (tools/assertions/base.py)

```python
from typing import Any, Sized
import allure
from tools.logger import get_logger

logger = get_logger("BASE_ASSERTIONS")

@allure.step("Check that response status code equals to {expected}")
def assert_status_code(actual: int, expected: int):
    """
    Проверяет, что фактический статус код ответа соответствует ожидаемому.
    
    :param actual: Фактический статус код ответа
    :param expected: Ожидаемый статус код
    :raises AssertionError: Если статус коды не совпадают
    """
    logger.info(f"Check that response status code equals to {expected}")
    
    assert actual == expected, (
        f"Incorrect response status code. Expected: {expected}. Actual: {actual}"
    )

@allure.step("Check that {name} equals to {expected}")
def assert_equal(actual: Any, expected: Any, name: str):
    """
    Проверяет, что фактическое значение соответствует ожидаемому.
    
    :param actual: Фактическое значение
    :param expected: Ожидаемое значение
    :param name: Имя проверяемого значения для лучшего описания ошибки
    :raises AssertionError: Если значения не совпадают
    """
    logger.info(f'Check that "{name}" equals to {expected}')
    
    assert actual == expected, (
        f'Incorrect value: "{name}". Expected: {expected}. Actual: {actual}'
    )

@allure.step("Check that {name} is true")
def assert_is_true(actual: Any, name: str):
    """
    Проверяет, что значение является истинным.
    
    :param actual: Проверяемое значение
    :param name: Имя значения для описания ошибки
    :raises AssertionError: Если значение ложно
    """
    logger.info(f'Check that "{name}" is true')
    
    assert actual, f'Expected true value but got: {actual}'

def assert_length(actual: Sized, expected: Sized, name: str):
    """
    Проверяет, что длины двух объектов совпадают.
    
    :param actual: Фактический объект
    :param expected: Ожидаемый объект
    :param name: Имя объекта для описания ошибки
    :raises AssertionError: Если длины не совпадают
    """
    with allure.step(f"Check that length of {name} equals to {len(expected)}"):
        logger.info(f'Check that length of "{name}" equals to {len(expected)}')
        
        assert len(actual) == len(expected), (
            f'Incorrect object length: "{name}". '
            f"Expected length: {len(expected)}. "
            f"Actual length: {len(actual)}"
        )
```

### Валидация схем (tools/assertions/schema.py)

```python
from typing import Any
import allure
from jsonschema import validate
from jsonschema.validators import Draft202012Validator
from tools.logger import get_logger

logger = get_logger("SCHEMA_ASSERTIONS")

@allure.step("Validate JSON schema")
def validate_json_schema(instance: Any, schema: dict) -> None:
    """
    Валидирует JSON объект против JSON схемы.
    
    Использует Draft 2020-12 валидатор для проверки соответствия
    JSON данных заданной схеме с поддержкой форматов.
    
    :param instance: JSON данные для валидации
    :param schema: Ожидаемая JSON схема
    :raises ValidationError: Если данные не соответствуют схеме
    """
    logger.info("Validating JSON schema")
    
    validate(
        schema=schema,
        instance=instance,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )
```

### Доменные assertions пользователей (tools/assertions/users.py)

```python
import allure
from clients.users.users_schema import (
    CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
)
from tools.assertions.base import assert_equal

@allure.step("Check create user response")
def assert_create_user_response(
    request: CreateUserRequestSchema, 
    response: CreateUserResponseSchema
):
    """
    Проверяет корректность ответа создания пользователя.
    
    Сравнивает данные из запроса с данными в ответе,
    убеждаясь, что пользователь создан с правильными данными.
    
    :param request: Данные запроса создания пользователя
    :param response: Ответ сервера с созданным пользователем
    """
    assert_equal(response.user.email, request.email, "user email")
    assert_equal(response.user.first_name, request.first_name, "user first name")
    assert_equal(response.user.last_name, request.last_name, "user last name")
    assert_equal(response.user.middle_name, request.middle_name, "user middle name")

@allure.step("Check get user response")
def assert_get_user_response(
    response: GetUserResponseSchema, 
    expected: CreateUserResponseSchema
):
    """
    Проверяет корректность ответа получения пользователя.
    
    Сравнивает данные полученного пользователя с ожидаемыми данными.
    
    :param response: Ответ получения пользователя
    :param expected: Ожидаемые данные пользователя
    """
    assert_equal(response.user.id, expected.user.id, "user id")
    assert_equal(response.user.email, expected.user.email, "user email")
    assert_equal(response.user.first_name, expected.user.first_name, "user first name")
    assert_equal(response.user.last_name, expected.user.last_name, "user last name")
    assert_equal(response.user.middle_name, expected.user.middle_name, "user middle name")
```

### Паттерны assertions:

1. **Allure интеграция** - каждая проверка становится отдельным шагом
2. **Логирование** - все проверки записываются в лог
3. **Описательные ошибки** - понятные сообщения об ошибках
4. **Доменная специфичность** - отдельные assertions для каждого домена
5. **Композиция** - сложные проверки состоят из простых

---

## Allure интеграция

### Константы Allure (tools/allure/)

#### Эпики (tools/allure/epics.py)
```python
from enum import Enum

class AllureEpic(str, Enum):
    """Высокоуровневые группы функциональности."""
    LMS = "LMS service"
    STUDENT = "Student service"
    ADMINISTRATION = "Administration service"
```

#### Фичи (tools/allure/features.py)
```python
from enum import Enum

class AllureFeature(str, Enum):
    """Группы связанных тестов."""
    USERS = "Users"
    AUTHENTICATION = "Authentication"
    COURSES = "Courses"
    EXERCISES = "Exercises"
    FILES = "Files"
```

#### Истории (tools/allure/stories.py)
```python
from enum import Enum

class AllureStory(str, Enum):
    """Типы операций/сценариев."""
    CREATE_ENTITY = "Create entity"
    GET_ENTITY = "Get entity"
    UPDATE_ENTITY = "Update entity"
    DELETE_ENTITY = "Delete entity"
```

#### Теги (tools/allure/tag.py)
```python
from enum import Enum

class AllureTag(str, Enum):
    """Теги для фильтрации и группировки тестов."""
    CREATE_ENTITY = "create_entity"
    GET_ENTITY = "get_entity"
    UPDATE_ENTITY = "update_entity"
    DELETE_ENTITY = "delete_entity"
    POSITIVE = "positive"
    NEGATIVE = "negative"
```

### Coverage Tracking (clients/api_coverage.py)

```python
from swagger_coverage_tool import SwaggerCoverageTracker

# Глобальный трекер покрытия API для сервиса
tracker = SwaggerCoverageTracker(service="api-course")
```

### Использование Allure в тестах:

```python
@pytest.mark.users
@pytest.mark.regression
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.USERS)
@allure.sub_suite(AllureStory.CREATE_ENTITY)
@allure.tag(AllureTag.CREATE_ENTITY)
@allure.story(AllureStory.CREATE_ENTITY)
@allure.severity(Severity.BLOCKER)
@allure.title("Create user with valid data")
def test_create_user(self, public_users_client: PublicUsersClient):
    # Тест автоматически получает все Allure аннотации
    # HTTP запросы автоматически становятся шагами
    # cURL команды автоматически прикрепляются
    pass
```

### Автоматические возможности Allure:

1. **HTTP шаги** - каждый API вызов становится шагом в отчёте
2. **cURL команды** - автоматическое прикрепление для отладки
3. **Логи** - автоматическое прикрепление логов к упавшим тестам
4. **Скриншоты** - для UI тестов (при наличии)
5. **Иерархия тестов** - Epic → Feature → Story → Test
6. **Фильтрация** - по тегам, severity, маркерам

---

## Утилиты и инструменты

### Генератор тестовых данных (tools/fakers.py)

```python
from faker import Faker

class Fake:
    """
    Класс для генерации случайных тестовых данных с использованием Faker.
    
    Предоставляет методы для создания реалистичных тестовых данных
    различных типов с консистентными настройками.
    """
    
    def __init__(self, faker: Faker):
        """
        :param faker: Экземпляр класса Faker для генерации данных
        """
        self.faker = faker
    
    def text(self) -> str:
        """Генерирует случайный текст."""
        return self.faker.text()
    
    def uuid4(self) -> str:
        """Генерирует случайный UUID4."""
        return self.faker.uuid4()
    
    def email(self, domain: str | None = None) -> str:
        """
        Генерирует случайный email адрес.
        
        :param domain: Опциональный домен для email
        :return: Случайный email адрес
        """
        return self.faker.email(domain=domain)
    
    def sentence(self) -> str:
        """Генерирует случайное предложение."""
        return self.faker.sentence()
    
    def password(self) -> str:
        """Генерирует случайный пароль."""
        return self.faker.password()
    
    def last_name(self) -> str:
        """Генерирует случайную фамилию."""
        return self.faker.last_name()
    
    def first_name(self) -> str:
        """Генерирует случайное имя."""
        return self.faker.first_name()
    
    def middle_name(self) -> str:
        """Генерирует случайное отчество."""
        return self.faker.first_name()
    
    def estimated_time(self) -> str:
        """
        Генерирует строку с оценочным временем (например, "2 weeks").
        
        :return: Строка с оценочным временем
        """
        return f"{self.integer(1, 10)} weeks"
    
    def integer(self, start: int = 1, end: int = 100) -> int:
        """
        Генерирует случайное целое число в заданном диапазоне.
        
        :param start: Начало диапазона (включительно)
        :param end: Конец диапазона (включительно)
        :return: Случайное целое число
        """
        return self.faker.random_int(start, end)
    
    def max_score(self) -> int:
        """Генерирует случайный максимальный балл в диапазоне 50-100."""
        return self.integer(50, 100)
    
    def min_score(self) -> int:
        """Генерирует случайный минимальный балл в диапазоне 1-30."""
        return self.integer(1, 30)

# Глобальный экземпляр для использования в схемах и тестах
fake = Fake(faker=Faker())
```

### Система логирования (tools/logger.py)

```python
import logging

def get_logger(name: str) -> logging.Logger:
    """
    Создаёт и настраивает logger с консистентными настройками.
    
    Все логгеры в фреймворке используют одинаковый формат и уровень логирования.
    
    :param name: Имя логгера (обычно название модуля)
    :return: Настроенный logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Проверяем, не добавлены ли уже handlers (избегаем дублирования)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
    
    return logger
```

### cURL генератор (tools/http/curl.py)

```python
from httpx import Request, RequestNotRead

def make_curl_from_request(request: Request) -> str:
    """
    Генерирует cURL команду из httpx HTTP запроса.
    
    Создаёт cURL команду, которую можно скопировать и выполнить
    для воспроизведения HTTP запроса вручную.
    
    :param request: HTTP запрос от которого формируется cURL команда
    :return: Строка с cURL командой, содержащая метод, URL, заголовки и тело
    """
    result: list[str] = [f"curl -X '{request.method}'", f"'{request.url}'"]
    
    # Добавляем все заголовки
    for header, value in request.headers.items():
        result.append(f"-H '{header}: {value}'")
    
    # Добавляем тело запроса, если оно есть
    try:
        if body := request.content:
            result.append(f"-d '{body.decode('utf-8')}'")
    except RequestNotRead:
        # Тело запроса ещё не было прочитано
        pass
    
    # Форматируем команду с переносами строк для читаемости
    return " \\\n  ".join(result)
```

### API маршруты (tools/routes.py)

```python
from enum import Enum

class APIRoutes(str, Enum):
    """
    Централизованное хранение всех API маршрутов.
    
    Позволяет избежать дублирования строк и обеспечивает
    консистентность использования маршрутов по всему проекту.
    """
    USERS = "/api/v1/users"
    FILES = "/api/v1/files"
    COURSES = "/api/v1/courses"
    EXERCISES = "/api/v1/exercises"
    AUTHENTICATION = "/api/v1/authentication"
    
    def __str__(self):
        """Позволяет использовать enum как строку."""
        return self.value
```

---

## Примеры тестов

### Комплексный тест пользователей (tests/users/test_users.py)

```python
from http import HTTPStatus
import allure
import pytest
from allure_commons.types import Severity

from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import (
    CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema,
)
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tag import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response
from tools.fakers import fake

@pytest.mark.users
@pytest.mark.regression
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.USERS)
class TestUsers:
    """Тесты функциональности пользователей."""
    
    @pytest.mark.parametrize("domain", ["mail.ru", "gmail.com", "example.com"])
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Create user with email domain: {domain}")
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_user_with_different_domains(
        self,
        domain,
        public_users_client: PublicUsersClient,
    ):
        """
        Тест создания пользователя с различными доменами email.
        
        Проверяет, что система корректно обрабатывает email адреса
        с различными доменами при регистрации пользователей.
        """
        # Arrange - подготовка данных
        request = CreateUserRequestSchema(email=fake.email(domain=domain))
        
        # Act - выполнение действия
        response = public_users_client.create_user_api(request=request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)
        
        # Assert - проверка результатов
        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_user_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())
    
    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Get current user profile")
    @allure.sub_suite(AllureStory.GET_ENTITY)
    def test_get_user_me(
        self, 
        private_users_client: PrivateUsersClient, 
        function_user: UserFixture
    ):
        """
        Тест получения профиля текущего пользователя.
        
        Проверяет, что аутентифицированный пользователь может
        получить свой профиль через /users/me эндпоинт.
        """
        # Act
        response = private_users_client.get_user_me_api()
        response_data = GetUserResponseSchema.model_validate_json(response.text)
        
        # Assert
        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        assert_get_user_response(response_data, function_user.response)
        validate_json_schema(
            instance=response.json(), 
            schema=response_data.model_json_schema()
        )
    
    @allure.tag(AllureTag.NEGATIVE)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Create user with invalid email")
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_user_invalid_email_negative(
        self,
        public_users_client: PublicUsersClient,
    ):
        """
        Негативный тест создания пользователя с некорректным email.
        
        Проверяет, что система правильно валидирует email адрес
        и возвращает ошибку для некорректных значений.
        """
        # Arrange
        request = CreateUserRequestSchema(email="invalid-email")
        
        # Act
        response = public_users_client.create_user_api(request=request)
        
        # Assert
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
```

### Тест аутентификации (tests/authentication/test_authentication.py)

```python
from http import HTTPStatus
import allure
import pytest
from allure_commons.types import Severity

from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import (
    LoginRequestSchema, LoginResponseSchema
)
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tag import AllureTag
from tools.assertions.base import assert_status_code, assert_is_true
from tools.assertions.schema import validate_json_schema

@pytest.mark.authentication
@pytest.mark.smoke
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTHENTICATION)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.AUTHENTICATION)
class TestAuthentication:
    """Тесты аутентификации пользователей."""
    
    @allure.tag(AllureTag.POSITIVE)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Login with valid credentials")
    @allure.sub_suite(AllureStory.GET_ENTITY)
    def test_login_valid_credentials(
        self,
        authentication_client: AuthenticationClient,
        function_user: UserFixture,
    ):
        """
        Тест успешной аутентификации с валидными учётными данными.
        
        Проверяет, что пользователь может войти в систему,
        используя корректные email и пароль.
        """
        # Arrange
        login_request = LoginRequestSchema(
            email=function_user.email,
            password=function_user.password
        )
        
        # Act
        response = authentication_client.login_api(login_request)
        response_data = LoginResponseSchema.model_validate_json(response.text)
        
        # Assert
        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_is_true(response_data.token.access_token, "access token")
        assert_is_true(response_data.token.refresh_token, "refresh token")
        validate_json_schema(response.json(), response_data.model_json_schema())
```

---

## Конфигурационные файлы

### pytest.ini

```ini
[pytest]
# Паттерны для поиска тестовых файлов
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Опции запуска по умолчанию
addopts = -s -v --tb=short

# Директории с тестами
testpaths = tests

# Маркеры для группировки тестов
markers =
    authentication: authentication tests
    regression: regression tests
    smoke: smoke tests
    users: users tests
    files: files tests
    courses: courses tests
    exercises: exercises tests
```

### pyproject.toml (конфигурация ruff)

```toml
[tool.ruff]
# Увеличиваем длину строки до 100 символов
line-length = 100

# Исключаем директории из проверки
exclude = [
    ".git",
    "__pycache__",
    ".venv",
    ".pytest_cache",
    "allure-results",
    "temp",
]

# Целевая версия Python
target-version = "py312"

[tool.ruff.lint]
# Включаем основные правила линтинга
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "N",  # pep8-naming
    "UP", # pyupgrade
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
]

# Игнорируем специфичные правила
ignore = [
    "E501",  # line too long (handled by line-length)
]

[tool.ruff.format]
# Настройки форматирования (аналогично Black)
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

[tool.ruff.lint.isort]
# Конфигурация сортировки импортов
known-first-party = ["clients", "tools", "fixtures", "tests"]
```

### conftest.py (конфигурация pytest)

```python
# Автоматическое подключение всех модулей фикстур
pytest_plugins = (
    "fixtures.users",
    "fixtures.files",
    "fixtures.courses",
    "fixtures.authentication",
    "fixtures.exercises",
    "fixtures.allure",
)
```

### .env.example (пример переменных окружения)

```env
# HTTP Client Configuration
HTTP_CLIENT.URL=https://api.example.com
HTTP_CLIENT.TIMEOUT=30.0

# Test Data Configuration
TEST_DATA.IMAGE_PNG_FILE=./testdata/files/image.png

# Swagger Coverage Configuration
SWAGGER_COVERAGE_SERVICE=api-course

# Optional Debug Settings
DEBUG=false
LOG_LEVEL=INFO

# CI/CD Specific
CI=false
ALLURE_RESULTS_DIR=./allure-results
```

---

## Команды и workflow

### Основные команды для разработки

#### Запуск тестов:
```bash
# Запуск всех тестов
pytest

# Запуск с подробным выводом
pytest -v

# Запуск конкретного модуля
pytest tests/authentication/

# Запуск по маркерам
pytest -m smoke                    # Smoke тесты
pytest -m regression               # Regression тесты
pytest -m "authentication and regression"  # Комбинация маркеров

# Запуск с повторами при падении
pytest --reruns 2

# Параллельный запуск
pytest -n auto                     # Автоматическое определение кол-ва процессов
pytest -n 4                        # Запуск в 4 процесса

# Запуск конкретного теста
pytest tests/users/test_users.py::TestUsers::test_create_user

# Запуск с фильтрацией по имени
pytest -k "create_user"            # Все тесты, содержащие "create_user"
```

#### Линтинг и форматирование:
```bash
# Проверка кода линтером
ruff check

# Автоматическое исправление проблем
ruff check --fix

# Форматирование кода
ruff format

# Проверка конкретной папки
ruff check clients/
ruff format tests/
```

#### Отчёты:
```bash
# Генерация и открытие Allure отчёта
allure serve allure-results

# Генерация отчёта в папку
allure generate allure-results --output allure-report

# Очистка результатов
rm -rf allure-results/*
```

#### Управление зависимостями:
```bash
# Установка зависимостей
pip install -r requirements.txt

# Обновление requirements.txt
pip freeze > requirements.txt

# Создание виртуального окружения
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### CI/CD интеграция

#### GitHub Actions workflow пример:
```yaml
name: API Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python 3.12
      uses: actions/setup-python@v4
      with:
        python-version: "3.12"
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Lint with ruff
      run: |
        ruff check
        ruff format --check
    
    - name: Run smoke tests
      run: |
        pytest -m smoke --alluredir=allure-results
      env:
        HTTP_CLIENT.URL: ${{ secrets.API_URL }}
        HTTP_CLIENT.TIMEOUT: 30.0
    
    - name: Run regression tests
      if: github.event_name == 'push'
      run: |
        pytest -m regression --alluredir=allure-results
      env:
        HTTP_CLIENT.URL: ${{ secrets.API_URL }}
        HTTP_CLIENT.TIMEOUT: 30.0
    
    - name: Upload Allure results
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: allure-results
        path: allure-results/
    
    - name: Upload coverage results
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: coverage-results
        path: coverage-results/
```

### Workflow для разработки

#### 1. Настройка окружения:
```bash
# Клонирование репозитория
git clone <repository-url>
cd api-test-framework

# Создание виртуального окружения
python -m venv .venv
source .venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Копирование и настройка переменных окружения
cp .env.example .env
# Редактирование .env файла с реальными настройками
```

#### 2. Разработка новых тестов:
```bash
# Создание ветки для фичи
git checkout -b feature/new-api-tests

# Написание тестов
# Запуск локальных проверок
ruff check --fix
ruff format
pytest -m smoke

# Коммит изменений
git add .
git commit -m "Add new API tests for feature X"
git push origin feature/new-api-tests
```

#### 3. Отладка тестов:
```bash
# Запуск конкретного теста с подробным выводом
pytest -v -s tests/users/test_users.py::TestUsers::test_create_user

# Запуск с остановкой на первой ошибке
pytest -x

# Запуск с отладчиком
pytest --pdb

# Просмотр логов
tail -f pytest.log
```

---

## Расширение фреймворка

### Добавление нового API домена

#### Шаг 1: Создание структуры клиента
```bash
# Создание директории для нового домена
mkdir -p clients/orders
touch clients/orders/__init__.py
touch clients/orders/orders_client.py
touch clients/orders/orders_schema.py
```

#### Шаг 2: Создание схем данных (clients/orders/orders_schema.py)
```python
from pydantic import BaseModel, Field
from tools.fakers import fake
from typing import Optional
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class OrderSchema(BaseModel):
    id: str
    user_id: str = Field(alias="userId")
    status: OrderStatus
    total_amount: float = Field(alias="totalAmount")
    created_at: str = Field(alias="createdAt")

class CreateOrderRequestSchema(BaseModel):
    user_id: str = Field(alias="userId", default_factory=fake.uuid4)
    items: list[str] = Field(default_factory=lambda: [fake.uuid4()])
    total_amount: float = Field(alias="totalAmount", default_factory=lambda: fake.integer(10, 1000))

class CreateOrderResponseSchema(BaseModel):
    order: OrderSchema

class GetOrderResponseSchema(BaseModel):
    order: OrderSchema

class UpdateOrderRequestSchema(BaseModel):
    status: Optional[OrderStatus] = None
    total_amount: Optional[float] = Field(alias="totalAmount", default=None)
```

#### Шаг 3: Создание клиента (clients/orders/orders_client.py)
```python
import allure
from httpx import Response
from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client
from clients.orders.orders_schema import (
    CreateOrderRequestSchema, CreateOrderResponseSchema,
    GetOrderResponseSchema, UpdateOrderRequestSchema
)
from tools.routes import APIRoutes

class OrdersClient(APIClient):
    """Клиент для работы с заказами."""
    
    @allure.step("Create order")
    @tracker.track_coverage_httpx(APIRoutes.ORDERS)
    def create_order_api(self, request: CreateOrderRequestSchema) -> Response:
        return self.post(APIRoutes.ORDERS, json=request.model_dump(by_alias=True))
    
    @allure.step("Get order by ID")
    @tracker.track_coverage_httpx(f"{APIRoutes.ORDERS}/{{order_id}}")
    def get_order_api(self, order_id: str) -> Response:
        return self.get(f"{APIRoutes.ORDERS}/{order_id}")
    
    @allure.step("Update order")
    @tracker.track_coverage_httpx(f"{APIRoutes.ORDERS}/{{order_id}}")
    def update_order_api(self, order_id: str, request: UpdateOrderRequestSchema) -> Response:
        return self.patch(
            f"{APIRoutes.ORDERS}/{order_id}", 
            json=request.model_dump(by_alias=True, exclude_none=True)
        )
    
    def create_order(self, request: CreateOrderRequestSchema) -> CreateOrderResponseSchema:
        response = self.create_order_api(request)
        return CreateOrderResponseSchema.model_validate_json(response.text)
    
    def get_order(self, order_id: str) -> GetOrderResponseSchema:
        response = self.get_order_api(order_id)
        return GetOrderResponseSchema.model_validate_json(response.text)

def get_orders_client(user: AuthenticationUserSchema) -> OrdersClient:
    return OrdersClient(client=get_private_http_client(user))
```

#### Шаг 4: Обновление маршрутов (tools/routes.py)
```python
class APIRoutes(str, Enum):
    USERS = "/api/v1/users"
    FILES = "/api/v1/files"
    COURSES = "/api/v1/courses"
    EXERCISES = "/api/v1/exercises"
    AUTHENTICATION = "/api/v1/authentication"
    ORDERS = "/api/v1/orders"  # Новый маршрут
```

#### Шаг 5: Создание фикстур (fixtures/orders.py)
```python
import pytest
from pydantic import BaseModel
from clients.orders.orders_client import OrdersClient, get_orders_client
from clients.orders.orders_schema import CreateOrderRequestSchema, CreateOrderResponseSchema
from fixtures.users import UserFixture

class OrderFixture(BaseModel):
    request: CreateOrderRequestSchema
    response: CreateOrderResponseSchema
    
    @property
    def order_id(self) -> str:
        return self.response.order.id

@pytest.fixture
def orders_client(function_user: UserFixture) -> OrdersClient:
    return get_orders_client(function_user.authentication_user)

@pytest.fixture
def function_order(orders_client: OrdersClient) -> OrderFixture:
    request = CreateOrderRequestSchema()
    response = orders_client.create_order(request)
    return OrderFixture(request=request, response=response)
```

#### Шаг 6: Создание assertions (tools/assertions/orders.py)
```python
import allure
from clients.orders.orders_schema import (
    CreateOrderRequestSchema, CreateOrderResponseSchema, OrderStatus
)
from tools.assertions.base import assert_equal

@allure.step("Check create order response")
def assert_create_order_response(
    request: CreateOrderRequestSchema,
    response: CreateOrderResponseSchema
):
    assert_equal(response.order.user_id, request.user_id, "order user_id")
    assert_equal(response.order.total_amount, request.total_amount, "order total_amount")
    assert_equal(response.order.status, OrderStatus.PENDING, "order status")
```

#### Шаг 7: Создание тестов (tests/orders/test_orders.py)
```python
from http import HTTPStatus
import allure
import pytest
from allure_commons.types import Severity

from clients.orders.orders_client import OrdersClient
from clients.orders.orders_schema import CreateOrderRequestSchema, CreateOrderResponseSchema
from fixtures.orders import OrderFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tag import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.orders import assert_create_order_response

@pytest.mark.orders
@pytest.mark.regression
@allure.epic(AllureEpic.LMS)
@allure.feature("Orders")
@allure.parent_suite(AllureEpic.LMS)
@allure.suite("Orders")
class TestOrders:
    
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Create order")
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_order(self, orders_client: OrdersClient):
        request = CreateOrderRequestSchema()
        response = orders_client.create_order_api(request)
        response_data = CreateOrderResponseSchema.model_validate_json(response.text)
        
        assert_status_code(response.status_code, HTTPStatus.CREATED)
        assert_create_order_response(request, response_data)
```

#### Шаг 8: Обновление конфигурации
```python
# conftest.py - добавление новой фикстуры
pytest_plugins = (
    "fixtures.users",
    "fixtures.files",
    "fixtures.courses",
    "fixtures.authentication",
    "fixtures.exercises",
    "fixtures.orders",  # Новая фикстура
    "fixtures.allure",
)

# pytest.ini - добавление нового маркера
markers =
    authentication: authentication tests
    regression: regression tests
    smoke: smoke tests
    users: users tests
    files: files tests
    courses: courses tests
    exercises: exercises tests
    orders: orders tests  # Новый маркер
```

### Добавление новых типов assertions

#### Создание специализированных проверок (tools/assertions/performance.py):
```python
import time
import allure
from typing import Callable, Any
from tools.logger import get_logger

logger = get_logger("PERFORMANCE_ASSERTIONS")

@allure.step("Check response time is less than {max_time_ms}ms")
def assert_response_time(response_func: Callable, max_time_ms: int, *args, **kwargs) -> Any:
    """
    Проверяет, что время ответа не превышает заданное значение.
    
    :param response_func: Функция, выполняющая запрос
    :param max_time_ms: Максимальное время ответа в миллисекундах
    :return: Результат выполнения функции
    """
    start_time = time.time()
    result = response_func(*args, **kwargs)
    end_time = time.time()
    
    actual_time_ms = (end_time - start_time) * 1000
    
    logger.info(f"Response time: {actual_time_ms:.2f}ms")
    
    assert actual_time_ms <= max_time_ms, (
        f"Response time {actual_time_ms:.2f}ms exceeds maximum {max_time_ms}ms"
    )
    
    return result
```

### Интеграция с внешними системами

#### Пример интеграции с базой данных (tools/database/):
```python
# tools/database/connection.py
import psycopg2
from contextlib import contextmanager
from tools.logger import get_logger

logger = get_logger("DATABASE")

@contextmanager
def get_db_connection():
    """Контекстный менеджер для подключения к БД."""
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="test_db", 
            user="test_user",
            password="test_password"
        )
        yield conn
    finally:
        if conn:
            conn.close()

# tools/database/queries.py
def get_user_by_email(email: str) -> dict:
    """Получает пользователя из БД по email."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        return cursor.fetchone()
```

### Лучшие практики расширения:

1. **Консистентность** - следуйте существующим паттернам
2. **Тестирование** - каждый новый компонент должен быть протестирован
3. **Документация** - обновляйте README и комментарии
4. **Линтинг** - проверяйте код с помощью ruff
5. **Обратная совместимость** - не ломайте существующий API
6. **Модульность** - новые компоненты должны быть независимыми
7. **Конфигурация** - выносите настройки в config.py или .env

---

## Заключение

Данный фреймворк автотестов API представляет собой комплексное решение для автоматизированного тестирования веб-сервисов. Он обеспечивает:

### Ключевые преимущества:

1. **Модульная архитектура** - легко расширяемая и поддерживаемая
2. **Типизация** - полная поддержка type hints для безопасности разработки
3. **Автоматизация** - минимум ручной работы, максимум автоматических проверок
4. **Отчётность** - детальные Allure отчёты с визуализацией
5. **Покрытие API** - автоматическое отслеживание тестируемых эндпоинтов
6. **Масштабируемость** - простое добавление новых доменов и функций

### Применение:

Фреймворк подходит для:
- Тестирования REST API
- Регрессионного тестирования
- Smoke тестирования в CI/CD
- Нагрузочного тестирования (с расширениями)
- Интеграционного тестирования

### Дальнейшее развитие:

- Добавление поддержки GraphQL
- Интеграция с системами мониторинга
- Расширение coverage анализа
- Добавление UI тестов с Playwright
- Интеграция с системами управления тестами

Этот фреймворк служит надёжной основой для создания качественных автотестов API и может быть адаптирован под различные проекты и требования.
