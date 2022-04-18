from datetime import datetime

from pydantic import BaseModel


class UserProfile(BaseModel):
    nickname: str
    location: str | None = None
    subscribed_newsletter: bool = True


class Model(BaseModel):
    d: datetime = datetime.now()
