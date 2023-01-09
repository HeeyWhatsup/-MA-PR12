from pydantic import BaseModel

class CreateMusic(BaseModel):
    name: str
    datasozd: str

class Music:
    def __init__(self, id: int, name: str, datasozd: str) -> None:
        self.id = id
        self.name = name
        self.datasozd = datasozd