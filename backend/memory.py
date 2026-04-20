import json
import os
from datetime import datetime

# Path to store conversations and images
DB_DIR = "data"
CONVERSATIONS_FILE = os.path.join(DB_DIR, "conversations.json")
IMAGES_FILE = os.path.join(DB_DIR, "images.json")

# Create data directory if it doesn't exist
os.makedirs(DB_DIR, exist_ok=True)

chat_history = []

def _load_conversations():
    """Load conversations from file"""
    if os.path.exists(CONVERSATIONS_FILE):
        try:
            with open(CONVERSATIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def _save_conversations(data):
    """Save conversations to file"""
    with open(CONVERSATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _load_images():
    """Load selected images from file"""
    if os.path.exists(IMAGES_FILE):
        try:
            with open(IMAGES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def _save_images(data):
    """Save selected images to file"""
    with open(IMAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_to_memory(user, bot):
    """Add message to memory and save to file"""
    global chat_history
    
    message = {
        "user": user,
        "bot": bot,
        "timestamp": datetime.now().isoformat()
    }
    
    chat_history.append(message)
    
    # Save to file
    all_conversations = _load_conversations()
    all_conversations.append(message)
    _save_conversations(all_conversations)
    
    return message

def save_image_choice(choice_index, image_metadata, message_text):
    """Save selected image choice"""
    image_record = {
        "choice_index": choice_index,
        "mood_type": image_metadata.get("mood_type"),
        "emoji": image_metadata.get("emoji"),
        "image_url": image_metadata.get("url"),
        "user_message": message_text,
        "timestamp": datetime.now().isoformat()
    }
    
    # Save to file
    all_images = _load_images()
    all_images.append(image_record)
    _save_images(all_images)
    
    return image_record

def get_memory():
    """Get current chat history"""
    return chat_history

def load_all_conversations():
    """Load all stored conversations"""
    return _load_conversations()

def load_all_images():
    """Load all stored image selections"""
    return _load_images()
