from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import UserCreate, UserResponse, UserLogin, UserUpdate, PaginatedUserResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.user import (
    get_user_by_email,
    get_user_by_id,
    get_user_by_username,
    create_user,
    update_user,
    delete_user,
    get_all_users
)
from app.utils.security import (
    verify_password,
    create_access_token
)


user_router = r = APIRouter(tags=["Users"])

@user_router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    return create_user(db, user)


@user_router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.put("/users/{user_id}", response_model=UserResponse)
def update_user_endpoint(
    user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)
):
    db_user = update_user(db, user_id, user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    result = delete_user(db, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@user_router.get("/users", response_model=PaginatedUserResponse)
def get_all_users_endpoint(db: Session = Depends(get_db), page: int = 1, per_page: int = 10):
    if page < 1 or per_page < 1:
        raise HTTPException(status_code=400, detail="Page and per_page must be positive integers")
    
    users, total = get_all_users(db, page, per_page)
    total_pages = (total + per_page - 1) // per_page
    
    return PaginatedUserResponse(
        users=users,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )
