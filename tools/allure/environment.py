from config import settings


def create_allure_environment_file():
    items = [f'{key} = {value}' for key, value in settings.model_dump().items()]
    properties = '\n'.join(items)

    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w+') as file:
        file.write(properties)
