from typing import Union
from uuid import UUID as _UUID

def normalize_uuid(value: Union[str, _UUID]) -> _UUID:
    if isinstance(value, _UUID):
        return value
    return _UUID(value)  # ValueError если строка не UUID
