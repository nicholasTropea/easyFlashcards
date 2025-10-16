from pydantic import BaseModel

class FolderCreate(BaseModel):
    name: str

class FolderRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True