from sqlalchemy import Column, Integer, String, Boolean

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    uuid = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, unique=True)
    is_admin = Column(Boolean, default=False)
    hashed_password = Column(String)
