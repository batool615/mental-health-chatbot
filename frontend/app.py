import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="NAFSI",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon="🧠"
)

# Minimalist modern CSS
st.markdown("""
<style>
    /* Prevent raw global resets from breaking Streamlit grids */
    .stApp {
        background: #F4F7F6; /* مريح وهادئ للنفس */
    }

    /* Hide standard header/footer */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    footer {
        display: none !important;
    }

    .welcome-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 10vh;
        gap: 32px;
        text-align: center;
    }

    .robot-avatar {
        width: 140px;
        height: 140px;
        background: #CAD2C5;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 80px;
        color: #2F3E46 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        border: 2px solid #84A98C;
        animation: float 3s ease-in-out infinite;
        margin: 0 auto;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }

    .welcome-title {
        font-size: 48px;
        font-weight: 900;
        color: #2F3E46 !important;
        margin-top: 20px;
    }

    .welcome-subtitle {
        font-size: 18px;
        color: #52796F;
        line-height: 1.6;
        max-width: 420px;
        margin: 10px auto 30px auto;
    }

    .chat-header {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 20px;
        background: #FFFFFF;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid #CAD2C5;
        margin-bottom: 20px;
    }

    .header-avatar {
        width: 64px;
        height: 64px;
        background: #CAD2C5;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 34px;
        color: #2F3E46 !important;
        border: 1px solid #84A98C;
    }

    .header-text h3 {
        font-size: 20px;
        font-weight: 800;
        color: #2F3E46;
        margin: 0;
    }

    .header-text p {
        font-size: 14px;
        color: #52796F;
        margin: 4px 0 0;
    }

    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 14px;
        min-height: 200px;
        text-align: center;
        color: #52796F;
    }

    .empty-state-icon {
        font-size: 58px;
        opacity: 0.8;
    }
    
    .message-bubble {
        padding: 14px 18px;
        border-radius: 20px;
        font-size: 15px;
        line-height: 1.6;
        word-wrap: break-word;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
        margin-bottom: 15px;
    }

    .message-bubble.bot {
        background: #FFFFFF;
        color: #2F3E46;
        border: 1px solid #E2E8F0;
        border-bottom-right-radius: 6px;
    }

    .message-bubble.user {
        background: #D1E8E2;
        color: #19535F;
        border: 1px solid #B0D0D3;
        border-bottom-left-radius: 6px;
        text-align: right;
    }

    .image-selector-title {
        font-size: 16px;
        font-weight: 700;
        color: #2F3E46;
        margin-bottom: 14px;
        text-align: center;
    }

</style>
""", unsafe_allow_html=True)

# Initialize session state
if "session_started" not in st.session_state:
    st.session_state.session_started = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_images" not in st.session_state:
    st.session_state.current_images = None
if "show_images" not in st.session_state:
    st.session_state.show_images = False
if "image_selected" not in st.session_state:
    st.session_state.image_selected = False

# Welcome Screen
if not st.session_state.session_started:
    st.markdown("""
        <div class="welcome-wrapper">
            <div class="robot-avatar">🤖</div>
            <h1 class="welcome-title">NAFSI</h1>
            <p class="welcome-subtitle">مساعدك الذكي للصحة النفسية<br>دعني أساعدك لتشعر بتحسن 💚</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 ابدأ الآن", key="start_button", use_container_width=True):
            try:
                requests.post(f"{API_URL}/reset", timeout=5)
            except Exception:
                pass
            
            st.session_state.messages = []
            st.session_state.current_images = None
            st.session_state.show_images = False
            st.session_state.image_selected = False
            st.session_state.session_started = True
            st.rerun()

else:
    # Header
    st.markdown("""
    <div class="chat-header">
        <div class="header-avatar">🤖</div>
        <div class="header-text">
            <h3>NAFSI</h3>
            <p>مساعدك الذكي - متصل الآن ✨</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Messages display
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">💬</div>
            <div>ابدأ بكتابة رسالتك...</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="message-bubble user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                if msg.get("type") == "image":
                    img_url = msg["content"].replace("![selected-image](", "").replace(")", "")
                    st.image(img_url, use_container_width=True)
                else:
                    st.markdown(f'<div class="message-bubble bot">{msg["content"]}</div>', unsafe_allow_html=True)

    # Image selector
    if st.session_state.show_images and st.session_state.current_images and not st.session_state.image_selected:
        st.write("---")
        st.markdown('<div class="image-selector-title">🎨 اختر الصورة التي تعبر عن حالتك</div>', unsafe_allow_html=True)

        cols = st.columns(3)
        for i, img_data in enumerate(st.session_state.current_images):
            with cols[i]:
                img_url = img_data.get("url", "")
                emoji = img_data.get("emoji", "")

                if img_url:
                    st.image(img_url, use_container_width=True)
                    if st.button(f"اختر {emoji}", key=f"img_select_{i}", use_container_width=True):
                        last_user_msg = ""
                        for msg in reversed(st.session_state.messages):
                            if msg["role"] == "user":
                                last_user_msg = msg["content"]
                                break
                        try:
                            analysis_res = requests.post(f"{API_URL}/choose", json={"choice": i, "image_metadata": img_data, "message": last_user_msg}, timeout=10)
                            analysis_data = analysis_res.json()
                            assessment = analysis_data.get("analysis", "")
                            image_url = analysis_data.get("image_url", "")

                            if image_url:
                                st.session_state.messages.append({"role": "assistant", "content": f"![selected-image]({image_url})", "type": "image"})

                            st.session_state.messages.append({"role": "assistant", "content": assessment})
                            st.session_state.image_selected = True
                            st.session_state.show_images = False
                            st.rerun()
                        except Exception as e:
                            st.session_state.messages.append({"role": "assistant", "content": f"🚨 حدث خطأ أثناء تحليل الصورة: {str(e)}"})
                            st.rerun()

    # Input area
    st.write("---")
    with st.form(key="input_form", clear_on_submit=True):
        user_input = st.text_input("رسالتك", placeholder="اكتب رسالتك...", key="nafsi_user_input", label_visibility="collapsed")
        submit_input = st.form_submit_button("أرسل رسالة")

        if submit_input and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            try:
                res = requests.post(f"{API_URL}/chat", json={"message": user_input}, timeout=60)
                if res.status_code == 200:
                    data = res.json()
                    bot_reply = data.get("reply", "عذراً، حدث خطأ")
                    suggest_images = data.get("suggest_images", False)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

                    if suggest_images:
                        try:
                            img_res = requests.get(f"{API_URL}/images", timeout=10)
                            img_data = img_res.json()
                            images = img_data.get("images", [])
                            if images:
                                st.session_state.current_images = images
                                st.session_state.show_images = True
                        except Exception:
                            pass
                else:
                    st.session_state.messages.append({"role": "assistant", "content": f"🚨 الخادم أرجع خطأ: {res.status_code} - {res.text}"})
                st.rerun()
            except Exception as e:
                st.session_state.messages.append({"role": "assistant", "content": f"🚨 خطأ في الاتصال: تأكد من أن الخادم (FastAPI) يعمل.\n\n التفاصيل: {str(e)}"})
                st.rerun()
