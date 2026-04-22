"""
Data retrieval functions for accessing database records
Provides functions to query conversations and image selections
"""

from database import SessionLocal, Conversation, ImageSelection
from datetime import datetime, timedelta


def get_all_conversations(limit=None):
    """Get all conversations from database"""
    db = SessionLocal()
    try:
        query = db.query(Conversation).order_by(Conversation.timestamp.desc())
        if limit:
            query = query.limit(limit)
        conversations = query.all()
        return [
            {
                "id": c.id,
                "user": c.user_message,
                "bot": c.bot_response,
                "timestamp": c.timestamp.isoformat()
            }
            for c in conversations
        ]
    finally:
        db.close()


def get_conversations_by_date_range(start_date, end_date):
    """Get conversations within a specific date range"""
    db = SessionLocal()
    try:
        conversations = db.query(Conversation).filter(
            Conversation.timestamp >= start_date,
            Conversation.timestamp <= end_date
        ).order_by(Conversation.timestamp.desc()).all()
        
        return [
            {
                "id": c.id,
                "user": c.user_message,
                "bot": c.bot_response,
                "timestamp": c.timestamp.isoformat()
            }
            for c in conversations
        ]
    finally:
        db.close()


def get_all_image_selections(limit=None):
    """Get all image selections from database"""
    db = SessionLocal()
    try:
        query = db.query(ImageSelection).order_by(ImageSelection.timestamp.desc())
        if limit:
            query = query.limit(limit)
        images = query.all()
        return [
            {
                "id": img.id,
                "choice_index": img.choice_index,
                "mood_type": img.mood_type,
                "emoji": img.emoji,
                "image_url": img.image_url,
                "user_message": img.user_message,
                "timestamp": img.timestamp.isoformat()
            }
            for img in images
        ]
    finally:
        db.close()


def get_image_selections_by_mood(mood_type):
    """Get all image selections filtered by mood type"""
    db = SessionLocal()
    try:
        images = db.query(ImageSelection).filter(
            ImageSelection.mood_type == mood_type
        ).order_by(ImageSelection.timestamp.desc()).all()
        
        return [
            {
                "id": img.id,
                "choice_index": img.choice_index,
                "mood_type": img.mood_type,
                "emoji": img.emoji,
                "image_url": img.image_url,
                "user_message": img.user_message,
                "timestamp": img.timestamp.isoformat()
            }
            for img in images
        ]
    finally:
        db.close()


def get_mood_statistics():
    """Get statistics about mood selections"""
    db = SessionLocal()
    try:
        mood_types = ["calm", "stressed", "neutral"]
        stats = {}
        
        for mood in mood_types:
            count = db.query(ImageSelection).filter(
                ImageSelection.mood_type == mood
            ).count()
            stats[mood] = count
        
        total = sum(stats.values())
        stats["total"] = total
        
        return stats
    finally:
        db.close()


def get_conversation_statistics():
    """Get statistics about conversations"""
    db = SessionLocal()
    try:
        total_conversations = db.query(Conversation).count()
        total_image_selections = db.query(ImageSelection).count()
        
        return {
            "total_conversations": total_conversations,
            "total_image_selections": total_image_selections,
            "total_messages": total_conversations * 2  # Each conversation has user + bot
        }
    finally:
        db.close()
