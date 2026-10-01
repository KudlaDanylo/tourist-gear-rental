from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table import Base, Client

class Bd:
    def __init__(self, db_name: str = "sqlite:///tourist_rental.db"):
        self.engine = create_engine(db_name, echo=False)
        Base.metadata.create_all(self.engine)
        self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self._SessionLocal()