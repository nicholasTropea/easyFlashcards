from sqlmodel import SQLModel, Field, Relationship, create_engine
from typing import Optional, List

# Defines the users table
class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    hashed_password: str

    folders: List["Folders"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete"} # When a user is deleted, all of its folders are too
    )

# Defines the folders table
class Folders(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    user_id: Optional[int] = Field(default=None, foreign_key="users.id")

    user: Optional[Users] = Relationship(back_populates="folders")
    flashcards: List["Flashcards"] = Relationship(
        back_populates="folder",
        sa_relationship_kwargs={"cascade": "all, delete"} # When a folder is deleted, all of its flashcards are too
    )

# Defines the flashcards table
class Flashcards(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str
    answer: str

    folder_id: Optional[int] = Field(default=None, foreign_key="folders.id") 

    folder: Optional[Folders] = Relationship(back_populates="flashcards")


# Creates the SQLite database file
engine = create_engine("sqlite:///flashcards.db")

# Creates tables
def create_db():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db()
    print("Database created: flashcards.db")