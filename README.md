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

# 3. Move into backend/ and run the server
cd backend
uvicorn server:app --reload
```

Then open your browser at:  
- **Swagger docs:** http://127.0.0.1:8000/docs  
- **ReDoc docs:** http://127.0.0.1:8000/redoc  

---

## 🗂️ Project Structure

```
easyFlashcards/
├── server.py        # FastAPI app and endpoints
├── database.py      # Database models and engine setup
├── requirements.txt # Dependencies
├── README.md        # Project instructions
└── flashcards.db    # SQLite database (auto-created)
```

---

## 🧩 Example Endpoints

### ➕ Create a User
**POST** `/users/`
```json
{
  "email": "test@example.com",
  "password": "secret"
}
```

### ➕ Create a Folder
**POST** `/users/{user_id}/folders`
```json
{
  "name": "My First Folder"
}
```

### ➕ Create a Flashcard
**POST** `/users/{user_id}/folders/{folder_id}/flashcards`
```json
{
  "question": "What is FastAPI?",
  "answer": "A modern web framework for building APIs with Python."
}
```

---

## ❌ Delete Endpoints

### Delete a User (and all their folders + flashcards)
**DELETE** `/users/{user_id}`

### Delete a Folder (and its flashcards)
**DELETE** `/users/{user_id}/folders/{folder_id}`

### Delete a Flashcard
**DELETE** `/users/{user_id}/folders/{folder_id}/flashcards/{flashcard_id}`

---

## 🧰 Tech Stack

- **FastAPI** – Web framework  
- **SQLModel** – ORM built on SQLAlchemy and Pydantic  
- **SQLite** – Lightweight local database  
- **Uvicorn** – ASGI server for development  

---

## 👨‍💻 Author

Developed by **Nicholas Riccardo Tropea**
