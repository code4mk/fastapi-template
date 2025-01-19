from fastapi import Request
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, ValidationError
from sqlalchemy import desc


async def validate_data(data: Dict[str, Any], model: BaseModel) -> Dict[str, Union[str, Dict[str, Any]]]:
    output = {'status': 'valid'}
    
    try:
        instance = model(**data)
        output['data'] = instance.dict()
    except ValidationError as e:
        # If validation fails, return status as invalid and the validation errors
        output['status'] = 'invalid'
        output['errors'] = e.errors()
        
    return output
    
def app_path(path_name = None):
    from pathlib import Path
    the_path = str(Path(__file__).parent.parent)
    
    if path_name:
        the_path = f'{the_path}/{path_name}'
        
    return the_path