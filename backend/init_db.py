"""
Database initialization and migration script
This script initializes the MySQL database and optionally migrates existing JSON data
"""

import json
import os
from datetime import datetime
from sqlalchemy import create_engine, text

# MySQL Configuration
MYSQL_USER = "root"
MYSQL_PASSWORD = "12345"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DATABASE = "mental_chatbot"

# MySQL connection URL (without database for initial setup)
MYSQL_URL_WITHOUT_DB = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}"
MYSQL_URL_WITH_DB = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"


def create_database():
    """Create the MySQL database if it doesn't exist"""
    try:
        engine = create_engine(MYSQL_URL_WITHOUT_DB)
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}"))
            conn.commit()
        print(f"✓ Database '{MYSQL_DATABASE}' created or already exists")
        return True
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False


def migrate_json_to_db():
    """Migrate existing JSON data to MySQL database"""
    try:
        from database import SessionLocal, Conversation, ImageSelection
        
        db = SessionLocal()
        
        # Migrate conversations from JSON
        conversations_file = "data/conversations.json"
        if os.path.exists(conversations_file):
            with open(conversations_file, 'r', encoding='utf-8') as f:
                conversations = json.load(f)
            
            print(f"\n📥 Migrating {len(conversations)} conversations from JSON...")
            for conv in conversations:
                existing = db.query(Conversation).filter(
                    Conversation.user_message == conv.get('user'),
                    Conversation.bot_response == conv.get('bot')
                ).first()
                
                if not existing:
                    new_conv = Conversation(
                        user_message=conv.get('user', ''),
                        bot_response=conv.get('bot', ''),
                        timestamp=datetime.fromisoformat(conv.get('timestamp', datetime.now().isoformat()))
                    )
                    db.add(new_conv)
            
            db.commit()
            print("✓ Conversations migrated successfully!")
        
        # Migrate images from JSON
        images_file = "data/images.json"
        if os.path.exists(images_file):
            with open(images_file, 'r', encoding='utf-8') as f:
                images = json.load(f)
            
            print(f"\n📥 Migrating {len(images)} image selections from JSON...")
            for img in images:
                existing = db.query(ImageSelection).filter(
                    ImageSelection.image_url == img.get('image_url'),
                    ImageSelection.timestamp == datetime.fromisoformat(img.get('timestamp', datetime.now().isoformat()))
                ).first()
                
                if not existing:
                    new_img = ImageSelection(
                        choice_index=img.get('choice_index', 0),
                        mood_type=img.get('mood_type', ''),
                        emoji=img.get('emoji'),
                        image_url=img.get('image_url', ''),
                        user_message=img.get('user_message', ''),
                        timestamp=datetime.fromisoformat(img.get('timestamp', datetime.now().isoformat()))
                    )
                    db.add(new_img)
            
            db.commit()
            print("✓ Image selections migrated successfully!")
        
        db.close()
        return True
    
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False


def initialize_database():
    """Initialize MySQL database and create all tables"""
    print("=" * 60)
    print("🗄️  Initializing MySQL Database")
    print("=" * 60)
    
    # Step 1: Create database
    if not create_database():
        return False
    
    # Step 2: Create tables
    try:
        from database import init_db
        print("\n📋 Creating database tables...")
        init_db()
        print("✓ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    # Step 3: Migrate data
    try:
        from database import SessionLocal, Conversation, ImageSelection
        
        db = SessionLocal()
        conv_count = db.query(Conversation).count()
        img_count = db.query(ImageSelection).count()
        db.close()
        
        if conv_count == 0 and img_count == 0:
            if os.path.exists("data/conversations.json") or os.path.exists("data/images.json"):
                print("\n🔄 JSON files found. Migrating data to MySQL...")
                migrate_json_to_db()
            else:
                print("\n✓ Database is ready. No existing data to migrate.")
        else:
            print(f"\n✓ Database already has data:")
            print(f"   - Conversations: {conv_count}")
            print(f"   - Image selections: {img_count}")
    
    except Exception as e:
        print(f"⚠️  Warning during data check: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Database initialization complete!")
    print("=" * 60)
    print(f"\n📊 Database Details:")
    print(f"   Host: {MYSQL_HOST}:{MYSQL_PORT}")
    print(f"   Database: {MYSQL_DATABASE}")
    print(f"   User: {MYSQL_USER}")
    
    return True


if __name__ == "__main__":
    initialize_database()

