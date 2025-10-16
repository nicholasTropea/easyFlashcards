from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import engine, Users
from models.user import UserCreate, UserRead
from security import hash_password, validate_password, verify_password, Psw_Validation_Results

router = APIRouter(prefix="/users", tags=["Users"])

# Creates a temporary connection to the database and closes it after each request
def get_session():
    with Session(engine) as session:
        yield session


# --- POST ENDPOINTS ---

# Create new user
@router.post("", response_model=UserRead)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    # Checks for users with same email
    existing_user = session.exec(
        select(Users).where(Users.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    # Checks for password validity
    errno = validate_password(user_data.password)
    if errno == Psw_Validation_Results.CHARS:
        raise HTTPException(status_code=400, detail="Password must be at least 10 characters long.")
    elif errno == Psw_Validation_Results.UPPERCASE:
        raise HTTPException(status_code=400, detail="Password must contain an uppercase character.")
    elif errno == Psw_Validation_Results.LOWERCASE:
        raise HTTPException(status_code=400, detail="Password must contain a lowercase character.")
    elif errno == Psw_Validation_Results.DIGIT:
        raise HTTPException(status_code=400, detail="Password must contain a digit.")        
    elif errno == Psw_Validation_Results.SPECIAL:
        raise HTTPException(status_code=400, detail="Password must contain one of these characters: % / @ # ! ? ( ) & _ - * +")        
        
    hashed_pw = hash_password(user_data.password)

    user = Users(
        email=user_data.email,
        hashed_password=hashed_pw
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Login user
@router.post("/login")
def login(
    credentials: UserCreate,
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(Users).where(Users.email == credentials.email)
    ).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    
    return {"message": "Login successful!"}


# --- DELETE ENDPOINTS ---

# Delete a user
@router.delete("/{user_id}")
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
