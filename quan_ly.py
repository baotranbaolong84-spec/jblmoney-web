import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. GIAO DIỆN LUXURY GOLD (SIÊU MƯỢT)
# ==========================================
st.set_page_config(page_title="VIP Calorie Scanner", page_icon="🍔", layout="centered")

st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp { background-color: #0a0a0a; color: #e0e0e0; }
    
    div.stButton > button {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        color: #000000 !important; font-weight: 900; border-radius: 8px;
        border: none; padding: 12px 24px; transition: all 0.4s ease;
        text-transform: uppercase; letter-spacing: 1px; width: 100%;
    }
    div.stButton > button:hover {
        transform: scale(1.05); box-shadow: 0 0 20px rgba(212, 175, 55, 0.6);
    }
    
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Georgia', serif; text-align: center; text-transform: uppercase;}
    .ai-box { background-color: #111111; border: 1px solid #D4AF37; border-radius: 12px; padding: 20px; margin-top: 20px; box-shadow: 0 8px 32px rgba(212, 175, 55, 0.15); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. APP SOI CALO ĐỒ ĂN TRỰC TIẾP (KHÔNG FIREBASE)
# ==========================================
st.title("🍔 AI MẮT THẦN ĐO CALO")
st.markdown("<p style='text-align: center; color: #FCF6BA;'>Chụp ảnh đồ ăn, AI sẽ bóc tách từng cọng hành và tính Calo cho Boss!</p>", unsafe_allow_html=True)
st.markdown("---")

# Ô nhập khóa AI an toàn 
api_key = st.text_input("🔑 Dán chìa khóa AI (AIza... hoặc AQ...) vào đây để cấp điện cho Mắt Thần:", type="password")

# Bật Camera trực tiếp
st.markdown("### 📸 MỞ CAMERA LÊN NÀO")
anh_do_an = st.camera_input("Đưa dĩa thức ăn vào giữa khung hình!")

if anh_do_an:
    # Đọc ảnh sống trực tiếp từ RAM, không lưu ổ cứng
    img = Image.open(anh_do_an)
    
    if st.button("🔍 AI XUẤT CHIÊU PHÂN TÍCH"):
        if not api_key:
            st.error("⚠️ Boss quên cắm chìa khóa AI kìa! Cắm vào ô bên trên nhé!")
        else:
            with st.spinner("🤖 AI đang soi từng hạt cơm... Boss đợi chút nhé..."):
                try:
                    # 1. Khởi động AI
                    genai.configure(api_key=api_key)
                    
                    # 2. Đọc lệnh cho AI
                    lenh_cho_ai = """
                    Bạn là một chuyên gia dinh dưỡng và thể hình cực kỳ chuyên nghiệp. 
                    Hãy nhìn bức ảnh đồ ăn này và thực hiện các nhiệm vụ sau:
                    1. Nhận diện đây là món ăn gì.
                    2. Liệt kê các thành phần chính có trong đĩa.
                    3. Ước tính lượng Calo (Kcal) cho từng thành phần.
                    4. Tính TỔNG SỐ CALO của cả đĩa thức ăn.
                    5. Đưa ra 1 lời khuyên ngắn gọn (Món này ăn béo không, hợp để tăng cơ hay giảm mỡ?).
                    Trình bày bằng tiếng Việt, rõ ràng, đẹp mắt, có dùng icon (emoji).
                    """
                    
                    # 3. CHIẾN THUẬT VÉT MÁNG TÌM ĐÚNG ĐỜI AI (CHỐNG LỖI 404)
                    try:
                        # Thử con 2.5 Flash mới nhất
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        response = model.generate_content([lenh_cho_ai, img])
                    except:
                        try:
                            # Lùi về 1.5 Flash nếu 2.5 chưa mở
                            model = genai.GenerativeModel('gemini-1.5-flash-latest')
                            response = model.generate_content([lenh_cho_ai, img])
                        except:
                            # Chốt hạ bằng bản Vision huyền thoại
                            model = genai.GenerativeModel('gemini-pro-vision')
                            response = model.generate_content([lenh_cho_ai, img])
                    
                    # 4. In kết quả 
                    st.balloons()
                    st.markdown("<div class='ai-box'>", unsafe_allow_html=True)
                    st.markdown("### 📊 KẾT QUẢ TỪ CHUYÊN GIA AI")
                    st.markdown(response.text)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Lỗi kết nối máy chủ: {e}\n\n👉 Boss nhớ kiểm tra lại file requirements.txt trên Github nhé!")
