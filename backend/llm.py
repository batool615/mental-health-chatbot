import requests

API_KEY = "tZFrCZcfWe4foAovR7Ct8tfkI3NA6WVg"


def generate_response(user_input, history):

    try:
        import json
        import os
        therapists_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'therapists_jordan.json')
        with open(therapists_path, 'r', encoding='utf-8') as f:
            therapists_data = json.load(f)
            
        therapists_text = "إذا سأل أو طلب المستخدم مساعدة طبية، أرقام هواتف، أو البحث عن طبيب/أخصائي/مركز نفسي في الأردن، أو شعرت من كلامه أنه يعاني بشدة أو لديه ميول خطرة، اقترح عليه بأسلوب دافئ هذه الخيارات الأردنية (واذكر تفاصيلها له):\n"
        for t in therapists_data:
            therapists_text += f"- 🏥 {t['name']} ({t['location']}) - {t['specialty']} | هاتف: {t['contact']}\n"
    except Exception:
        therapists_text = ""

    messages = [
       {
    "role": "system",
    "content": f"""
أنت معالج نفسي داعم.

❗ مهم جداً:
- احكي باللهجة العربية (مش مصري، خليها عربية مفهومة)
- لا تستخدم الإنجليزية أبداً
- خليك دافئ، إنساني، وذكي
- اسأل أسئلة تساعد المستخدم يفضفض

{therapists_text}
"""
}
    ]

    for h in history:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["bot"]})

    messages.append({"role": "user", "content": user_input})

    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistral-small-latest",
                "messages": messages,
                "temperature": 0.6
            },
            timeout=30
        )
        
        if response.status_code != 200:
            return f"❌ عذراً، خدمة الذكاء الاصطناعي لا تستجيب حالياً (الرمز: {response.status_code}). الرجاء التأكد من مفتاح API."
            
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ خطأ غير متوقع في محرك التحدث: {str(e)}"

def generate_image_analysis(user_message, image_mood_text, stress_level):
    prompt = f"""
أنت معالج نفسي متمرس وذكي. المريض يتحدث معك مؤخراً وقال: "{user_message}"
ومستوى التوتر الحالي لديه مصنف كـ: "{stress_level}"
كما أنه للتو اختار صورة تعبر عن حالته النفسية، ومعناها: "{image_mood_text}"

بناءً على هذا، اكتب فقرة تحليلية دافئة جداً وداعمة (بالعربية المريحة المفهومة غير الرسمية) تشرح للمريض كيف ترتبط مشاعره الحالية بالصورة التي اختارها.
ثم بعد ذلك، اقترح عليه نشاطين أو ثلاثة أنشطة بالتحديد (Mental Health Habits) تناسب حالته لتطبيقها الآن لتلطيف مزاجه.
لا تطل كثيراً، بل كن مفيداً ومختصراً وحنوناً في نفس الوقت. استخدم الإيموجي المناسب.
"""
    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistral-small-latest",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.6
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return None
    except Exception:
        return None