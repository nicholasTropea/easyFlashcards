from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy import exc
from database import engine, Users, Folders
from models.folder import FolderCreate, FolderRead

router = APIRouter(prefix="/users", tags=["Folders"])

# Creates a temporary connection to the database and closes it after each request
def get_session():
    with Session(engine) as session:
        yield session


# --- POST ENDPOINTS ---

# Create new folder
@router.post("/{user_id}/folders", response_model=FolderRead)
def create_folder(
    user_id: int,
    folder_data: FolderCreate,
    session: Session = Depends(get_session)
):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Checks for folders with same name under the same user
    existing_folder = session.exec(
        select(Folders).where(
            (Folders.user_id == user_id) & (Folders.name == folder_data.name)
        )
    ).first()
    if existing_folder:
        raise HTTPException(status_code=400, detail="Folder name already used.")

    folder = Folders(
        name=folder_data.name,
        user_id=user_id
    )

    try:
        session.add(folder)
        session.commit()
    except exc.IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Folder name already used.")

    session.refresh(folder)
    return folder


# --- DELETE ENDPOINTS ---

# Delete a folder
@router.delete("/{user_id}/folders/{folder_id}")
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


# --- GET ENDPOINTS ---

# Retrieve all user's folders
@router.get("/{user_id}/folders", response_model=list[FolderRead])
def get_all_folders(
    user_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    folders = session.exec(
        select(Folders).where(Folders.user_id == user_id)
    ).all()
    return folders