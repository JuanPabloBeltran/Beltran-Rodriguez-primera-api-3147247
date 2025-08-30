from sqlalchemy import Column, Integer, String
from database import Base

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=True)
    phone = Column(String(15), nullable=True)
