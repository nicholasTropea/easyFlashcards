# 🧠 EasyFlashcards API

A backend API built with **FastAPI** and **SQLModel** to manage users, folders, and flashcards.

Each user can have multiple folders, and each folder can contain multiple flashcards.  
Deleting a user automatically deletes their folders and flashcards (cascade delete).

---

## ⚙️ Run Locally

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate    # On Linux/Mac
venv\Scripts\activate       # On Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
uvicorn main:app --reload

# 4. Open your browser at
Swagger docs → http://127.0.0.1:8000/docs
```
## 🗂️ Project Structure
easyFlashcards/
├── main.py          # FastAPI app and endpoints
├── database.py      # Database models and engine setup
├── requirements.txt # Dependencies
├── README.md        # Project instructions
└── flashcards.db    # SQLite database (auto-created)

## 🧩 Example Endpoints
➕ Create a user

POST ```/users/```
```
{
  "email": "test@example.com",
  "password": "secret"
}
```

➕ Create a folder

POST ```/users/{user_id}/folders```
```
{
  "name": "My First Folder"
}
```

➕ Create a flashcard

POST ```/users/{user_id}/folders/{folder_id}/flashcards```
```
{
  "question": "What is FastAPI?",
  "answer": "A modern web framework for building APIs with Python."
}
```

## ❌ Delete Endpoints
Delete a user (and all their folders + flashcards)

DELETE ```/users/{user_id}```

Delete a folder (and its flashcards)

DELETE ```/users/{user_id}/folders/{folder_id}```

Delete a flashcard

DELETE ```/users/{user_id}/folders/{folder_id}/flashcards/{flashcard_id}```

## 🧰 Tech Stack

FastAPI – Web framework

SQLModel – ORM built on SQLAlchemy and Pydantic

SQLite – Lightweight local database

Uvicorn – ASGI server for development

## 👨‍💻 Author

Developed by Nicholas Riccardo Tropea