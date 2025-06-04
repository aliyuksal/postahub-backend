from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.api_server.schemas.auth import LoginRequest, LoginResponse
from apps.api_server.services.auth_service import login_user
from apps.api_server.core.database import get_db
from apps.api_server.schemas.user import UserOut, UpdateUserRequest
from apps.api_server.services.auth_service import get_current_user
from apps.api_server.models.user import User
from apps.api_server.schemas.user import UpdatePasswordRequest
from apps.api_server.core.security import verify_password, hash_password
from fastapi import HTTPException

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, data.email, data.password)


@router.get("/me", response_model=UserOut)
def get_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    full_name = f"{current_user.first_name or ''} {current_user.last_name or ''}".strip()

    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "role": current_user.role,
        "plan": current_user.subscription_plan.plan_name if current_user.subscription_plan else "free",
        "createdAt": current_user.created_at.isoformat() if current_user.created_at else None,
        "name": full_name
    }


@router.patch("/password")
def update_password(
    data: UpdatePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(data.current_password, current_user.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect.")

    current_user.password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password updated successfully."}


@router.patch("/me", response_model=UserOut)
def update_me(
    data: UpdateUserRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # full_name varsa: parçala ve yaz
    if data.full_name:
        name_parts = data.full_name.strip().split(" ")
        current_user.first_name = name_parts[0]
        current_user.last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

    # varsa override edilecek alanlar
    if data.first_name is not None:
        current_user.first_name = data.first_name

    if data.last_name is not None:
        current_user.last_name = data.last_name

    if data.email is not None:
        current_user.email = data.email

    db.commit()
    db.refresh(current_user)
    return current_user