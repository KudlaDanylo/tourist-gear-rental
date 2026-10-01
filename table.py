from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(String)
    number = Column(String)
    email = Column(String)
    password_hash = Column(String)
    admin = Column(Boolean, default=False, nullable=False)


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    price_par_day = Column(String)
    is_available = Column(Boolean, default=True, nullable=False)