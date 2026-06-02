import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime

# ==========================================
# 1. CẤU HÌNH GIAO DIỆN CHUYÊN NGHIỆP (UI/UX)
# ==========================================
st.set_page_config(page_title="Boss Life OS", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# Nhúng CSS custom để ép giao diện thành App xịn (Dark Mode, Bo góc, Nút nổi)
st.markdown("""
<style>
    /* Ẩn menu mặc định của Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Làm đẹp nút bấm toàn hệ thống */
    div.stButton > button {
        background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
        color: white; font-weight: bold; border-radius: 12px;
        border: none; padding: 10px 24px; transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%);
        color: #000;
    }
    
    /* Form nhập liệu */
    [data-testid="stForm"] {
        border-radius: 15px; border: 1px solid #444; background-color: #1E1E2E; padding: 20px;
    }
    
    /* Các con số thống kê (Metrics) */
    [data-testid="stMetricValue"] { font-size: 2.5rem; color: #00C9FF; font-weight: 800; }
    
    /* Thiết kế thẻ Card Custom bằng HTML */
    .custom-card {
        background-color: #252535; border-radius: 15px; padding: 20px; 
        margin-bottom: 15px; border-left: 5px solid #00C9FF;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2); transition: 0.3s;
    }
    .custom-card:hover { transform: translateX(5px); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HỆ THỐNG CƠ SỞ DỮ LIỆU (DATA ENGINE)
# ==========================================
# Tự động tạo file CSV nếu chưa có
FILE_GYM = 'gym_tracker.csv'
FILE_ENG = 'eng_vocab.csv'
FILE_FASH = 'fashion_closet.csv'
FILE_MOV = 'movie_diary.csv'

def load_db(file_name, columns):
    if os.path.exists(file_name):
        try: return pd.read_csv(file_name)
        except: pass
    return pd.DataFrame(columns=columns)

def save_db(df, file_name):
    df.to_csv(file_name, index=False)

# Tải toàn bộ dữ liệu khi mở web
df_gym = load_db(FILE_GYM, ['Ngày', 'Môn tập', 'Bài tập/Thành tích', 'Ghi chú'])
df_eng = load_db(FILE_ENG, ['Từ vựng', 'Nghĩa', 'Ví dụ', 'Ngày học'])
df_fash = load_db(FILE_FASH, ['Tên đồ', 'Loại', 'Thương hiệu', 'Màu sắc'])
df_mov = load_db(FILE_MOV, ['Tên phim', 'Rạp', 'Điểm', 'Ngày xem'])

# ==========================================
# 3. THANH ĐIỀU HƯỚNG (SIDEBAR NAVIGATION)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.markdown("## ⚡ LIFE OS")
    st.caption("Phiên bản V6 - Không cần API Key")
    st.markdown("---")
    
    menu = st.radio("ĐIỀU HƯỚNG:", 
                    ["🏠 Bảng Điều Khiển (Dashboard)", 
                     "💪 Hệ Thống Gym (Strong)", 
                     "🇬🇧 Trạm Tiếng Anh (Duolingo)", 
                     "🧢 Tủ Đồ Chất (Acloset)", 
                     "🎬 Nhật Ký Phim (Letterboxd)"])
    
    st.markdown("---")
    st.success("Tình trạng: Mạng cục bộ hoạt động 100%. Dữ liệu được lưu an toàn.")

# ==========================================
# 4. TRIỂN KHAI CÁC TRANG CHỨC NĂNG
# ==========================================

# ------------------------------------------
# TRANG 1: DASHBOARD (BẢNG TỔNG QUAN)
# ------------------------------------------
if menu == "🏠 Bảng Điều Khiển (Dashboard)":
    st.title("Hi Boss! Chúc một ngày năng suất! 👋")
    st.markdown("Dưới đây là báo cáo tổng hợp từ các trạm dữ liệu của Boss:")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🏋️ Số buổi đã tập", f"{len(df_gym['Ngày'].unique()) if not df_gym.empty else 0} Ngày")
    c2.metric("📚 Kho từ vựng", f"{len(df_eng)} Từ")
    c3.metric("🧢 Tủ đồ hiện tại", f"{len(df_fash)} Món")
    c4.metric("🎬 Số phim đã cày", f"{len(df_mov)} Bộ")
    
    st.markdown("---")
    st.markdown("### 🚀 Hoạt động mới nhất")
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("**Từ vựng mới nhất:** " + (df_eng.iloc[-1]['Từ vựng'] if not df_eng.empty else "Chưa có"))
    with col_b:
        st.warning("**Phim mới xem:** " + (df_mov.iloc[-1]['Tên phim'] if not df_mov.empty else "Chưa có"))

# ------------------------------------------
# TRANG 2: GYM TRACKER (Giống Hevy/Strong)
# ------------------------------------------
elif menu == "💪 Hệ Thống Gym (Strong)":
    st.title("💪 GYM & FITNESS TRACKER")
    
    # Khu vực ẩn để nhập dữ liệu (Tránh làm rối mắt)
    with st.expander("➕ THÊM BÀI TẬP / BUỔI TẬP MỚI", expanded=False):
        with st.form("gym_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            ngay_tap = col1.date_input("Ngày tập")
            mon_tap = col2.selectbox("Nhóm cơ / Môn", ["Ngực", "Lưng - Xô", "Chân - Mông", "Vai - Tay", "Cardio/Bơi lội"])
            thanh_tich = st.text_input("Chi tiết (VD: Đẩy ngực 60kg - 4 hiệp x 10 reps)")
            ghi_chu = st.text_area("Cảm nhận buổi tập")
            
            if st.form_submit_button("LƯU KẾT QUẢ", use_container_width=True):
                moi = pd.DataFrame([{'Ngày': str(ngay_tap), 'Môn tập': mon_tap, 'Bài tập/Thành tích': thanh_tich, 'Ghi chú': ghi_chu}])
                df_gym = pd.concat([df_gym, moi], ignore_index=True)
                save_db(df_gym, FILE_GYM)
                st.success("💪 Lên cơ! Đã lưu buổi tập.")
                st.rerun()

    st.markdown("### 📅 Lịch sử tập luyện")
    if df_gym.empty:
        st.info("Chưa có dữ liệu tập luyện. Cầm tạ lên Boss ơi!")
    else:
        # Hiển thị dữ liệu đẹp mắt không dùng bảng mặc định
        for i in reversed(range(len(df_gym))):
            row = df_gym.iloc[i]
            st.markdown(f"""
            <div class="custom-card" style="border-left-color: #FF4B2B;">
                <h4 style='margin:0; color: #FF4B2B;'>🔥 {row['Môn tập']} ({row['Ngày']})</h4>
                <p style='margin:5px 0 0 0; font-size: 18px;'><b>Bài tập:</b> {row['Bài tập/Thành tích']}</p>
                <p style='margin:0; color: #888;'><i>{row['Ghi chú']}</i></p>
            </div>
            """, unsafe_allow_html=True)

# ------------------------------------------
# TRANG 3: HỌC TIẾNG ANH (Giống Duolingo/Quizlet)
# ------------------------------------------
elif menu == "🇬🇧 Trạm Tiếng Anh (Duolingo)":
    st.title("📚 ĐẤU TRƯỜNG TỪ VỰNG")
    
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.markdown("### ➕ Nạp Đạn (Thêm từ mới)")
        with st.form("eng_form", clear_on_submit=True):
            tu_vung = st.text_input("Từ vựng (Tiếng Anh)")
            nghia = st.text_input("Nghĩa (Tiếng Việt)")
            vi_du = st.text_area("Câu ví dụ để nhớ lâu hơn")
            if st.form_submit_button("LƯU VÀO NÃO", use_container_width=True):
                if tu_vung and nghia:
                    moi = pd.DataFrame([{'Từ vựng': tu_vung, 'Nghĩa': nghia, 'Ví dụ': vi_du, 'Ngày học': str(datetime.now().date())}])
                    df_eng = pd.concat([df_eng, moi], ignore_index=True)
                    save_db(df_eng, FILE_ENG)
                    st.success(f"Đã nạp từ '{tu_vung}'!")
                    st.rerun()
                else:
                    st.error("Phải nhập đủ Từ và Nghĩa!")

    with c2:
        st.markdown("### 🃏 Flashcard Kiểm Tra Trí Nhớ")
        if df_eng.empty:
            st.warning("Kho đạn trống. Hãy nhập từ vựng trước!")
        else:
            # Tạo bộ nhớ tạm (Session State) để giữ thẻ Flashcard không bị đổi liên tục
            if 'current_word' not in st.session_state:
                st.session_state.current_word = df_eng.sample(1).iloc[0]
            
            card = st.session_state.current_word
            st.markdown(f"""
            <div style="background-color: #1a1a24; border: 2px solid #00C9FF; border-radius: 15px; padding: 30px; text-align: center;">
                <h2 style="color: #00C9FF; margin:0; font-size: 40px;">{card['Từ vựng']}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            with st.expander("👀 Bấm vào đây để lật thẻ xem đáp án"):
                st.markdown(f"**👉 Nghĩa:** <span style='color:#FF4B2B; font-size:20px;'>{card['Nghĩa']}</span>", unsafe_allow_html=True)
                st.write(f"📝 Ví dụ:")
            
            if st.button("🔀 Đổi từ khác", use_container_width=True):
                st.session_state.current_word = df_eng.sample(1).iloc[0]
                st.rerun()

# ------------------------------------------
# TRANG 4: TỦ ĐỒ THỜI TRANG (Giống Acloset)
# ------------------------------------------
elif menu == "🧢 Tủ Đồ Chất (Acloset)":
    st.title("🧢 STREETWEAR WARDROBE")
    
    with st.expander("➕ CẤT ĐỒ MỚI VÀO TỦ", expanded=False):
        with st.form("fash_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            ten_do = col_a.text_input("Tên món (VD: Áo Hoodie, Quần Cargo)")
            loai = col_b.selectbox("Phân loại", ["Áo", "Quần", "Giày", "Phụ kiện (Mũ, Túi)"])
            brand = col_a.selectbox("Thương hiệu", ["Dirty Coins", "Saigon Swagger", "SWE", "Nike", "Khác"])
            mau = col_b.text_input("Màu sắc chính")
            
            if st.form_submit_button("CẤT VÀO TỦ", use_container_width=True):
                moi = pd.DataFrame([{'Tên đồ': ten_do, 'Loại': loai, 'Thương hiệu': brand, 'Màu sắc': mau}])
                df_fash = pd.concat([df_fash, moi], ignore_index=True)
                save_db(df_fash, FILE_FASH)
                st.success("Đã treo lên móc!")
                st.rerun()

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### 🎲 Phối đồ ngẫu nhiên hôm nay")
        if st.button("Tạo Outfit (Không cần AI)", use_container_width=True):
            aos = df_fash[df_fash['Loại'] == 'Áo']
            quans = df_fash[df_fash['Loại'] == 'Quần']
            if not aos.empty and not quans.empty:
                ao_chon = aos.sample(1).iloc[0]
                quan_chon = quans.sample(1).iloc[0]
                st.success(f"**👕 TOP:** {ao_chon['Tên đồ']} ({ao_chon['Thương hiệu']} - {ao_chon['Màu sắc']})")
                st.warning(f"**👖 BOTTOM:** {quan_chon['Tên đồ']} ({quan_chon['Thương hiệu']} - {quan_chon['Màu sắc']})")
                st.balloons()
            else:
                st.error("Tủ đồ chưa đủ cả Áo và Quần để mix!")
                
    with c2:
        st.markdown("### 🗄️ Thống kê Tủ đồ")
        if not df_fash.empty:
            st.bar_chart(df_fash['Thương hiệu'].value_counts())

    st.markdown("### 🧥 Danh sách đồ trong tủ")
    st.dataframe(df_fash, use_container_width=True, hide_index=True)

# ------------------------------------------
# TRANG 5: PHIM ẢNH (Giống Letterboxd)
# ------------------------------------------
elif menu == "🎬 Nhật Ký Phim (Letterboxd)":
    st.title("🍿 LETTERBOXD CÁ NHÂN")
    
    with st.expander("➕ RATE PHIM VỪA XEM", expanded=False):
        with st.form("mov_form", clear_on_submit=True):
            col_x, col_y = st.columns(2)
            ten_phim = col_x.text_input("Tên bộ phim")
            rap = col_y.selectbox("Xem ở đâu?", ["Galaxy Sala", "CGV", "Lotte", "Netflix", "Web Lậu 🏴‍☠️"])
            diem = st.slider("Chấm điểm (1-10)", 1.0, 10.0, 8.0, step=0.5)
            ngay_xem = st.date_input("Ngày xem")
            
            if st.form_submit_button("LƯU REVIEW", use_container_width=True):
                moi = pd.DataFrame([{'Tên phim': ten_phim, 'Rạp': rap, 'Điểm': diem, 'Ngày xem': str(ngay_xem)}])
                df_mov = pd.concat([df_mov, moi], ignore_index=True)
                save_db(df_mov, FILE_MOV)
                st.success("Đã ghi dấu ấn điện ảnh!")
                st.rerun()

    if not df_mov.empty:
        c1, c2 = st.columns(2)
        c1.metric("Tổng phim đã xem", f"{len(df_mov)} Bộ")
        c2.metric("Điểm trung bình", f"{df_mov['Điểm'].mean():.1f} ⭐️")
        
        st.markdown("### 🎞️ Bộ sưu tập điện ảnh")
        # In phim theo dạng Card (Thẻ) từ mới đến cũ
        cols = st.columns(3)
        for i, row in df_mov.iloc[::-1].iterrows():
            col_idx = i % 3
            with cols[col_idx]:
                st.markdown(f"""
                <div class="custom-card" style="border-left-color: #92FE9D;">
                    <h4 style="margin:0; color:#92FE9D;">{row['Tên phim']}</h4>
                    <p style="margin:5px 0; font-size:14px; color:#aaa;">📍 {row['Rạp']}</p>
                    <p style="margin:0; font-size:18px; color:gold;">{'⭐' * int(row['Điểm'])} ({row['Điểm']})</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Chưa có phim nào được lưu.")
