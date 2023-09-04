from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


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
    description = Column(String)
    image_url = Column(String)
    download_url = Column(String)
    download_url2 = Column(String)
    category = Column(String)
    sub_category = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="android")




