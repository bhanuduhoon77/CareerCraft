from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from pydantic import BaseModel, EmailStr

from backend.database import get_db
from backend.models.user import User

from backend.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================================
# REGISTER
# ==========================================

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "status": "success",
        "message": "User registered successfully",
        "user_id": user.id
    }


# ==========================================
# LOGIN - JSON
# ==========================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(user.id)

    return {
        "status": "success",
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id
    }


# ==========================================
# LOGIN - OAUTH2 / SWAGGER
# ==========================================

@router.post("/token")
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ==========================================
# CURRENT USER
# ==========================================

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):

    return {
        "status": "success",
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email
        }
    }