from fastapi import APIRouter, HTTPException, Query, Header, Depends
from typing import List

from sqlalchemy import desc
from starlette import status

from db.models.pdv_models import ClientBase as Model, ClientCreate as ModelCreate, Client as Base
from db.config.db_config import Session, get_db
api = APIRouter()


@api.post("/create", response_model=Model)
def create_user(obj: ModelCreate, db: Session = Depends(get_db)):
    obj = Base(**obj.dict(exclude_none=True))
    db.add(obj)
    db.commit()
    obj_ret = db.query(Base).filter_by(
        name=obj.name,
    ).order_by(desc(Base.id)).first()
    return Model.from_orm(obj_ret)


@api.get("/get_all", response_model=List[Model])
def get_all_users(db: Session = Depends(get_db)):
    list_obj = db.query(Base).all()
    return [Model.from_orm(obj) for obj in list_obj]