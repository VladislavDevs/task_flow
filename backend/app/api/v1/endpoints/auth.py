from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.core.security import create_access_token, create_refresh_token, get_password_hash, verify_password
from backend.app.services.auth_service import get_user_by_email, authenticate_user, get_user_by_id
from backend.app.schemas.auth import UserCreate, UserLogin, Token, TokenRefresh, PasswordChange, UserOut
from backend.app.api.v1.dependencies import get_current_user
from backend.app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email.__str__()):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email.__str__(), user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    iat = datetime.now(timezone.utc)
    access_token = create_access_token(data={"sub": str(db_user.id), "iat": iat})
    refresh_token = create_refresh_token(data={"sub": str(db_user.id), "iat": iat})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
def refresh(token_data: TokenRefresh, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
    )
    try:
        payload = jwt.decode(token_data.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_type = payload.get("type")
        if token_type != "refresh":
            raise credentials_exception
        token_iat = payload.get("iat")
        if token_iat is None:
            raise credentials_exception
        token_iat_datetime = datetime.fromtimestamp(token_iat, tz=timezone.utc)
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(db, int(user_id))
    if not user or user.password_updated_at > token_iat_datetime:
        raise credentials_exception

    new_iat = datetime.now(timezone.utc)
    new_access = create_access_token(data={"sub": str(user.id), "iat": new_iat})
    new_refresh = create_refresh_token(data={"sub": str(user.id), "iat": new_iat})
    return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}

@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    if password_data.old_password == password_data.new_password:
        raise HTTPException(status_code=400, detail="New password must be different from old password")
    current_user.hashed_password = get_password_hash(password_data.new_password)
    current_user.password_updated_at = datetime.now(timezone.utc)
    db.commit()
    return {"detail": "Password updated successfully"}