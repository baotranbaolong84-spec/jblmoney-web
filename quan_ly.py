import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from datetime import datetime

# =======================================
# 1. CẤU HÌNH TRANG WEB CHUẨN XỊN
# =======================================
st.set_page_config(page_title="Boss Super App", page_icon="🔥", layout="wide")

st.markdown("""
<style>
    div.stButton > button { background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%) !important; color: white !important; font-weight: bold !important; border-radius: 8px !important; border: none !important; }
    div.stButton > button:hover { opacity: 0.8 !important; }
    h1, h2, h3 { color: #00C9FF !important; }
</style>
""", unsafe_allow_html=True)

# =======================================
# 2. HỆ THỐNG LƯU TRỮ CSV RIÊNG BIỆT
# =======================================
FILES = {'gym': 'gym_data.csv', 'eng': 'eng_data.csv', 'fashion': 'fashion_data.csv', 'movie': 'movie_data.csv'}

def load_data(file_name, columns):
    if os.path.exists(file_name):
        try: return pd.read_csv(file_name)
        except: pass
    return pd.DataFrame(columns=columns)

def save_data(df, file_name):
    df.to_csv(file_name, index=False)

df_gym = load_data(FILES['gym'], ['Ngày', 'Loại', 'Thành tích', 'Ghi chú'])
df_eng = load_data(FILES['eng'], ['Ngày', 'Từ vựng', 'Nghĩa', 'Ví dụ'])
df_fashion = load_data(FILES['fashion'], ['Tên món đồ', 'Thương hiệu', 'Loại', 'Màu sắc'])
df_movie = load_data(FILES['movie'], ['Ngày xem', 'Tên phim', 'Rạp', 'Đánh giá'])

# =======================================
# 3. SIDEBAR - CHÌA KHÓA & TRỢ LÝ AI ĐA NĂNG
# =======================================
with st.sidebar:
    st.markdown("### 🔑 Khởi Động Trợ Lý AI")
    khoa_api = st.text_input("Dán mã AIza hoặc AQ của Boss vào đây:", type="password")
    
    st.markdown("---")
    st.markdown("### 🤖 Trợ Lý Đa Năng")
    chat_box = st.container(height=400, border=True)
    
    if "chat" not in st.session_state: 
        st.session_state.chat = [{"role": "assistant", "content": "Siêu ứng dụng 4-in-1 đã sẵn sàng! Boss muốn check lịch tập, học từ vựng, phối đồ hay tìm phim?"}]
        
    for msg in st.session_state.chat: 
        chat_box.chat_message(msg["role"]).write(msg["content"])
    
    if q := st.chat_input("Ra lệnh cho AI..."):
        if not khoa_api:
            st.error("⚠️ Boss nhập chìa khóa ở trên kìa!")
        else:
            st.session_state.chat.append({"role": "user", "content": q})
            chat_box.chat_message("user").write(q)
            try:
                genai.configure(api_key=khoa_api)
                model = genai.GenerativeModel('gemini-1.5-flash')
                # Nhồi ngữ cảnh dữ liệu 4 mảng cho AI
                context = f"Dữ liệu Boss: \n- Đồ streetwear: {df_fashion.to_string()} \n- Phim đã xem: {df_movie.to_string()} \n- Lịch tập: {df_gym.to_string()} \nHãy trả lời câu hỏi sau như một người trợ lý đắc lực, ngầu và hài hước: {q}"
                ans = model.generate_content(context)
                chat_box.chat_message("assistant").write(ans.text)
                st.session_state.chat.append({"role": "assistant", "content": ans.text})
            except Exception as e:
                st.error(f"Lỗi AI: {e}")

# =======================================
# 4. GIAO DIỆN CHÍNH - 4 PHÂN KHU
# =======================================
st.title("🔥 KHO CHỈ HUY CÁ NHÂN TỐI THƯỢNG 🔥")
tab1, tab2, tab3, tab4 = st.tabs(["🏋️ CƠ BẮP & BƠI LỘI", "🇬🇧 ĐẤU TRƯỜNG ENGLISH", "🧢 TỦ ĐỒ STREETWEAR", "🍿 RẠP PHIM GALAXY"])

# --- KHU 1: GYM & BƠI LỘI ---
with tab1:
    st.markdown("### 🏋️ Ghi Chép Luyện Tập")
    with st.form("form_gym", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        ngay_tap = c1.date_input("Ngày tập")
        loai_tap = c2.selectbox("Môn tập", ["Gym", "Bơi lội", "Khác"])
        thanh_tich = c3.text_input("Thành tích (VD: Đẩy 50kg, Bơi 20 vòng)")
        ghi_chu_gym = st.text_input("Ghi chú")
        if st.form_submit_button("LƯU BUỔI TẬP"):
            moi = pd.DataFrame([{'Ngày': str(ngay_tap), 'Loại': loai_tap, 'Thành tích': thanh_tich, 'Ghi chú': ghi_chu_gym}])
            df_gym = pd.concat([df_gym, moi], ignore_index=True)
            save_data(df_gym, FILES['gym'])
            st.success("Đã lưu lịch tập!")
            st.rerun()
    st.dataframe(df_gym, use_container_width=True)

# --- KHU 2: TIẾNG ANH ---
with tab2:
    st.markdown("### 🇬🇧 Nạp Từ Vựng Mỗi Ngày")
    with st.form("form_eng", clear_on_submit=True):
        c1, c2 = st.columns(2)
        tu_vung = c1.text_input("Từ mới")
        nghia = c2.text_input("Nghĩa tiếng Việt")
        vi_du = st.text_input("Câu ví dụ (Tùy chọn)")
        if st.form_submit_button("LƯU TỪ VỰNG"):
            moi = pd.DataFrame([{'Ngày': str(datetime.now().date()), 'Từ vựng': tu_vung, 'Nghĩa': nghia, 'Ví dụ': vi_du}])
            df_eng = pd.concat([df_eng, moi], ignore_index=True)
            save_data(df_eng, FILES['eng'])
            st.success("Đã nạp thêm đạn từ vựng!")
            st.rerun()
    st.dataframe(df_eng, use_container_width=True)

# --- KHU 3: STREETWEAR ---
with tab3:
    st.markdown("### 🧢 Quản Lý Tủ Đồ Hiphop")
    with st.form("form_fashion", clear_on_submit=True):
        c1, c2 = st.columns(2)
        ten_do = c1.text_input("Tên món đồ (VD: Áo thun Oversize)")
        brand = c2.selectbox("Thương hiệu", ["Saigon Swagger", "Dirty Coins", "SWE", "Tự do", "Khác"])
        loai_do = st.selectbox("Phân loại", ["Áo", "Quần", "Giày", "Phụ kiện (Mũ, Kính, Túi...)"])
        mau_sac = st.text_input("Màu sắc")
        if st.form_submit_button("CẤT VÀO TỦ"):
            moi = pd.DataFrame([{'Tên món đồ': ten_do, 'Thương hiệu': brand, 'Loại': loai_do, 'Màu sắc': mau_sac}])
            df_fashion = pd.concat([df_fashion, moi], ignore_index=True)
            save_data(df_fashion, FILES['fashion'])
            st.success("Đã update tủ đồ!")
            st.rerun()
    st.dataframe(df_fashion, use_container_width=True)
    if st.button("🔥 Mặc gì hôm nay (Hỏi AI)", use_container_width=True):
        st.info("Boss hãy sang ô Chat AI bên trái, nhập: 'Hôm nay tôi đi cháy phố, hãy mix cho tôi 1 bộ từ tủ đồ!'")

# --- KHU 4: RẠP PHIM ---
with tab4:
    st.markdown("### 🍿 Nhật Ký Điện Ảnh")
    with st.form("form_movie", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        ngay_xem = c1.date_input("Ngày xem phim")
        ten_phim = c2.text_input("Tên phim")
        rap = c3.selectbox("Rạp chiếu", ["Galaxy Sala", "CGV", "Lotte", "Xem ở nhà"])
        danh_gia = st.slider("Chấm điểm (1-10 ⭐️)", 1, 10, 8)
        if st.form_submit_button("LƯU PHIM"):
            moi = pd.DataFrame([{'Ngày xem': str(ngay_xem), 'Tên phim': ten_phim, 'Rạp': rap, 'Đánh giá': f"{danh_gia} ⭐️"}])
            df_movie = pd.concat([df_movie, moi], ignore_index=True)
            save_data(df_movie, FILES['movie'])
            st.success("Đã lưu nhật ký xem phim!")
            st.rerun()
    st.dataframe(df_movie, use_container_width=True)
