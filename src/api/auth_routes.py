from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import timedelta, date
from src.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from src.database.connection import db

router = APIRouter(prefix="/auth", tags=["auth"])


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "listener"


class UserResponse(BaseModel):
    id_user: int
    email: str
    role: str


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email']},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    existing = db.execute_query(
        "SELECT ID_User FROM Users WHERE Email = %s",
        (user_data.email,),
        fetch_one=True
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(user_data.password)

    listener_id = None
    author_id = None

    if user_data.role == "listener":
        result = db.execute_query(
            """
            INSERT INTO Listeners (Name, Email, Reg_Date, Sub_Status)
            VALUES (%s, %s, %s, 'Бесплатно')
            RETURNING ID_Listener
            """,
            (user_data.email.split('@')[0], user_data.email, date.today()),
            fetch_one=True
        )
        listener_id = result['id_listener']

    elif user_data.role == "author":
        result = db.execute_query(
            """
            INSERT INTO Authors (Nickname, Email, Description, Rating)
            VALUES (%s, %s, %s, 0)
            RETURNING ID_Author
            """,
            (user_data.email.split('@')[0], user_data.email, ''),
            fetch_one=True
        )
        author_id = result['id_author']

    result = db.execute_query(
        """
        INSERT INTO Users (Email, Password_Hash, Role, ID_Listener, ID_Author)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING ID_User
        """,
        (user_data.email, hashed_password, user_data.role, listener_id, author_id),
        fetch_one=True
    )

    return {
        "id_user": result['id_user'],
        "email": user_data.email,
        "role": user_data.role
    }


@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    return {
        "id_user": current_user['id_user'],
        "email": current_user['email'],
        "role": current_user['role']
    }