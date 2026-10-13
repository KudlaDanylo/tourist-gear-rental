from sqlalchemy import Column, Integer, String
from db import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    price = Column(Integer)
    quantity = Column(Integer, nullable=False, default=1)