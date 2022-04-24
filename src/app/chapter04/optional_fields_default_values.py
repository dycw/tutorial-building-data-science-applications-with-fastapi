from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserProfile(BaseModel):
    nickname: str
    location: Optional[str] = None
    subscribed_newsletter: bool = True


class Model(BaseModel):
    d: datetime = datetime.now()
