from dataclasses import dataclass
from dataclasses import field

from chapter03.project.models.post import Post
from chapter03.project.models.user import User


@dataclass
class DummyDatabase:
    users: dict[int, User] = field(default_factory=dict)
    posts: dict[int, Post] = field(default_factory=dict)


db = DummyDatabase()
