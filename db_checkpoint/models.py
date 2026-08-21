from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime,default=lambda : datetime.now(timezone.utc))

    conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    title = Column(String,nullable=False)
    created_at = Column(DateTime,default=lambda : datetime.now(timezone.utc))
    tokens_used = Column(Integer, default=0)
    user = relationship("User",back_populates="conversations")
    messages = relationship("Message",back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer,primary_key=True,index=True)
    conversation_id = Column(Integer,ForeignKey("conversations.id"),nullable=False)
    role = Column(String,nullable=False)
    content = Column(Text, nullable=False)
    
    created_at = Column(DateTime,default=lambda : datetime.now(timezone.utc))

    conversation = relationship("Conversation",back_populates="messages")

