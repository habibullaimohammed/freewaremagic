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
    windows = relationship("Windows", back_populates="owner")
    mac = relationship("Mac", back_populates="owner")
    iphone = relationship("Iphone", back_populates="owner")
    consolegame = relationship("ConsoleGame", back_populates="owner")
    goggame = relationship("GOGGame", back_populates="owner")
    articles = relationship("Articles", back_populates="owner")


class Articles(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author_name = Column(String)
    author_image_url = Column(String)
    sub_title = Column(String)
    quill_description = Column(String)
    image_url = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="articles")


class Android(Base):
    __tablename__ = "android"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String)
    developer = Column(String)
    quill_description = Column(String)
    image_url = Column(String)
    background_image_url = Column(String)
    download_url_getintopc = Column(String)
    download_url_igetintopc = Column(String)
    download_url_softonic = Column(String)
    download_url_filehippo = Column(String)
    download_url_moddroid = Column(String)
    download_count = Column(Integer, default=0)
    category = Column(String)
    sub_category = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="android")


class Windows(Base):
    __tablename__ = "windows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String)
    developer = Column(String)
    quill_description = Column(String)
    image_url = Column(String)
    background_image_url = Column(String)
    download_url_getintopc = Column(String)
    download_url_igetintopc = Column(String)
    download_url_softonic = Column(String)
    download_url_filehippo = Column(String)
    download_url_moddroid = Column(String)
    download_count = Column(Integer, default=0)
    category = Column(String)
    sub_category = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="windows")


class Mac(Base):
    __tablename__ = "mac"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String)
    developer = Column(String)
    quill_description = Column(String)
    image_url = Column(String)
    background_image_url = Column(String)
    download_url_getintopc = Column(String)
    download_url_igetintopc = Column(String)
    download_url_softonic = Column(String)
    download_url_filehippo = Column(String)
    download_url_moddroid = Column(String)
    download_count = Column(Integer, default=0)
    category = Column(String)
    sub_category = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="mac")


class Iphone(Base):
    __tablename__ = "iphone"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String)
    developer = Column(String)
    quill_description = Column(String)
    image_url = Column(String)
    background_image_url = Column(String)
    download_url_getintopc = Column(String)
    download_url_igetintopc = Column(String)
    download_url_softonic = Column(String)
    download_url_filehippo = Column(String)
    download_url_moddroid = Column(String)
    download_count = Column(Integer, default=0)
    category = Column(String)
    sub_category = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="iphone")


class ConsoleGame(Base):
    __tablename__ = "consolegame"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String)
    developer = Column(String)
    quill_description = Column(String)
    image_url = Column(String)
    background_image_url = Column(String)
    download_url_getintopc = Column(String)
    download_url_igetintopc = Column(String)
    download_url_softonic = Column(String)
    download_url_filehippo = Column(String)
    download_url_moddroid = Column(String)
    download_count = Column(Integer, default=0)
    category = Column(String)
    sub_category = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="consolegame")


class GOGGame(Base):
    __tablename__ = "goggame"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String)
    developer = Column(String)
    quill_description = Column(String)
    image_url = Column(String)
    background_image_url = Column(String)
    download_url_getintopc = Column(String)
    download_url_igetintopc = Column(String)
    download_url_softonic = Column(String)
    download_url_filehippo = Column(String)
    download_url_moddroid = Column(String)
    download_count = Column(Integer, default=0)
    category = Column(String)
    sub_category = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="goggame")
