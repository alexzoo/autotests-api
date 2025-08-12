from enum import Enum


class APIRoutes(str, Enum):
    USERS = "/api/v1/users"
    FILES = "/api/v1/files"
    COURSES = "/api/v1/courses"
    EXERCISES = "/api/v1/exercises"
    AUTHENTICATION = "/api/v1/authentication"

    def __str__(self):
        return self.value
