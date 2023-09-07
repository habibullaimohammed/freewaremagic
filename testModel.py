from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    android = relationship("Android", back_populates="owner")


class Android(Base):
    __tablename__ = "android"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    quill_description = Column(String)
    description = Column(String)
    image_url = Column(String)
    download_url = Column(String)
    download_url2 = Column(String)
    download_count = Column(Integer, default=0)
    category = Column(String)
    sub_category = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="android")




