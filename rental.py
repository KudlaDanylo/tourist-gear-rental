from sqlalchemy import Column, Integer, ForeignKey, Date
from db import Base

class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    start_time = Column(Date, nullable=False)
    end_time = Column(Date, nullable=False)