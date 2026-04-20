import json
from llm import generate_image_analysis

# -------- SENTIMENT ANALYSIS --------

def get_text_sentiment(message):
    """Analyze text sentiment and return sentiment score (-1 to 1)"""
    message = message.lower()
    
    # Negative keywords (stress, anxiety, sadness)
    negative_keywords = [
        "توتر", "قلق", "حزين", "متعب", "تعبان", "مكتئب", "مضغوط", "ضغط",
        "stress", "anxiety", "sad", "tired", "depressed", "alone", "afraid",
        "خايف", "وحيد", "مكسور", "أنهكت", "ضاعت", "فقدان", "loss"
    ]
    
    # Positive keywords (calm, peaceful, happy)
    positive_keywords = [
        "هدوء", "سعيد", "بخير", "رايق", "تمام", "كويس", "أحسن", "أفضل",
        "calm", "happy", "peaceful", "good", "better", "fine", "relaxed",
        "ممتاز", "رائع", "جميل", "مستقر"
    ]
    
    negative_count = sum(1 for kw in negative_keywords if kw in message)
    positive_count = sum(1 for kw in positive_keywords if kw in message)
    
    sentiment = (positive_count - negative_count) / max(positive_count + negative_count, 1)
    return sentiment

# -------- STRESS CLASSIFICATION --------

def classify_stress_level(message, sentiment):
    """Classify stress level into Low, Moderate, or High"""
    message = message.lower()
    
    # High stress indicators
    high_stress_keywords = [
        "قلق شديد", "خوف", "فزع", "ذعر", "كارثة", "كوارث", "كسر", "مصيبة",
        "panic", "severe", "terrible", "horrible", "can't take", "breaking"
    ]
    
    # Moderate stress indicators
    moderate_stress_keywords = [
        "توتر", "ضغط", "مشاكل", "محبط", "خيبة", "تردد", "شك",
        "stress", "problem", "worried", "frustrated", "unsure"
    ]
    
    # Check for high stress keywords
    if any(kw in message for kw in high_stress_keywords) or sentiment < -0.6:
        return "High", "🚨"
    
    # Check for moderate stress keywords
    elif any(kw in message for kw in moderate_stress_keywords) or sentiment < -0.2:
        return "Moderate", "😔"
    
    # Otherwise low stress
    else:
        return "Low", "🌿"

# -------- SAFETY DETECTION --------

def detect_distress(message, stress_level):
    """Detect SEVERE emotional distress (only extreme cases)"""
    message = message.lower()
    
    # ONLY extreme distress keywords - not just "high stress"
    extreme_distress_keywords = [
        "انتحار", "suicide", "تؤذي نفسي", "harm myself", "الموت", "death",
        "لا فائدة", "hopeless", "لا أستطيع", "can't go on", "أنهي", "انهاء"
    ]
    
    # Only trigger if EXTREME keywords are found
    is_severe = any(kw in message for kw in extreme_distress_keywords)
    
    if is_severe:
        return True, {
            "warning": True,
            "message": "أنا قلق عليك 🤍\n\nإذا كنت تمر بأوقات صعبة جداً، رجاءً تواصل مع:\n\n📞 متخصص نفسي موثوق\n👤 شخص تثق به\n🚑 خط الطوارئ النفسية\n\nأنت لست وحدك. هناك من يريد مساعدتك ❤️"
        }
    
    return False, None

# -------- IMAGE MOOD ANALYSIS --------

def analyze_image_mood(image_metadata):
    """Analyze emotional meaning of selected image"""
    mood_type = image_metadata.get("mood_type", "neutral")
    
    mood_analysis = {
        "calm": {
            "text": "اخترت انعكاساً يعكس الهدوء والسلام 🌿",
            "sentiment": 0.7,
            "category": "peaceful"
        },
        "stressed": {
            "text": "اخترت انعكاساً يعبر عن المشاعر الصعبة الحالية 🌧️",
            "sentiment": -0.5,
            "category": "processing_emotions"
        },
        "neutral": {
            "text": "اخترت انعكاساً متوازناً بين الواقع والأمل ☁️",
            "sentiment": 0.0,
            "category": "balanced"
        }
    }
    
    return mood_analysis.get(mood_type, mood_analysis["neutral"])

# -------- COMBINED ANALYSIS --------

def analyze_state(message):
    """Analyze text sentiment and return state"""
    sentiment = get_text_sentiment(message)
    stress_level, emoji = classify_stress_level(message, sentiment)
    
    # Check for distress
    is_distressed, safety_response = detect_distress(message, stress_level)
    
    if is_distressed:
        return {
            "stress_level": stress_level,
            "sentiment": sentiment,
            "is_distressed": True,
            "message": safety_response["message"]
        }
    
    return {
        "stress_level": stress_level,
        "sentiment": sentiment,
        "is_distressed": False,
        "emoji": emoji
    }

def analyze_choice(choice, image_metadata, message_text, chat_history):
    """Analyze combined text + image choice for psychological assessment"""
    
    # Get text analysis
    sentiment = get_text_sentiment(message_text)
    stress_level, _ = classify_stress_level(message_text, sentiment)
    is_distressed, distress_msg = detect_distress(message_text, stress_level)
    
    # Get image analysis
    image_mood = analyze_image_mood(image_metadata)
    image_sentiment = image_mood["sentiment"]
    
    # Combined analysis
    combined_sentiment = (sentiment + image_sentiment) / 2
    
    # Determine psychological assessment
    ai_assessment = generate_image_analysis(message_text, image_mood['text'], stress_level)
    
    if ai_assessment:
        assessment = f"🧠 تقييم تفاعلي:\n\n{ai_assessment}"
    else:
        # Fallback in case of API failure
        if stress_level == "High" and image_metadata.get("mood_type") == "calm":
            assessment = f"🧠 تحليل نفسي:\n\nاخترت صورة هادئة بينما تشعر بضغط نفسي - هذا يشير إلى:{image_mood['text']}\n\nيبدو أنك تحتاج:\n• استرخاء وسلام داخلي 🌿\n• وقت لنفسك\n• ربما دعم من شخص تثق به\n\nجرب التركيز على اللحظة الحالية والتنفس الهادئ عند الشعور بالضغط."
        
        elif stress_level == "Moderate":
            assessment = f"🧠 تحليل نفسي:\n\n{image_mood['text']}\n\nحالتك النفسية: متوسطة التوتر 😔\n\nتوصيات:\n• تقبل مشاعرك الحالية\n• تحدث مع من تثق به\n• خذ فترات راحة منتظمة\n• لا تترددوا في طلب دعم مختص إذا لزمت الحاجة"
        
        else:  # Low stress
            assessment = f"🧠 تحليل نفسي:\n\n{image_mood['text']}\n\nحالتك النفسية: مستقرة ومتوازنة 🌿\n\nواصل الاهتمام بنفسك واستمتع بهذه اللحظات الإيجابية!"
    
    # Add safety message if extreme distress detected
    if is_distressed:
        assessment += f"\n\n---\n\n{distress_msg['message']}"
    
    return {
        "assessment": assessment,
        "stress_level": stress_level,
        "text_sentiment": sentiment,
        "image_mood": image_metadata.get("mood_type"),
        "combined_sentiment": combined_sentiment,
        "is_distressed": is_distressed
    }