from pydantic import BaseModel
from typing import Optional, Dict

class PaginationLinks(BaseModel):
    self: Dict[str, str]
    next: Optional[Dict[str, str]] = None
    prev: Optional[Dict[str, str]] = None