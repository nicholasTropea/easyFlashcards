from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import engine, Users, Folders, Flashcards, create_db, SQLModel
from pydantic import BaseModel

# Creates the web app and listens for HTTP requests
app = FastAPI()

# Makes sure the database exists when the app starts
create_db()

# Creates a temporary connection to the database and closes it after each request
def get_session():
    with Session(engine) as session:
        yield session


# Models to send requests as JSON
class UserCreate(BaseModel):
    email: str
    password: str

class FolderCreate(BaseModel):
    name: str

class FlashcardCreate(BaseModel):
    question: str
    answer: str


# Development debugging only
@app.post("/reset-db")
def reset_database():
    # Drop all tables
    SQLModel.metadata.drop_all(engine)
    # Recreate tables
    SQLModel.metadata.create_all(engine)
    return {"message": "Database has been reset!"}

@app.get("/")
def root():
    return {"message": "Welcome to EasyFlashcards!"}

# Create new user
@app.post("/users/")
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    # Checks for users with same email
    existing_user = session.exec(select(Users).where(Users.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    user = Users(
        email=user_data.email,
        password=user_data.password
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Create new folder
@app.post("/users/{user_id}/folders")
def create_folder(
    user_id: int,
    folder_data: FolderCreate,
    session: Session = Depends(get_session)
):
    # Checks for folders with same name under the same user
    existing_folder = session.exec(
        select(Folders).where(
            (Folders.user_id == user_id) & (folder_data.name == Folders.name)
        )
    ).first()
    if existing_folder:
        raise HTTPException(status_code=400, detail="Folder name already used.")

    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    folder = Folders(
        name=folder_data.name,
        user_id=user_id
    )

    session.add(folder)
    session.commit()
    session.refresh(folder)
    return folder

# Create new flashcard
@app.post("/users/{user_id}/folders/{folder_id}/flashcards/")
def create_flashcard(
    user_id: int,
    folder_id: int,
    flashcard_data: FlashcardCreate,
    session: Session = Depends(get_session)
):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    folder = session.get(Folders, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found.")
    
    if folder.user_id != user.id:
        raise HTTPException(status_code=403, detail="Permission denied.")

    flashcard = Flashcards(
        question=flashcard_data.question,
        answer=flashcard_data.answer,
        folder_id=folder_id
    )

    session.add(flashcard)
    session.commit()
    session.refresh(flashcard)
    return flashcard

# Delete a user
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(Users, user_id) # Loads user by primary key
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    session.delete(user)
    session.commit()
    return {"message": f"User '{user.email}' deleted."}

# Delete a folder
@app.delete("/users/{user_id}/folders/{folder_id}/")
def delete_folder(
    user_id: int,
    folder_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    folder = session.get(Folders, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found.")

    if folder.user_id != user.id:
        raise HTTPException(status_code=403, detail="Permission denied.")
    
    session.delete(folder)
    session.commit()
    return {"message": f"Folder '{folder.name}' deleted."}

# Delete a flashcard
@app.delete("/users/{user_id}/folders/{folder_id}/flashcards/{flashcard_id}")
def delete_flashcard(
    user_id: int,
    folder_id: int,
    flashcard_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    folder = session.get(Folders, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found.")

    if folder.user_id != user.id:
        raise HTTPException(status_code=403, detail="Permission denied.")
    
    flashcard = session.get(Flashcards, flashcard_id)
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found.")

    if flashcard.folder_id != folder.id:
        raise HTTPException(status_code=403, detail="Permission denied.")

    session.delete(flashcard)
    session.commit()
    return {"message": f"Flashcard {flashcard.id} deleted."}