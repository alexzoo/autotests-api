from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.exercises.exercises_client import get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from tools.fakers import get_random_email


public_users_client = get_public_users_client()

# create user
create_user_request = CreateUserRequestSchema(
    email=get_random_email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string"
)

create_user_response = public_users_client.create_user(create_user_request)

# initialize clients
authentication_user = AuthenticationUserSchema(
    email=create_user_request.email,
    password=create_user_request.password
)

files_client = get_files_client(authentication_user)
courses_client = get_courses_client(authentication_user)
exercise_client = get_exercises_client(user=authentication_user)

# upload file
create_file_request = CreateFileRequestSchema(
    filename="image.png",
    directory="courses",
    upload_file="/Users/zubescu/my_projects/autotests-api/testdata/files/image.png"
)
create_file_response = files_client.create_file(create_file_request)
print('Create file data: ', create_file_response)

# create course
create_course_request = CreateCourseRequestSchema(
    title="Python",
    max_score=100,
    min_score=10,
    description="Python api course",
    estimated_time="2 weeks",
    preview_file_id=create_file_response.file.id,
    created_by_user_id=create_user_response.user.id
)
create_course_response = courses_client.create_course(create_course_request)
print('Create course data: ', create_course_response)

# create exercise
create_exercise_request = CreateExerciseRequestSchema(
    title="Test exercise",
    course_id=create_course_response.course.id,
    max_score=100,
    min_score=10,
    order_index=0,
    description="Test description",
    estimated_time="string"
)
create_exercise_response = exercise_client.create_exercise(request=create_exercise_request)
print('Create exercise data: ', create_exercise_response)
