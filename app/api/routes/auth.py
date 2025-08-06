from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt
from app.schemas.user import *
from app.schemas.token import Token
from app.db.session import SessionLocal
from app.models.user import User as UserModel
from app.core.config import settings
from app.utils.response import success_response, error_response  
from jose import jwt, JWTError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
        if existing_user:
            return JSONResponse(
                content={
                    "success": False,
                    "successMessage": None,
                    "data": None,
                    "errorMessage": "User with this email already exists.",
                    "statusCode": "400",
                },
                status_code=400,
            )

        hashed_password = pwd_context.hash(user.password)
        db_user = UserModel(
            name=user.name,
            mobile_no=user.mobile_no,
            email=user.email,
            hashed_password=hashed_password,
            dob=user.dob
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return JSONResponse(
            content={
                "success": True,
                "successMessage": "User registered successfully.",
                "data": {
                    "id": db_user.id,
                    "email": db_user.email
                },
                "errorMessage": None,
                "statusCode": "200",
            },
            status_code=200,
        )
    except Exception as e:
        print(f"Register Error: {e}")
        return JSONResponse(
            content={
                "success": False,
                "successMessage": None,
                "data": None,
                "errorMessage": "Network Is Busy, Try After Sometime",
                "statusCode": "404",
            },
            status_code=404,
        )


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        db_user = db.query(UserModel).filter(UserModel.email == data.email).first()

        if not db_user or not pwd_context.verify(data.password, db_user.hashed_password):
            return JSONResponse(
                content={
                    "success": False,
                    "successMessage": None,
                    "data": None,
                    "errorMessage": "Incorrect email or password.",
                    "statusCode": "400",
                },
                status_code=400,
            )

        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": str(db_user.id), "exp": expire}
        access_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return JSONResponse(
            content={
                "success": True,
                "successMessage": "Login successful.",
                "data": {
                    "access_token": access_token,
                    "token_type": "bearer"
                },
                "errorMessage": None,
                "statusCode": "200",
            },
            status_code=200,
        )

    except Exception as e:
        print(f"Login Error: {e}")
        return JSONResponse(
            content={
                "success": False,
                "successMessage": None,
                "data": None,
                "errorMessage": "Network Is Busy, Try After Sometime",
                "statusCode": "404",
            },
            status_code=404,
        )



@router.get("/userInfo")
def get_user_info(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise Exception("Invalid token")

        user = db.query(UserModel).filter(UserModel.id == int(user_id)).first()
        if not user:
            return JSONResponse(
                content={
                    "success": False,
                    "successMessage": None,
                    "data": None,
                    "errorMessage": "User not found.",
                    "statusCode": "400",
                },
                status_code=400,
            )

        return JSONResponse(
            content={
                "success": True,
                "successMessage": "User info fetched successfully.",
                "data": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "mobile_no": user.mobile_no,
                    "dob": str(user.dob)
                },
                "errorMessage": None,
                "statusCode": "200",
            },
            status_code=200,
        )

    except JWTError as e:
        print(f"Token decode error: {e}")
        return JSONResponse(
            content={
                "success": False,
                "successMessage": None,
                "data": None,
                "errorMessage": "Invalid or expired token.",
                "statusCode": "400",
            },
            status_code=400,
        )
    except Exception as e:
        print(f"User info error: {e}")
        return JSONResponse(
            content={
                "success": False,
                "successMessage": None,
                "data": None,
                "errorMessage": "Network Is Busy, Try After Sometime",
                "statusCode": "404",
            },
            status_code=404,
        )