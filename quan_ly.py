import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime

# =======================================
# 1. CẤU HÌNH TRANG & GIAO DIỆN CHUYÊN NGHIỆP
# =======================================
st.set_page_config(page_title="Boss Super Workspace", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    /* Ẩn menu mặc định của Streamlit cho giống web thật */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Thiết kế thẻ Card sang trọng */
    .st-emotion-cache-1r6slb0 { background-color: #1E1E2E; border-radius: 15px; padding: 20px; border: 1px solid #333; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    
    /* Làm đẹp các nút bấm */
    div.stButton > button { background: linear-gradient(135deg, #6e8efb, #a777e3); color: white; font-weight: bold; border-radius: 8px; border: none; transition: 0.3s; }
    div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
    
    /* Màu sắc tiêu đề */
    h1 { color: #ffffff; font-weight: 800; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-transform: uppercase; letter-spacing: 2px;}
    h2, h3 { color: #a777e3; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# =======================================
# 2. HỆ THỐNG LƯU TRỮ CSV
# =======================================
FILES = {'gym': 'gym_data.csv', 'eng': 'eng_data.csv', 'fashion': 'fashion_data.csv', 'movie': 'movie_data.csv'}

def load_data(file_name, columns):
    if os.path.exists(file_name):
        try: return pd.read_csv(file_name)
        except: pass
    return pd.DataFrame(columns=columns)

def save_data(df, file_name):
    df.to_csv(file_name, index=False)

df_gym = load_data(FILES['gym'], ['Ngày', 'Nhóm cơ / Môn', 'Thành tích', 'Ghi chú'])
df_eng = load_data(FILES['eng'], ['Ngày', 'Từ vựng', 'Nghĩa', 'Ví dụ', 'Đã thuộc'])
df_fashion = load_data(FILES['fashion'], ['Tên món đồ', 'Thương hiệu', 'Loại', 'Màu sắc'])
df_movie = load_data(FILES['movie'], ['Ngày xem', 'Tên phim', 'Rạp', 'Điểm (1-10)'])

# =======================================
# 3. SIDEBAR - THÔNG TIN CÁ NHÂN & BẢO TRÌ AI
# =======================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.markdown("## 👑 BẢNG ĐIỀU KHIỂN")
    st.markdown("---")
    
    # Khu vực AI đã được đưa vào bảo trì
    st.warning("🚧 TRỢ LÝ AI ĐANG BẢO TRÌ")
    st.caption("Hệ thống AI đang được nâng cấp. Các tính năng tự động cục bộ vẫn hoạt động bình thường 100%.")
    
    st.markdown("---")
    st.markdown("### 📊 Tổng quan nhanh:")
    st.metric("💪 Tổng buổi tập", f"{len(df_gym)} buổi")
    st.metric("📚 Từ vựng đã nạp", f"{len(df_eng)} từ")
    st.metric("🍿 Phim đã cày", f"{len(df_movie)} bộ")

# =======================================
# 4. GIAO DIỆN CHÍNH - MENU ĐIỀU HƯỚNG
# =======================================
st.title("⚡ TRUNG TÂM KIỂM SOÁT CÁ NHÂN")

# Sử dụng Tab như Menu Bar của Website
t_gym, t_eng, t_fash, t_mov = st.tabs(["💪 GYM & FITNESS", "📚 ENGLISH ARENA", "🧢 STREETWEAR WARDROBE", "🎬 MOVIE STATION"])

# ---------------------------------------
# KHU 1: GYM & FITNESS (THÊM CÔNG CỤ BMI)
# ---------------------------------------
with t_gym:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Báo cáo Cơ Thể")
        with st.form("bmi_calc"):
            cao = st.number_input("Chiều cao (cm)", min_value=100, max_value=250, value=170)
            nang = st.number_input("Cân nặng (kg)", min_value=30, max_value=200, value=65)
            if st.form_submit_button("Tính BMI", use_container_width=True):
                bmi = nang / ((cao/100)**2)
                st.info(f"Chỉ số BMI của bạn: **{bmi:.1f}**")
                if bmi < 18.5: st.warning("Hơi gầy, ráng ăn nhiều lên Boss!")
                elif 18.5 <= bmi < 25: st.success("Body chuẩn đét!")
                else: st.error("Đang thừa mỡ rồi, cardio gấp!")

    with c2:
        st.subheader("Thêm Buổi Tập Mới")
        with st.form("form_gym", clear_on_submit=True):
            col1, col2 = st.columns(2)
            ngay_tap = col1.date_input("Ngày tập")
            mon_tap = col2.selectbox("Nhóm cơ / Môn", ["Ngực - Tay sau", "Lưng - Tay trước", "Chân - Mông - Bụng", "Cardio/Bơi lội", "Khác"])
            thanh_tich = st.text_input("Ghi nhận (VD: Đẩy ngực 60kg - 4 hiệp, Bơi 2km)")
            if st.form_submit_button("LƯU KẾT QUẢ", use_container_width=True):
                moi = pd.DataFrame([{'Ngày': str(ngay_tap), 'Nhóm cơ / Môn': mon_tap, 'Thành tích': thanh_tich, 'Ghi chú': ''}])
                df_gym = pd.concat([df_gym, moi], ignore_index=True)
                save_data(df_gym, FILES['gym'])
                st.success("Đã ghi nhận buổi tập!")
                st.rerun()
    st.markdown("---")
    st.dataframe(df_gym, use_container_width=True, hide_index=True)

# ---------------------------------------
# KHU 2: TIẾNG ANH (THÊM FLASHCARD ÔN TẬP)
# ---------------------------------------
with t_eng:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("Nạp Từ Mới")
        with st.form("form_eng", clear_on_submit=True):
            tu_vung = st.text_input("Từ vựng tiếng Anh")
            nghia = st.text_input("Nghĩa tiếng Việt")
            vi_du = st.text_area("Câu ví dụ")
            if st.form_submit_button("LƯU TỪ", use_container_width=True):
                moi = pd.DataFrame([{'Ngày': str(datetime.now().date()), 'Từ vựng': tu_vung, 'Nghĩa': nghia, 'Ví dụ': vi_du, 'Đã thuộc': 'Chưa'}])
                df_eng = pd.concat([df_eng, moi], ignore_index=True)
                save_data(df_eng, FILES['eng'])
                st.success("Lưu thành công!")
                st.rerun()
    with c2:
        st.subheader("Đấu Trường Kiểm Tra (Flashcard)")
        if not df_eng.empty:
            if st.button("🔀 Rút Ngẫu Nhiên 1 Từ", use_container_width=True):
                tu_nga_nhien = df_eng.sample(1).iloc[0]
                st.info(f"### Từ khóa: **{tu_nga_nhien['Từ vựng']}**")
                with st.expander("Bấm vào đây để xem đáp án"):
                    st.write(f"👉 **Nghĩa:** {tu_nga_nhien['Nghĩa']}")
                    st.write(f"📝 **Ví dụ:** {tu_nga_nhien['Ví dụ']}")
        else:
            st.warning("Kho từ vựng trống. Hãy nhập từ mới trước!")
    
    st.markdown("---")
    st.dataframe(df_eng, use_container_width=True, hide_index=True)

# ---------------------------------------
# KHU 3: THỜI TRANG (THÊM TỰ ĐỘNG PHỐI ĐỒ)
# ---------------------------------------
with t_fash:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Nhập Hàng Vào Tủ")
        with st.form("form_fashion", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            ten_do = col_a.text_input("Tên món (Áo thun rách, Quần túi hộp...)")
            brand = col_b.selectbox("Thương hiệu", ["Saigon Swagger", "Dirty Coins", "Tèoboki", "SWE", "Khác"])
            loai_do = col_a.selectbox("Phân loại", ["Áo", "Quần", "Giày", "Phụ kiện"])
            mau_sac = col_b.text_input("Màu chủ đạo")
            if st.form_submit_button("CẤT VÀO TỦ", use_container_width=True):
                moi = pd.DataFrame([{'Tên món đồ': ten_do, 'Thương hiệu': brand, 'Loại': loai_do, 'Màu sắc': mau_sac}])
                df_fashion = pd.concat([df_fashion, moi], ignore_index=True)
                save_data(df_fashion, FILES['fashion'])
                st.success("Đã treo lên móc!")
                st.rerun()
                
    with c2:
        st.subheader("Gợi Ý Lên Đồ")
        st.caption("Thuật toán tự động mix đồ không cần AI.")
        if st.button("🎲 Hôm nay mặc gì?", type="primary", use_container_width=True):
            ao = df_fashion[df_fashion['Loại'] == 'Áo']
            quan = df_fashion[df_fashion['Loại'] == 'Quần']
            if not ao.empty and not quan.empty:
                chọn_ao = ao.sample(1).iloc[0]
                chọn_quan = quan.sample(1).iloc[0]
                st.success(f"**Top:** {chọn_ao['Tên món đồ']} ({chọn_ao['Màu sắc']})\n\n**Bottom:** {chọn_quan['Tên món đồ']} ({chọn_quan['Màu sắc']})")
                st.balloons()
            else:
                st.error("Tủ đồ chưa đủ cả Áo và Quần để mix!")
                
    st.markdown("---")
    st.dataframe(df_fashion, use_container_width=True, hide_index=True)

# ---------------------------------------
# KHU 4: PHIM ẢNH (THÊM CHẤM ĐIỂM)
# ---------------------------------------
with t_mov:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Thống Kê Điện Ảnh")
        if not df_movie.empty:
            diem_tb = pd.to_numeric(df_movie['Điểm (1-10)'], errors='coerce').mean()
            st.metric("Điểm phim trung bình", f"{diem_tb:.1f} / 10")
            st.write("**Top rạp hay đi:**")
            st.bar_chart(df_movie['Rạp'].value_counts())
        else:
            st.info("Chưa có dữ liệu thống kê.")
            
    with c2:
        st.subheader("Lưu Dấu Chân Phim")
        with st.form("form_movie", clear_on_submit=True):
            col_x, col_y = st.columns(2)
            ngay_xem = col_x.date_input("Ngày xem")
            ten_phim = col_y.text_input("Tên phim")
            rap = col_x.selectbox("Xem ở đâu", ["Galaxy Sala", "CGV", "Lotte", "Netflix ở nhà", "Khác"])
            danh_gia = col_y.number_input("Chấm điểm (1-10)", min_value=1, max_value=10, value=8)
            if st.form_submit_button("LƯU CUỐN PHIM NÀY", use_container_width=True):
                moi = pd.DataFrame([{'Ngày xem': str(ngay_xem), 'Tên phim': ten_phim, 'Rạp': rap, 'Điểm (1-10)': danh_gia}])
                df_movie = pd.concat([df_movie, moi], ignore_index=True)
                save_data(df_movie, FILES['movie'])
                st.success("Tuyệt vời!")
                st.rerun()
                
    st.markdown("---")
    st.dataframe(df_movie, use_container_width=True, hide_index=True)
