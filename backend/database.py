from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# ==================== MySQL Configuration ====================
MYSQL_USER = "root"
MYSQL_PASSWORD = "12345"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DATABASE = "mental_chatbot"

# Database URL
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Create database engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Test connections before using them
    pool_recycle=3600,   # Recycle connections after 1 hour
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# ==================== DATABASE MODELS ====================

class Conversation(Base):
    """Model for storing conversation messages"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, timestamp={self.timestamp})>"


class ImageSelection(Base):
    """Model for storing selected image choices"""
    __tablename__ = "image_selections"
    
    id = Column(Integer, primary_key=True, index=True)
    choice_index = Column(Integer, nullable=False)
    mood_type = Column(String(50), nullable=False)  # calm, stressed, neutral
    emoji = Column(String(10), nullable=True)
    image_url = Column(String(500), nullable=False)
    user_message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    
    def __repr__(self):
        return f"<ImageSelection(id={self.id}, mood_type={self.mood_type}, timestamp={self.timestamp})>"


# Create all tables
def init_db():
    """Initialize database and create all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
