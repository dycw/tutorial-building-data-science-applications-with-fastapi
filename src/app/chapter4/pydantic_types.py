from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import HttpUrl


class User(BaseModel):
    email: EmailStr
    website: HttpUrl
