from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, DateTime
from sqlalchemy.orm import relationship, sessionmaker, Mapped, mapped_column
from pydantic import BaseModel
from typing import Optional, List

from db.config.db_config import Base

# Modelos SQLAlchemy
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mail = Column(String(450), nullable=False)
    password = Column(String(255), nullable=False)

    # Relaciones
    orders = relationship("Order", back_populates="user")


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)

    # Relaciones
    orders = relationship("Order", back_populates="client")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    price = Column(Float, nullable=False)

    # Relaciones
    orders = relationship("Order", back_populates="article")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_article = Column(Integer, ForeignKey("articles.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    id_client = Column(Integer, ForeignKey("clients.id"), nullable=False)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime, nullable=False)

    # Relaciones
    article = relationship("Article", back_populates="orders")
    client = relationship("Client", back_populates="orders")
    user = relationship("User", back_populates="orders")


# Modelos base (para creación)
class UserBase(BaseModel):
    mail: str
    password: str

    class Config:
        from_attributes = True


class ClientBase(BaseModel):
    id: Optional[int]
    name: str
    class Config:
        from_attributes = True


class ClientCreate(BaseModel):
    name: str
    class Config:
        from_attributes = True


class ArticleBase(BaseModel):
    id: Optional[int]
    name: str
    price: float
    class Config:
        from_attributes = True

class ArticleCreate(BaseModel):
    name: str
    price: float
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    id_article: int
    quantity: int
    amount: float
    id_client: int
    id_user: int
    created_date: datetime
    class Config:
        from_attributes = True


# Modelos para respuestas (incluyen ID)
class UserModel(UserBase):
    id: int
    mail: str

    class Config:
        from_attributes = True


class ClientModel(ClientBase):
    id: int

    class Config:
        from_attributes = True


class ArticleModel(ArticleBase):
    id: int

    class Config:
        from_attributes = True


class OrderModel(OrderBase):
    id: int

    class Config:
        from_attributes = True


# Modelos para respuestas con relaciones
class OrderWithDetails(OrderModel):
    id_article: int
    quantity: int
    amount: float
    id_client: int
    id_user: int
    article: ArticleModel
    client: ClientModel
    user: UserModel

    class Config:
        from_attributes = True


class UserWithOrders(UserModel):
    orders: List[OrderModel] = []

    class Config:
        from_attributes = True


class ClientWithOrders(ClientModel):
    orders: List[OrderModel] = []

    class Config:
        from_attributes = True


class ArticleWithOrders(ArticleModel):
    orders: List[OrderModel] = []

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int

class UserInDB(User):
    hashed_password: Mapped[str] = mapped_column(String)
