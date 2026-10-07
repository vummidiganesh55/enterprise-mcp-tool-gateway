from dataclasses import dataclass
from typing import Optional


@dataclass
class RequestContext:
    request_id: str
    user_id: Optional[str] = None
    roles: Optional[list[str]] = None