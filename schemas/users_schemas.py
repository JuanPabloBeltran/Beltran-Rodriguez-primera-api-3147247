from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: Optional[int] = Field(None, ge=0, le=120)  
    phone: Optional[str] = Field(None, regex=r"^\+?\d{7,15}$")  

    @validator("username")
    def username_must_be_capitalized(cls, value):
        return value.title()

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True  # Permite convertir desde SQLAlchemy
