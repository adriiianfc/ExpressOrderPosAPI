from datetime import timedelta, datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Header, Depends
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import desc
from starlette import status

from db.models.pdv_models import UserModel as Model, UserBase as ModelCreate, User as Base, Token, User
from db.config.db_config import Session, get_db
from utils.gen_token import verify_password, create_access_token, get_password_hash, create_token

api = APIRouter()


@api.post("/login", response_model=Token)
def login(user: ModelCreate, db: Session = Depends(get_db)):
    db_user = db.query(Base).filter(Base.mail == user.mail).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_token(db_user.id)


@api.post("/create", response_model=Model)
def create_user(obj: ModelCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(obj.password)
    obj.password = hashed_password
    obj = Base(id=0, mail=obj.mail, password=obj.password)
    db.add(obj)
    db.commit()
    obj_ret = db.query(Base).filter_by(
        mail=obj.mail,
    ).order_by(desc(Base.id)).first()
    return Model.from_orm(obj_ret)