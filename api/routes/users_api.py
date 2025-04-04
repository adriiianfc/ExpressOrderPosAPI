from fastapi import APIRouter, HTTPException, Query, Header, Depends
from typing import List

from sqlalchemy import desc
from starlette import status

from db.models.pdv_models import UserModel as Model, UserBase as ModelCreate, User as Base, Token
from db.config.db_config import Session, get_db
from utils.gen_token import get_password_hash, validate

api = APIRouter()


@api.post("/create", response_model=Model)
def create_user(obj: ModelCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(obj.password)
    obj.password = hashed_password
    obj = Base(**Model.dict(exclude_none=True))
    db.add(obj)
    db.commit()
    obj_ret = db.query(Base).filter_by(
        mail=Model.mail,
    ).order_by(desc(Base.id)).first()
    return Model.from_orm(obj_ret)


@api.get("/get_all", response_model=List[Model])
def get_all_users(db: Session = Depends(get_db)):
    list_obj = db.query(Base).all()
    return [Model.from_orm(obj) for obj in list_obj]


@api.get("/get_by_id/{id}", response_model=Model)
def get_user_by_id(id: int,db: Session = Depends(get_db)):
    obj = db.query(Base).filter_by(id=id).first()
    if obj:
        return Model.from_orm(obj)
    else:
        raise HTTPException(status_code=404, detail="Register not found")


@api.get("/get_by_filter", response_model=List[Model])
def get_users_by_filter(filter: str = Query(..., description="Filter string for searching users"),
                        db: Session = Depends(get_db)):
    filter_query = f"%{filter}%"
    list_obj = db.query(Base).filter(
        Base.mail.like(filter_query)
    ).all()
    return [Model.from_orm(obj) for obj in list_obj]


@api.put("/update/{id}", response_model=Model)
def update_user(id: int, user: Model, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    obj = db.query(Base).filter_by(id=id).first()
    print(obj.id_empresa)
    for key, value in Model.dict(exclude_unset=True, exclude_none=True).items():
        setattr(obj, key, value)
    db.commit()
    return Model.from_orm(obj)


@api.delete("/delete/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    obj = db.query(Base).filter_by(id=id).first()
    db.delete(obj)
    db.commit()
    return {"detail": "Register deleted successfully"}


@api.get("/validate-token", response_model=Token)
def validate_token(authorization: str = Header(None), db: Session = Depends(get_db)):
    print(authorization)
    scheme, token = authorization.split()
    return validate(token)


