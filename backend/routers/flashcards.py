from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import engine, Users, Folders, Flashcards
from models.flashcard import FlashcardCreate, FlashcardRead

router = APIRouter(prefix="/users", tags=["Flashcards"])

# Creates a temporary connection to the database and closes it after each request
def get_session():
    with Session(engine) as session:
        yield session
    

# --- POST ENDPOINTS ---

# Create new flashcard
@router.post("/{user_id}/folders/{folder_id}/flashcards", response_model=FlashcardRead)
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


# --- DELETE ENDPOINTS ---

# Delete a flashcard
@router.delete("/{user_id}/folders/{folder_id}/flashcards/{flashcard_id}")
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


# --- GET ENDPOINTS ---

# Retrieve all user's folder's flashcards
@router.get("/{user_id}/folders/{folder_id}/flashcards", response_model=list[FlashcardRead])
def get_all_flashcards(
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
    
    flashcards = session.exec(
        select(Flashcards).where(Flashcards.folder_id == folder_id)
    ).all()
    return flashcards
