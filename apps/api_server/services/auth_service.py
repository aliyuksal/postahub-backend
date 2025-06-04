from sqlalchemy.orm import Session
from apps.api_server.models.user import User
from apps.api_server.core.security import verify_password, create_access_token
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from apps.api_server.core.database import get_db
import os


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret")
ALGORITHM = "HS256"

def authenticate_user(db, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})

    full_name = f"{user.first_name} {user.last_name}".strip() if user.first_name and user.last_name else user.company_name or "Unnamed"

    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": full_name,
            "role": user.role or "user",
            "plan": user.subscription_plan.plan_name if user.subscription_plan else "free",
            "createdAt": user.created_at.isoformat() if user.created_at else None
        }
    }

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    print("🔐 Token received:", token)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token (sub)")
    except JWTError as e:
        print("❌ Token decode error:", str(e))
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user