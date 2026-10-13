from sqlalchemy import Column, Integer, String, Boolean
from db import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(String)
    number = Column(String)
    email = Column(String)
    password_hash = Column(String)
    admin = Column(Boolean, default=False, nullable=False)
