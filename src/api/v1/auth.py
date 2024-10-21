from typing import Annotated, Dict, Optional, List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy import select
from starlette import status
from starlette.exceptions import HTTPException
from sqlalchemy.orm import joinedload

from src.auth.auth import authenticate_user, create_access_token, reg_user, user_dependency, JWT_SECRET, ALGORITHM, \
    bcrypt_context, oauth2_bearer
from src.db.db import db_dependency
from src.models import User
from src.schemas.user import UserRegisterSchema, UserLoginSchema

auth_router = APIRouter(prefix="/auth", tags=['auth'])


@auth_router.post("/login")
async def login_for_access_token(db: db_dependency,
                                login_data: UserLoginSchema):
   user = await authenticate_user(login_data, db)
   if not user:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Incorrect username or password",
           headers={"WWW-Authenticate": "Bearer"},
       )
   access_token = create_access_token(
       data={"sub": user.email, "role": user.role.name.value}
   )
   return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/token")
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
               db: db_dependency):
   user = await authenticate_user(
       UserLoginSchema(email=form_data.username, password=form_data.password),
       db=db)

   if not user:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                           detail="Could not validate user.")
   access_token = create_access_token(
       data={"sub": user.email, "role": user.role.name.value}
   )
   return {'access_token': access_token, 'token_type': 'bearer'}

async def get_current_user(token: str = Depends(oauth2_bearer)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_data = {"sub": payload.get("sub"), "role": payload.get("role")}
        if user_data is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_data


@auth_router.get("/current_user")
async def get_current_user(user: user_dependency):
    return {"user": user}

user_dependency = Annotated[Dict, Depends(get_current_user)]



# Аутентификация пользователя
async def authenticate_user(login_data: UserLoginSchema, db: db_dependency):
    # делаем SELECT-запрос в базу данных для нахождения пользователя по email
    result = await db.execute(select(User)
                              .options(joinedload(User.role))
                              .where(User.email == login_data.email))
    user: Optional[User] = result.scalars().first()

    # пользователь будет авторизован, если он зарегистрирован и ввёл корректный пароль
    if not user:
        return False
    if not bcrypt_context.verify(login_data.password + user.salt, user.hashed_password):
        return False
    return user

def has_role(required_role: List[str]):
    def role_checker(current_user: user_dependency):
        if current_user["role"] not in required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker