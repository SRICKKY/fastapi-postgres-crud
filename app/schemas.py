from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str
