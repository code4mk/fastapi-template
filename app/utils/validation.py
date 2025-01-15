from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from functools import wraps
from app.utils.base import the_query
from app.utils.exceptions import ValidationException, BadRequestException

def dto(schema: BaseModel):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            try:
                request_data = await the_query(request)
                validated_data = schema(**request_data)
                request.state.validated_data = validated_data
                return await func(request, *args, **kwargs)
            except ValidationError as e:
                errors = {}
                for error in e.errors():
                    field = error['loc'][0]
                    message = field + " " + error['msg']
                    if field not in errors:
                        errors[field] = []
                    errors[field].append(message)
                raise ValidationException(errors=errors)
            except ValueError:
                raise BadRequestException(message="Invalid JSON")
            
        return wrapper
    return decorator

__all__ = ['dto', 'setup_exception_handlers']