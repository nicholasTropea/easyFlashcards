# Used for password hashing (with envvar pepper)
from passlib.context import CryptContext
from dotenv import load_dotenv
import os, hashlib # hashlib used in _prehash()


# Password validation constants
from enum import Enum

class Psw_Validation_Results(int, Enum):
    VALID = 1
    CHARS = -1
    UPPERCASE = -2
    LOWERCASE = -3
    DIGIT = -4
    SPECIAL = -5


# Load environmnet variables
load_dotenv()
PEPPER = os.getenv("PASSWORD_PEPPER", "") # Fallback to empty if not set
if not PEPPER:
    raise RuntimeError("Missing PASSWORD_PEPPER in .env file")

# Creates password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -- CORE HASHING FUNCTIONS ---

# Returns 32-byte digest (safe for bcrypt since it handles max 72 bytes)
def _prehash(password: str) -> bytes:
    return hashlib.sha256((password + PEPPER).encode()).digest()

def hash_password(password: str) -> str:
    return pwd_context.hash(_prehash(password))

def verify_password(plain_password: str, hashed_password) -> bool:
    return pwd_context.verify(_prehash(plain_password), hashed_password)


# --- PASSWORD STRENGTH VALIDATOR ---

def validate_password(plain_password: str) -> int:
    SPECIAL_CHARS = "%/@#!?()&_-*+"
    
    count = 0
    upper = lower = digit = special = False

    for char in plain_password:
        count += 1
        if not upper and char.isupper(): upper = True
        if not lower and char.islower(): lower = True
        if not digit and char.isdigit(): digit = True
        if not special and char in SPECIAL_CHARS: special = True
    
    if count < 10: return Psw_Validation_Results.CHARS
    if not upper: return Psw_Validation_Results.UPPERCASE
    if not lower: return Psw_Validation_Results.LOWERCASE
    if not digit: return Psw_Validation_Results.DIGIT
    if not special: return Psw_Validation_Results.SPECIAL

    return Psw_Validation_Results.VALID