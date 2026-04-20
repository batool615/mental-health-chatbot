from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict, List

import logging
from llm import generate_response
from analysis import analyze_state, analyze_choice
from images import generate_images_with_metadata
from memory import save_image_choice, add_to_memory

# إعداد وتجهيز ملف السجلات (logger)
import os
os.makedirs("data", exist_ok=True)
logging.basicConfig(
    filename='data/mental_health.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_history = []
last_user_message = ""
message_count = 0  # Track conversation length for delayed image suggestion
image_suggestion_made = False  # Track if images have been suggested

# Therapy suggestions database
THERAPY_SUGGESTIONS = {
    "calm": {
        "condition": "حالة هادئة ومطمئنة",
        "description": "يبدو أنك تشعر بالراحة والسلام الداخلي. قد تواجه ما يلي:",
        "symptoms": ["استرخاء", "راحة", "سلام داخلي", "استقرار"],
        "therapies": [
            "✨ **التأمل**: مارس التأمل لمدة 10-15 دقيقة يومياً",
            "🌿 **التواصل مع الطبيعة**: اقضِ وقتاً بالخارج لبقاء هذا الهدوء",
            "📔 **كتابة الامتنان**: اكتب 3 أشياء تشعر بالامتنان لها يومياً",
            "🎵 **الموسيقى الهادئة**: استمع إلى ألحان مريحة في الأوقات الهادئة"
        ]
    },
    "stressed": {
        "condition": "توتر وقلق",
        "description": "بناءً على حديثنا وحالتك، قد تكون تواجه ما يلي:",
        "symptoms": ["قلق", "توتر", "الانشغال الذهني", "الإجهاد"],
        "therapies": [
            "🫂 **العلاج السلوكي المعرفي**: حاول إعادة صياغة الأفكار المزعجة",
            "🧘 **تمارين التنفس العميق**: جرب نمط 4-4-4-4",
            "💪 **النشاط البدني**: مارس رياضة خفيفة لتحسين المزاج",
            "😴 **روتين نوم صحي**: حافظ على مواعيد نوم ثابتة",
            "👥 **الدعم الاجتماعي**: تحدث مع شخص تثق به",
            "🩺 **استشر أخصائي نفسي إذا استمرت الأعراض**"
        ]
    },
    "neutral": {
        "condition": "حالة نفسية متوازنة",
        "description": "يبدو أنك في حالة توازن. قد تكون تشعر بما يلي:",
        "symptoms": ["استقرار", "قبول", "قلق خفيف", "توازن"],
        "therapies": [
            "⚖️ **حافظ على التوازن**: استمر بالاستراتيجيات التي تعمل معك",
            "🎯 **حدد أهدافك**: ركز على خطوات صغيرة نحو أهدافك",
            "📚 **التأمل الذاتي**: اكتب يومياتك لتفهم مشاعرك أكثر",
            "🤝 **ابنِ علاقات أعمق**: تحدث مع من تثق به",
            "💡 **النمو الشخصي**: جرب مهارة جديدة أو هواية",
            "✅ **واصل روتين العناية بالنفس**"
        ]
    }
}

# ---------------- MODELS ----------------

class ChatRequest(BaseModel):
    message: str

class ChoiceRequest(BaseModel):
    choice: int
    image_metadata: dict
    message: str

# ---------------- RESET ----------------
@app.post("/reset")
def reset_session():
    global chat_history, last_user_message, message_count, image_suggestion_made
    chat_history = []
    last_user_message = ""
    message_count = 0
    image_suggestion_made = False
    return {"status": "ok"}

# ---------------- CHAT ----------------

@app.post("/chat")
def chat(req: ChatRequest):

    global chat_history, last_user_message, message_count, image_suggestion_made

    bot_reply = generate_response(req.message, chat_history)
    message_count += 1

    chat_history.append({
        "user": req.message,
        "bot": bot_reply
    })
    
    # تخزين في قاعدة البيانات (JSON) وفي ملف السجلات (Log)
    add_to_memory(req.message, bot_reply)
    logging.info(f"User Message: {req.message}")
    logging.info(f"Bot Reply: {bot_reply}")

    last_user_message = req.message
    state = analyze_state(req.message)
    
    # Check if distressed - suggest professional help
    if state.get("is_distressed"):
        return {
            "reply": state["message"],
            "state": state,
            "is_distressed": True,
            "suggest_images": False
        }

    # Suggest images after 4 user messages and not already suggested
    suggest_images = False
    image_prompt = ""
    if message_count >= 4 and not image_suggestion_made:
        suggest_images = True
        image_suggestion_made = True
        image_prompt = "\n\n💭 **الآن سأعرض لك بعض الصور. اختر الصورة التي تعبر عن حالتك النفسية الآن لكي أفهمك أفضل.**"
        bot_reply += image_prompt

    return {
        "reply": bot_reply,
        "state": state,
        "is_distressed": False,
        "suggest_images": suggest_images
    }

# -------- IMAGES --------

@app.get("/images")
def get_images():
    images = generate_images_with_metadata()
    return {
        "images": images,
        "prompt": "اختر الصورة التي تعبر عن حالتك النفسية الحالية"
    }

# -------- CHOOSE IMAGE --------

@app.post("/choose")
def choose_image(req: ChoiceRequest):
    global last_user_message
    
    analysis = analyze_choice(
        req.choice,
        req.image_metadata,
        last_user_message,
        chat_history
    )
    
    # Save image choice to database and log
    save_image_choice(req.choice, req.image_metadata, last_user_message)
    logging.info(f"Image Chosen by User: index {req.choice}, mood {req.image_metadata.get('mood_type')}, image_url: {req.image_metadata.get('url')}")
    
    mood_type = req.image_metadata.get("mood_type", "neutral")
    therapy_data = THERAPY_SUGGESTIONS.get(mood_type, THERAPY_SUGGESTIONS["neutral"])

    assessment_message = analysis.get("assessment", "")
    if analysis.get("is_distressed"):
        assessment_message += "\n\n⚠️ إذا شعرت أن حالتك النفسية خطرة، رجاءً تواصل مع استشاري نفسي أو مع الدعم المحلي فوراً."
        assessment_message += "\n\n📞 في الأردن: خط الدعم النفسي الوطني 065-218-850\n📍 يمكن أيضاً التواصل مع أقرب مستشفى أو مركز صحة نفسية لحجز موعد مع أخصائي نفسي."

    return {
        "analysis": assessment_message,
        "mood_type": mood_type,
        "image_url": req.image_metadata.get("url"),
        "details": {
            "stress_level": therapy_data["condition"],
            "therapies": therapy_data["therapies"]
        }
    }

# -------- ROOT --------

@app.get("/")
def root():
    return {"message": "Mental Chatbot API running 🚀"}

# -------- DEBUG/TEST --------

@app.get("/test")
def test_images():
    """Test endpoint - returns debug info and images"""
    images = generate_images_with_metadata()
    return {
        "status": "ok",
        "debug": "Image generation test",
        "images": images,
        "count": len(images)
    }