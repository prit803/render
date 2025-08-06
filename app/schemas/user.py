from pydantic import BaseModel, EmailStr
from datetime import date

class UserCreate(BaseModel):
    name: str
    mobile_no: str
    email: EmailStr
    password: str
    dob: date

class UserOut(BaseModel):
    id: int
    name: str
    mobile_no: str
    email: EmailStr
    dob: date

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
