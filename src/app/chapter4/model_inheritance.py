from pydantic import BaseModel


class PostCreate1(BaseModel):
    title: str
    content: str


class PostPublic1(BaseModel):
    id: int
    title: str
    content: str


class PostDB1(BaseModel):
    id: int
    title: str
    content: str
    nb_views: int = 0


class PostBase2(BaseModel):
    title: str
    content: str


class PostCreate2(PostBase2):
    pass


class PostPublic2(PostBase2):
    id: int


class PostDB2(PostBase2):
    id: int
    nb_views: int = 0


class PostBase3(BaseModel):
    title: str
    content: str

    def excerpt(self) -> str:
        return f"{self.content[:140]}..."


class PostCreate3(PostBase3):
    pass


class PostPublic3(PostBase3):
    id: int


class PostDB3(PostBase3):
    id: int
    nb_views: int = 0
