# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.user import UserCreate, UserRead, Token
from app.services.auth import UserAlreadyExistsError, InvalidCredentialsError, AuthStore, get_auth_store
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])

# creates a new user
@router.post("/register", response_model=UserRead, status_code=201)
def register_user(user_in: UserCreate, store: AuthStore = Depends(get_auth_store)):
    try:
        return store.register_user(user_in)
    except UserAlreadyExistsError:
        raise HTTPException(status_code=409, detail="User already exists")

# checks login credentials
@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), store: AuthStore = Depends(get_auth_store)):
    try:
        token = store.authenticate_user(email=form_data.username, password=form_data.password)
        return Token(access_token=token)
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Invalid credentials")