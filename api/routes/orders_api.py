from fastapi import APIRouter, HTTPException, Query, Header, Depends
from typing import List

from sqlalchemy import desc
from starlette import status

from db.models.pdv_models import OrderWithDetails as Model, OrderBase as ModelCreate, Order as Base, User
from db.config.db_config import Session, get_db
from utils.gen_token import get_current_user

#from utils.gen_token import get_current_user

api = APIRouter()


@api.post("/create", response_model=Model)
def create_user(obj: ModelCreate, db: Session = Depends(get_db)):
    obj = Base(**obj.dict(exclude_none=True))
    db.add(obj)
    db.commit()
    obj_ret = db.query(Base).filter_by(
        id_article=obj.id_article,
        id_client=obj.id_client,
        id_user=obj.id_user,
        quantity=obj.quantity,
    ).order_by(desc(Base.id)).first()
    return Model.from_orm(obj_ret)


@api.get("/get_all", response_model=List[Model])
def get_all_users(db: Session = Depends(get_db)):
    list_obj = db.query(Base).order_by(desc(Base.created_date)).all()
    return [Model.from_orm(obj) for obj in list_obj]


@api.get("/get_all_user", response_model=List[Model])
def get_user_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = db.query(Base).filter(Base.id_user == current_user.id).order_by(desc(Base.created_date)).all()
    return [Model.from_orm(order) for order in orders]


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
    obj = db.query(Base).filter_by(id=id).first()
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


@api.get("/report_by_date/{start_date}/{end_date}", response_model=List[Model])
def get_report_by_date(start_date: str, end_date: str, db: Session = Depends(get_db)):
    list_obj = db.query(Base).filter(
        Base.created_date.between(start_date, end_date)
    ).all()
    if not list_obj:
        raise HTTPException(status_code=404, detail="Register not found")
    return [Model.from_orm(obj) for obj in list_obj]