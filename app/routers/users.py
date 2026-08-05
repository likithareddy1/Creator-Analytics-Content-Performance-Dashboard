<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
=======
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import UserRole
from app.schemas.user import UserCreate, UserListResponse, UserResponse, UserUpdate
from app.services.user_service import UserService
>>>>>>> 567a2ff61666ec1d3b961045a6a013fac9a11976

router = APIRouter(prefix="/users", tags=["Users"])


<<<<<<< HEAD
# ✅ CREATE USER
@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=user.password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ✅ GET ALL USERS
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# ✅ 🔍 SEARCH USERS BY ROLE (NEW)
@router.get("/search")
def search_users(role: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.role == role).all()

    return {
        "total_count": len(users),
        "users": users
    }


# ✅ GET USER BY ID
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ✅ UPDATE USER
@router.put("/{user_id}")
def update_user(
    user_id: int,
    updated_user: UserUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 🔍 Email duplicate check
    if updated_user.email is not None:
        existing_user = db.query(User).filter(User.email == updated_user.email).first()
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=400, detail="Email already exists")

    # 🔄 Update fields
    if updated_user.full_name is not None:
        user.full_name = updated_user.full_name

    if updated_user.email is not None:
        user.email = updated_user.email

    if updated_user.password is not None:
        user.password = updated_user.password

    if updated_user.role is not None:
        user.role = updated_user.role

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully",
        "data": user
    }


# ✅ DELETE USER
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
=======
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    return UserService.create(db, user_in)


@router.get("/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return UserService.get_all(db, skip=skip, limit=limit)


# 1. SEARCH ENDPOINT
@router.get("/search", response_model=UserListResponse)
def search_users(
    role: Optional[UserRole] = Query(None, description="Filter users by role"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    return UserService.search_by_role(db, role=role, skip=skip, limit=limit)


# 2. GET SINGLE USER ENDPOINT
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.get_by_id(db, user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    return UserService.update(db, user_id, user_in)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.delete(db, user_id)
>>>>>>> 567a2ff61666ec1d3b961045a6a013fac9a11976
