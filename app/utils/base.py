from fastapi import Request
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, ValidationError
from sqlalchemy import desc

async def the_query(request: Request, name = None) -> Dict[str, str]:
    data = {}
    
    if request.query_params:
        data =  request.query_params
    elif request.headers.get("Content-Type") == "application/json":
        data = await request.json()
    else:
        data = await request.form()
    
    if name:
      return data.get(name)
    else:
      return data


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


def the_sorting(request, query):
    """Sort a SQLAlchemy query based on query parameters.
    
    Example:
        # For a request with URL: /api/items?sort=name,-created_at
        # This will sort by name (ascending) and created_at (descending)
    """
    sort_params = request.query_params.get("sort")
    
    if sort_params:
        sort_fields = sort_params.split(",")
        ordering = []
        for field in sort_fields:
            if field.startswith("-"):
                ordering.append(desc(field[1:]))
            else:
                ordering.append(field)
        query = query.order_by(*ordering)
        
    return query
    
def app_path(path_name = None):
    from pathlib import Path
    the_path = str(Path(__file__).parent.parent)
    
    if path_name:
        the_path = f'{the_path}/{path_name}'
        
    return the_path