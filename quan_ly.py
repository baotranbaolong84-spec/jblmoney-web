import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, timedelta

# ==========================================
# 1. UI/UX MAX LEVEL (DARK MODE & CSS)
# ==========================================
st.set_page_config(page_title="Boss Life OS Pro Max", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    div.stButton > button { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); color: white !important; font-weight: 900; border-radius: 10px; border: none; transition: 0.3s; }
    div.stButton > button:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(255,65,108,0.5); }
    .st-emotion-cache-1r6slb0, [data-testid="stForm"] { border-radius: 16px; border: 1px solid #333; background-color: #1a1a24; padding: 20px;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HỆ THỐNG DATABASE (CẤU TRÚC MỚI)
# ==========================================
FILES = {'gym': 'gym_v3.csv', 'eng': 'eng_v3.csv', 'fashion': 'fashion_v3.csv', 'movie': 'movie_v3.csv', 'profile': 'profile_v3.csv'}

def load_db(file_name, columns):
    if os.path.exists(file_name):
        try: 
            df = pd.read_csv(file_name)
            for col in columns:
                if col not in df.columns: df[col] = 0 if 'Số' in col or 'Giá' in col else ''
            return df
        except: pass
    return pd.DataFrame(columns=columns)

def save_db(df, file_name): df.to_csv(file_name, index=False)

df_gym = load_db(FILES['gym'], ['Ngày', 'Cân nặng', 'Môn tập', 'Bài tập', 'Hiệp', 'Reps', 'Khối lượng (kg)', 'Volume', 'Calo Đốt (Kcal)'])
df_eng = load_db(FILES['eng'], ['Ngày', 'Từ vựng', 'Nghĩa', 'Ví dụ', 'Đúng', 'Sai'])
df_fash = load_db(FILES['fashion'], ['Tên đồ', 'Loại', 'Thương hiệu', 'Giá tiền', 'Số lần mặc'])
df_mov = load_db(FILES['movie'], ['Ngày', 'Tên phim', 'Thể loại', 'Rạp', 'Điểm', 'Trạng thái'])
df_pro = load_db(FILES['profile'], ['Tuổi', 'Chiều cao (cm)', 'Giới tính', 'Mức vận động'])

if df_pro.empty:
    df_pro = pd.DataFrame([{'Tuổi': 20, 'Chiều cao (cm)': 170, 'Giới tính': 'Nam', 'Mức vận động': 'Vừa (3-5 ngày/tuần)'}])

# ==========================================
# 3. SIDEBAR: HỒ SƠ SỨC KHỎE & TÍNH CALO/BMI
# ==========================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #00C9FF;'>⚡ LIFE OS CORE</h1>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("ĐIỀU HƯỚNG BẢNG MẠCH:", 
                    ["📊 Tổng Quan & Phân Tích", 
                     "🏋️ Trạm Thể Chất & Calo", 
                     "🇬🇧 Đấu Trường Tiếng Anh", 
                     "🧢 Analytics Tủ Đồ", 
                     "🎬 Bản Đồ Điện Ảnh"])
    st.markdown("---")
    
    st.markdown("### 🧬 Hồ Sơ Sinh Học (BMR/TDEE)")
    with st.form("profile_form"):
        tuoi = st.number_input("Tuổi", 10, 100, int(df_pro.iloc[0]['Tuổi']))
        cao = st.number_input("Chiều cao (cm)", 100, 250, int(df_pro.iloc[0]['Chiều cao (cm)']))
        gioi = st.selectbox("Giới tính", ["Nam", "Nữ"], index=0 if df_pro.iloc[0]['Giới tính']=='Nam' else 1)
        van_dong = st.selectbox("Mức vận động", ["Ít (Không tập)", "Vừa (3-5 ngày/tuần)", "Nhiều (6-7 ngày/tuần)"])
        can_hien_tai = df_gym['Cân nặng'].iloc[-1] if not df_gym.empty else 65.0
        
        if st.form_submit_button("Cập nhật Body", use_container_width=True):
            df_pro = pd.DataFrame([{'Tuổi': tuoi, 'Chiều cao (cm)': cao, 'Giới tính': gioi, 'Mức vận động': van_dong}])
            save_db(df_pro, FILES['profile'])
            st.rerun()

    # TÍNH TOÁN BMI & BÉO PHÌ
    bmi = can_hien_tai / ((cao/100)**2)
    st.markdown(f"**Cân nặng hiện tại:** {can_hien_tai} kg")
    st.markdown(f"**Chỉ số BMI:** {bmi:.1f}")
    if bmi < 18.5: st.warning("⚠️ Thiếu cân (Cần ăn thêm calories!)")
    elif 18.5 <= bmi <= 24.9: st.success("✅ Chuẩn Body Fitness!")
    elif 25 <= bmi <= 29.9: st.warning("⚠️ Tiền béo phì (Cần cắt giảm mỡ)")
    else: st.error("🚨 Béo phì (Phải Cardio & Caloric Deficit ngay!)")

    # TÍNH TOÁN CALO (BMR & TDEE theo Mifflin-St Jeor)
    if gioi == "Nam": bmr = (10 * can_hien_tai) + (6.25 * cao) - (5 * tuoi) + 5
    else: bmr = (10 * can_hien_tai) + (6.25 * cao) - (5 * tuoi) - 161
    
    he_so = 1.2 if van_dong == "Ít (Không tập)" else (1.55 if van_dong == "Vừa (3-5 ngày/tuần)" else 1.725)
    tdee = bmr * he_so
    
    st.info(f"🔥 **Calo sinh tồn (BMR):** {bmr:.0f} Kcal/ngày")
    st.error(f"⚡ **Calo giữ cân (TDEE):** {tdee:.0f} Kcal/ngày")
    st.caption("Muốn giảm cân: Ăn ít hơn TDEE khoảng 300-500 Kcal. Tăng cơ: Ăn nhiều hơn 300 Kcal.")

# ==========================================
# 4. TRIỂN KHAI CÁC TRANG CÓ BIỂU ĐỒ 100%
# ==========================================

# ------------------------------------------
# TRANG 1: DASHBOARD
# ------------------------------------------
if menu == "📊 Tổng Quan & Phân Tích":
    st.title("📊 TRUNG TÂM PHÂN TÍCH")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⚖️ Biến động cân nặng", f"{df_gym['Cân nặng'].iloc[-1]} kg" if not df_gym.empty else "N/A")
    c2.metric("📚 Từ vựng đã nạp", f"{len(df_eng)} từ")
    c3.metric("💸 Đốt vào quần áo", f"{df_fash['Giá tiền'].sum():,.0f} đ" if not df_fash.empty else "0 đ")
    c4.metric("🎬 Số vé Galaxy/CGV", f"{len(df_mov)}")
    st.markdown("---")
    st.markdown("### 📈 Biểu đồ toàn cảnh hệ thống")
    st.info("Hệ thống sẽ tự động vẽ biểu đồ khi Boss bắt đầu nạp dữ liệu ở các tab bên dưới!")

# ------------------------------------------
# TRANG 2: GYM & CALORIES & GIÁO ÁN
# ------------------------------------------
elif menu == "🏋️ Trạm Thể Chất & Calo":
    st.title("🏋️ GYM & CALORIES TRACKER")
    
    t_nhap, t_giao_an = st.tabs(["📝 Nhập Lịch Tập & Biểu Đồ", "💡 Giáo Án Luyện Tập"])
    
    with t_nhap:
        with st.expander("➕ GHI NHẬN BUỔI TẬP", expanded=False):
            with st.form("gym_form"):
                col1, col2, col3 = st.columns(3)
                ngay_tap = col1.date_input("Ngày")
                can_nang = col2.number_input("Cân nặng hôm nay (kg)", 30.0, 150.0, float(df_gym['Cân nặng'].iloc[-1]) if not df_gym.empty else 65.0)
                mon_tap = col3.selectbox("Hoạt động", ["Gym (Tạ)", "Bơi lội", "Nhặt bóng / Tennis", "Chạy bộ"])
                
                c1, c2, c3 = st.columns(3)
                bai_tap = c1.text_input("Tên bài / Chi tiết (VD: Đẩy ngực, Bơi ếch)")
                hiep = c2.number_input("Số hiệp (Sets) / Thời gian (Phút)", 1, 300, 4)
                reps = c3.number_input("Số lần (Reps) / Vòng bơi", 1, 500, 10)
                
                c4, c5 = st.columns(2)
                khoi_luong = c4.number_input("Khối lượng tạ (kg) - Bỏ qua nếu bơi/tennis", 0.0, 500.0, 0.0)
                calo_dot = c5.number_input("Ước tính Calo đốt (Kcal) - Xem đồng hồ", 0, 3000, 300)
                
                if st.form_submit_button("LƯU BUỔI TẬP", use_container_width=True):
                    vol = hiep * reps * khoi_luong if mon_tap == "Gym (Tạ)" else 0
                    moi = pd.DataFrame([{'Ngày': str(ngay_tap), 'Cân nặng': can_nang, 'Môn tập': mon_tap, 'Bài tập': bai_tap, 
                                         'Hiệp': hiep, 'Reps': reps, 'Khối lượng (kg)': khoi_luong, 'Volume': vol, 'Calo Đốt (Kcal)': calo_dot}])
                    df_gym = pd.concat([df_gym, moi], ignore_index=True)
                    save_db(df_gym, FILES['gym'])
                    st.success("Lên cơ! Đã lưu thành công.")
                    st.rerun()

        st.markdown("### 📈 Biểu đồ Biến Động Cân Nặng")
        if not df_gym.empty:
            chart_weight = df_gym.groupby('Ngày')['Cân nặng'].last().reset_index()
            st.line_chart(chart_weight.set_index('Ngày'), color="#FF4B2B")
        
        st.markdown("### 📊 Biểu đồ Calo đã đốt")
        if not df_gym.empty:
            chart_calo = df_gym.groupby('Ngày')['Calo Đốt (Kcal)'].sum().reset_index()
            st.bar_chart(chart_calo.set_index('Ngày'), color="#00C9FF")
            
        st.dataframe(df_gym, use_container_width=True)

    with t_giao_an:
        st.markdown("### 💡 GỢI Ý BÀI TẬP ĐỐT CALO / TĂNG CƠ TỐI ĐA")
        c1, c2, c3 = st.columns(3)
        c1.success("**🏋️ Giáo án Gym (Ngực - Tay sau)**\n\n1. Bench Press: 4 hiệp x 8-10 reps\n2. Incline Dumbbell Press: 3 hiệp x 10 reps\n3. Ép ngực cáp: 3 hiệp x 12 reps\n4. Đẩy tay sau (Tricep Pushdown): 4 hiệp x 12 reps\n\n*🔥 Đốt khoảng: 300 - 400 Kcal*")
        c2.info("**🏊‍♂️ Giáo án Bơi Lội (Cardio toàn thân)**\n\n1. Khởi động trên cạn: 10 phút\n2. Bơi ếch nhẹ nhàng: 5 vòng (Làm nóng)\n3. Bơi sải tốc độ cao: 10 vòng (Nghỉ 30s giữa mỗi vòng)\n4. Bơi thả lỏng: 2 vòng\n\n*🔥 Đốt khoảng: 500 - 600 Kcal/giờ*")
        c3.warning("**🎾 Chạy Nhặt Bóng / Tennis**\n\n1. Chạy bứt tốc nhặt bóng dọc sân: Đốt mỡ cực rát như tập HIIT.\n2. Luyện phản xạ di chuyển ngang.\n3. Duy trì nhịp tim ở vùng Zone 2-3 (120 - 150 nhịp/phút) trong suốt 1 tiếng.\n\n*🔥 Đốt khoảng: 400 - 700 Kcal/giờ*")

# ------------------------------------------
# TRANG 3: ENGLISH & BIỂU ĐỒ HỌC TẬP
# ------------------------------------------
elif menu == "🇬🇧 Đấu Trường Tiếng Anh":
    st.title("📚 TRẠM TỪ VỰNG CHUYÊN SÂU")
    
    with st.expander("➕ NẠP TỪ MỚI", expanded=False):
        with st.form("eng_form"):
            tu = st.text_input("Từ vựng")
            nghia = st.text_input("Nghĩa")
            vidu = st.text_area("Câu ví dụ")
            if st.form_submit_button("NẠP ĐẠN", use_container_width=True):
                moi = pd.DataFrame([{'Ngày': str(datetime.now().date()), 'Từ vựng': tu, 'Nghĩa': nghia, 'Ví dụ': vidu, 'Đúng': 0, 'Sai': 0}])
                df_eng = pd.concat([df_eng, moi], ignore_index=True)
                save_db(df_eng, FILES['eng'])
                st.success("Đã nạp!")
                st.rerun()

    st.markdown("### 📈 Biểu đồ tiến độ nạp từ vựng")
    if not df_eng.empty:
        chart_eng = df_eng.groupby('Ngày').size().reset_index(name='Số từ mới')
        st.line_chart(chart_eng.set_index('Ngày'), color="#92FE9D")
        
    st.markdown("### 🧠 Flashcard Trắc Nghiệm")
    if not df_eng.empty:
        idx = df_eng.sample(1).index[0]
        card = df_eng.loc[idx]
        st.markdown(f"<h1 style='text-align:center; color:#00C9FF;'>{card['Từ vựng']}</h1>", unsafe_allow_html=True)
        with st.expander("👉 Bấm để lật thẻ"):
            st.markdown(f"Nghĩa:")
            st.write(f"Ví dụ:")
            st.write(f"*(Thống kê từ này: Bạn đã trả lời đúng {card['Đúng']} lần, sai {card['Sai']} lần)*")
    else: st.info("Thêm từ vựng để mở khóa thẻ bài!")
    
    st.dataframe(df_eng, use_container_width=True, hide_index=True)

# ------------------------------------------
# TRANG 4: TỦ ĐỒ CÔNG NGHỆ CAO
# ------------------------------------------
elif menu == "🧢 Analytics Tủ Đồ":
    st.title("🧢 STREETWEAR ANALYTICS")
    
    with st.expander("➕ THÊM QUẦN ÁO MỚI", expanded=False):
        with st.form("fash_form"):
            c1, c2 = st.columns(2)
            ten = c1.text_input("Tên sản phẩm")
            brand = c2.selectbox("Thương hiệu", ["Dirty Coins", "Saigon Swagger", "Nike", "Adidas", "Hades", "Khác"])
            loai = c1.selectbox("Phân loại", ["Áo", "Quần", "Giày", "Phụ kiện"])
            gia = c2.number_input("Giá mua (VNĐ)", 0, 50000000, 350000, step=50000)
            if st.form_submit_button("CẤT VÀO TỦ", use_container_width=True):
                moi = pd.DataFrame([{'Tên đồ': ten, 'Loại': loai, 'Thương hiệu': brand, 'Giá tiền': gia, 'Số lần mặc': 0}])
                df_fash = pd.concat([df_fash, moi], ignore_index=True)
                save_db(df_fash, FILES['fashion'])
                st.success("Tủ đồ +1!")
                st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📊 Tiền cúng cho Local Brand")
        if not df_fash.empty:
            chart_brand = df_fash.groupby('Thương hiệu')['Giá tiền'].sum().reset_index()
            st.bar_chart(chart_brand.set_index('Thương hiệu'), color="#FF416C")
            
    with c2:
        st.markdown("### 📈 Tỷ lệ phân bổ tủ đồ")
        if not df_fash.empty:
            chart_loai = df_fash.groupby('Loại').size().reset_index(name='Số lượng')
            st.bar_chart(chart_loai.set_index('Loại'), color="#FFD700")

    st.markdown("### 🧥 Kho đồ (Tính năng Cost Per Wear)")
    if not df_fash.empty:
        df_fash['Chi phí/Lần mặc'] = (df_fash['Giá tiền'] / df_fash['Số lần mặc'].replace(0, 1)).astype(int)
        st.dataframe(df_fash, use_container_width=True, hide_index=True)

# ------------------------------------------
# TRANG 5: ĐIỆN ẢNH (GALAXY SALA)
# ------------------------------------------
elif menu == "🎬 Bản Đồ Điện Ảnh":
    st.title("🍿 PHÂN TÍCH RẠP CHIẾU PHIM")
    
    with st.expander("➕ RATE PHIM MỚI / WATCHLIST", expanded=False):
        with st.form("mov_form"):
            c1, c2 = st.columns(2)
            ten = c1.text_input("Tên bộ phim")
            the_loai = c2.selectbox("Thể loại", ["Hành động", "Kinh dị", "Tâm lý/Tình cảm", "Viễn tưởng", "Hoạt hình"])
            rap = c1.selectbox("Rạp / Nền tảng", ["Galaxy Sala", "CGV", "Netflix", "Web lậu"])
            trang_thai = c2.radio("Trạng thái", ["Đã xem", "Muốn xem (Watchlist)"], horizontal=True)
            diem = st.slider("Chấm điểm", 1.0, 10.0, 8.0)
            if st.form_submit_button("LƯU CUỐN PHIM NÀY", use_container_width=True):
                moi = pd.DataFrame([{'Ngày': str(datetime.now().date()), 'Tên phim': ten, 'Thể loại': the_loai, 'Rạp': rap, 'Điểm': diem if trang_thai=='Đã xem' else 0, 'Trạng thái': trang_thai}])
                df_mov = pd.concat([df_mov, moi], ignore_index=True)
                save_db(df_mov, FILES['movie'])
                st.success("Đã nạp phim!")
                st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📊 Thống kê Thể loại yêu thích")
        if not df_mov.empty:
            chart_tl = df_mov[df_mov['Trạng thái']=='Đã xem'].groupby('Thể loại').size().reset_index(name='Số bộ')
            st.bar_chart(chart_tl.set_index('Thể loại'), color="#00C9FF")
            
    with c2:
        st.markdown("### 📊 Tần suất đi rạp (Galaxy vs CGV...)")
        if not df_mov.empty:
            chart_rap = df_mov.groupby('Rạp').size().reset_index(name='Số lần')
            st.bar_chart(chart_rap.set_index('Rạp'), color="#92FE9D")

    st.dataframe(df_mov, use_container_width=True, hide_index=True)
