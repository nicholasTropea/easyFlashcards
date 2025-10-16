from pydantic import BaseModel

class FlashcardCreate(BaseModel):
    question: str
    answer: str

class FlashcardRead(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        from_attributes = True