from typing import Any, Optional

from pydantic import BaseModel


class ActionResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None
