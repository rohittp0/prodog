import json
from typing import TypeVar, Type

from drf_yasg import openapi
from pydantic import BaseModel
from pydantic_core import ValidationError
from rest_framework.exceptions import ParseError
from rest_framework.request import Request


def get_api_responses(description, serializer=None, code=200):
    return {
        code: openapi.Response(description=description, schema=serializer if serializer is not None else None),
        400: openapi.Response(description="Invalid parameters provided."),
        401: openapi.Response(description="Unauthorized access."),
        500: openapi.Response(description="Internal server error."),
    }


T = TypeVar('T', bound=BaseModel)

def validate_request(request: Request, model_class: Type[T], location: str = "query") -> T:
    try:
        if location == "query":
            data = dict(request.query_params.items())
        elif location == "body":
            data = request.data
        else:
            raise ValueError(f"Invalid location: {location}")

        return model_class.model_validate(data)
    except ValidationError as e:
        raise ParseError(detail=json.loads(e.json()))