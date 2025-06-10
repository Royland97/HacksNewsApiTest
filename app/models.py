from pydantic import BaseModel

class News(BaseModel):
    title: str
    url: str
    points: int
    author: str
    published: str
    comments: int
