from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app.core.security import verify_password

def get_user_by_email(db: Session, email: str) -> User | None:
    """

    :rtype: User | None
    """
    return db.query(User).filter(email == User.email).first()

def authenticate_user(db: Session, email: str, password: str) -> User | bool:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(user_id == User.id).first()