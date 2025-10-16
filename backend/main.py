from fastapi import FastAPI
from database import create_db, SQLModel, engine
from routers import users, folders, flashcards

# Create the app
app = FastAPI(title="EasyFlashcards API")

# Initialize database
create_db()

# Include routers
app.include_router(users.router)
app.include_router(folders.router)
app.include_router(flashcards.router)


# -- GLOBAL ENDPOINTS ---

# Health check
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

# Root endpoint
@app.get("/", tags=["System"])
def root():
    return {"message": "Welcome to EasyFlashcards!"}

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
