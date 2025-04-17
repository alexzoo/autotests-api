from typing import Any

from jsonschema import validate
from jsonschema.validators import Draft202012Validator


def validate_json_schema(instance: Any, schema: dict) -> None:
    """
    Validates if a JSON object (instance) conforms to the given JSON schema.

    :param instance: The JSON data to validate.
    :param schema: The expected JSON schema.
    :raises jsonschema.exceptions.ValidationError: If the instance doesn't conform to the schema.
    """
    validate(
        schema=schema,
        instance=instance,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )
