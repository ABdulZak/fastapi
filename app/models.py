from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable = False)
    contact = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    owner = relationship('User')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable = False, unique=True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.id', ondelete='CASCADE'), primary_key=True)