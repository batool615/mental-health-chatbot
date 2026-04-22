from datetime import datetime
from database import SessionLocal, Conversation, ImageSelection

# Get database session
db = SessionLocal()

def add_to_memory(user, bot):
    """Add message to database"""
    try:
        conversation = Conversation(
            user_message=user,
            bot_response=bot,
            timestamp=datetime.now()
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        return {
            "id": conversation.id,
            "user": user,
            "bot": bot,
            "timestamp": conversation.timestamp.isoformat()
        }
    except Exception as e:
        db.rollback()
        print(f"Error adding to memory: {e}")
        return None

def save_image_choice(choice_index, image_metadata, message_text):
    """Save selected image choice to database"""
    try:
        image_selection = ImageSelection(
            choice_index=choice_index,
            mood_type=image_metadata.get("mood_type"),
            emoji=image_metadata.get("emoji"),
            image_url=image_metadata.get("url"),
            user_message=message_text,
            timestamp=datetime.now()
        )
        db.add(image_selection)
        db.commit()
        db.refresh(image_selection)
        
        return {
            "id": image_selection.id,
            "choice_index": choice_index,
            "mood_type": image_metadata.get("mood_type"),
            "emoji": image_metadata.get("emoji"),
            "image_url": image_metadata.get("url"),
            "user_message": message_text,
            "timestamp": image_selection.timestamp.isoformat()
        }
    except Exception as e:
        db.rollback()
        print(f"Error saving image choice: {e}")
        return None

def get_memory():
    """Get current chat history from database"""
    try:
        conversations = db.query(Conversation).all()
        return [
            {
                "id": c.id,
                "user": c.user_message,
                "bot": c.bot_response,
                "timestamp": c.timestamp.isoformat()
            }
            for c in conversations
        ]
    except Exception as e:
        print(f"Error getting memory: {e}")
        return []


def load_all_conversations():
    """Load all stored conversations from database"""
    try:
        conversations = db.query(Conversation).all()
        return [
            {
                "id": c.id,
                "user": c.user_message,
                "bot": c.bot_response,
                "timestamp": c.timestamp.isoformat()
            }
            for c in conversations
        ]
    except Exception as e:
        print(f"Error loading conversations: {e}")
        return []


def load_all_images():
    """Load all stored image selections from database"""
    try:
        images = db.query(ImageSelection).all()
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
    except Exception as e:
        print(f"Error loading images: {e}")
        return []
