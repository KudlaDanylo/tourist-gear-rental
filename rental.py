from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from db import Base

class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    rent_time = Column(DateTime, default=datetime.now)