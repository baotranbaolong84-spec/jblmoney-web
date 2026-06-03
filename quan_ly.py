import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. CẤU HÌNH API KEY TRỰC TIẾP
# ==========================================
# ⚠️ DÁN MÃ API CỦA BẠN VÀO GIỮA 2 DẤU NGOẶC KÉP BÊN DƯỚI:
API_KEY = "AQ.Ab8RN6IHlAOP8kXcPptRPWX2DhlTBIXPLKN8nK7YO_uDbAoyvA"

# ==========================================
# 2. GIAO DIỆN LUXURY GOLD 
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
# 3. HỆ THỐNG XỬ LÝ HÌNH ẢNH VÀ AI
# ==========================================
st.title("🍔 MẮT THẦN ĐO CALO")
st.markdown("<p style='text-align: center; color: #FCF6BA;'>Chụp ảnh đồ ăn, hệ thống sẽ tự động bóc tách thành phần và tính Calo</p>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("### 📸 CAMERA")
anh_do_an = st.camera_input("Đưa thức ăn vào giữa khung hình")

if anh_do_an:
    # Đọc ảnh trực tiếp từ bộ nhớ tạm
    img = Image.open(anh_do_an)
    
    if st.button("🔍 PHÂN TÍCH DỮ LIỆU"):
        if not API_KEY or API_KEY == "DÁN_MÃ_CỦA_BẠN_VÀO_ĐÂY":
            st.error("⚠️ Lỗi: Chưa cấu hình API Key ở dòng số 8 trong mã nguồn.")
        else:
            with st.spinner("🤖 Hệ thống đang phân tích hình ảnh... Vui lòng đợi..."):
                try:
                    # Cấu hình AI
                    genai.configure(api_key=API_KEY)
                    
                    lenh_cho_ai = """
                    Bạn là một chuyên gia dinh dưỡng chuyên nghiệp. 
                    Hãy nhìn bức ảnh đồ ăn này và thực hiện:
                    1. Nhận diện món ăn.
                    2. Liệt kê các thành phần chính.
                    3. Ước tính lượng Calo (Kcal) cho từng thành phần.
                    4. Tính TỔNG SỐ CALO của đĩa thức ăn.
                    5. Đưa ra 1 lời khuyên ngắn gọn về sức khỏe.
                    Trình bày bằng tiếng Việt, rõ ràng, chuẩn xác.
                    """
                    
                    # Thuật toán dự phòng tự động chuyển phiên bản AI
                    try:
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        response = model.generate_content([lenh_cho_ai, img])
                    except:
                        try:
                            model = genai.GenerativeModel('gemini-1.5-flash-latest')
                            response = model.generate_content([lenh_cho_ai, img])
                        except:
                            model = genai.GenerativeModel('gemini-pro-vision')
                            response = model.generate_content([lenh_cho_ai, img])
                    
                    # Hiển thị kết quả
                    st.balloons()
                    st.markdown("<div class='ai-box'>", unsafe_allow_html=True)
                    st.markdown("### 📊 KẾT QUẢ PHÂN TÍCH")
                    st.markdown(response.text)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Lỗi hệ thống: {e}")
