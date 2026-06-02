import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, timedelta

# ==========================================
# 1. UI/UX LUXURY GOLD EDITION (MẠ VÀNG TOÀN BỘ)
# ==========================================
st.set_page_config(page_title="Boss VIP OS Ultimate", page_icon="👑", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    
    /* Nền đen sâu thẳm, chữ xám sáng */
    .stApp { background-color: #0a0a0a; color: #e0e0e0; }
    
    /* Nút bấm dốc màu Vàng Gold 3D siêu thực */
    div.stButton > button {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        color: #000000 !important; font-weight: 900; border-radius: 8px;
        border: none; padding: 12px 24px; transition: all 0.4s ease;
        text-transform: uppercase; letter-spacing: 1px;
    }
    div.stButton > button:hover {
        transform: scale(1.05); box-shadow: 0 0 20px rgba(212, 175, 55, 0.6);
    }
    
    /* Thẻ Form và Card mạ viền vàng */
    .st-emotion-cache-1r6slb0, [data-testid="stForm"] { 
        border-radius: 12px; border: 1px solid #D4AF37; 
        background-color: #111111; box-shadow: 0 8px 32px rgba(212, 175, 55, 0.15); 
    }
    
    /* Tiêu đề màu Vàng Cổ Điển */
    h1, h2, h3, h4 { color: #D4AF37 !important; font-family: 'Georgia', serif; text-transform: uppercase; letter-spacing: 1.5px;}
    
    /* Số Metric phát sáng vàng */
    [data-testid="stMetricValue"] { color: #FCF6BA !important; font-weight: 800; text-shadow: 0 0 10px rgba(252,246,186,0.4); }
    
    /* Thanh Tab màu Vàng sang trọng */
    .stTabs [data-baseweb="tab-list"] { gap: 5px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1a1a1a; border: 1px solid #D4AF37; border-bottom: none; 
        border-radius: 8px 8px 0 0; color: #D4AF37; 
    }
    .stTabs [aria-selected="true"] { 
        background: linear-gradient(to right, #BF953F, #FCF6BA); 
        color: #000 !important; font-weight: bold; 
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HỆ THỐNG DATABASE UNLIMITED
# ==========================================
FILES = {'gym': 'gym_ultimate.csv', 'eng': 'eng_ultimate.csv', 'fashion': 'fashion_ultimate.csv', 'movie': 'movie_ultimate.csv', 'profile': 'profile_ultimate.csv'}

def load_db(file_name, columns):
    if os.path.exists(file_name):
        try: 
            df = pd.read_csv(file_name)
            for col in columns:
                if col not in df.columns: df[col] = 0 if ('Số' in col or 'Giá' in col or 'Đúng' in col or 'Sai' in col) else ''
            return df
        except: pass
    return pd.DataFrame(columns=columns)

def save_db(df, file_name): df.to_csv(file_name, index=False)

# Tải full cột không cắt xén
df_gym = load_db(FILES['gym'], ['Ngày', 'Cân nặng', 'Môn tập', 'Bài tập', 'Hiệp', 'Reps', 'Khối lượng (kg)', 'Volume', 'Calo Đốt (Kcal)'])
df_eng = load_db(FILES['eng'], ['Từ vựng', 'Nghĩa', 'Ví dụ', 'Đúng', 'Sai', 'Ngày học cuối'])
df_fash = load_db(FILES['fashion'], ['Tên đồ', 'Loại', 'Thương hiệu', 'Màu sắc', 'Giá tiền', 'Số lần mặc'])
df_mov = load_db(FILES['movie'], ['Tên phim', 'Thể loại', 'Rạp', 'Điểm', 'Trạng thái', 'Ngày'])
df_pro = load_db(FILES['profile'], ['Tuổi', 'Chiều cao (cm)', 'Giới tính', 'Mức vận động'])

if df_pro.empty:
    df_pro = pd.DataFrame([{'Tuổi': 20, 'Chiều cao (cm)': 170, 'Giới tính': 'Nam', 'Mức vận động': 'Vừa (3-5 ngày/tuần)'}])

# ==========================================
# 3. ĐIỀU HƯỚNG VÀ BẢNG ĐIỀU KHIỂN SINH HỌC
# ==========================================
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1614164185128-e4ec99c436d7?auto=format&fit=crop&q=80&w=400", caption="👑 VIP Lounge")
    st.markdown("<h2 style='text-align: center;'>👑 VIP OS</h2>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("ĐIỀU HƯỚNG:", 
                    ["💎 Executive Dashboard", 
                     "🏋️ Premium Fitness", 
                     "🇬🇧 Elite Vocabulary", 
                     "🧢 Luxury Wardrobe", 
                     "🎬 VIP Cinema"])
    st.markdown("---")
    
    # Tính Streak Tiếng Anh
    streak = 0
    if not df_eng.empty:
        dates = pd.to_datetime(df_eng['Ngày học cuối']).dt.date.sort_values().unique()
        today = datetime.now().date()
        for i in range(len(dates)):
            if today - timedelta(days=i) in dates: streak += 1
            else: break
            
    st.metric("🔥 English Streak", f"{streak} Ngày", "Unstoppable!")
    
    st.markdown("### 🧬 Hồ Sơ Sinh Học (BMR/TDEE)")
    with st.form("profile_form"):
        tuoi = st.number_input("Tuổi", 10, 100, int(df_pro.iloc[0]['Tuổi']))
        cao = st.number_input("Chiều cao (cm)", 100, 250, int(df_pro.iloc[0]['Chiều cao (cm)']))
        gioi = st.selectbox("Giới tính", ["Nam", "Nữ"], index=0 if df_pro.iloc[0]['Giới tính']=='Nam' else 1)
        van_dong = st.selectbox("Mức vận động", ["Ít (Không tập)", "Vừa (3-5 ngày/tuần)", "Nhiều (6-7 ngày/tuần)"])
        can_hien_tai = df_gym['Cân nặng'].iloc[-1] if not df_gym.empty else 65.0
        
        if st.form_submit_button("CẬP NHẬT BODY", use_container_width=True):
            df_pro = pd.DataFrame([{'Tuổi': tuoi, 'Chiều cao (cm)': cao, 'Giới tính': gioi, 'Mức vận động': van_dong}])
            save_db(df_pro, FILES['profile'])
            st.rerun()

    # Tính toán chuẩn y khoa BMI & Béo Phì
    bmi = can_hien_tai / ((cao/100)**2)
    st.markdown(f"**Cân nặng hiện tại:** {can_hien_tai} kg")
    st.markdown(f"**Chỉ số BMI:** {bmi:.1f}")
    if bmi < 18.5: st.warning("⚠️ Thiếu cân (Cần ăn thêm calories!)")
    elif 18.5 <= bmi <= 24.9: st.success("✅ Chuẩn Body Fitness!")
    elif 25 <= bmi <= 29.9: st.warning("⚠️ Tiền béo phì (Cần cắt giảm mỡ)")
    else: st.error("🚨 Béo phì (Phải Cardio & Caloric Deficit ngay!)")

    # Tính Calo
    if gioi == "Nam": bmr = (10 * can_hien_tai) + (6.25 * cao) - (5 * tuoi) + 5
    else: bmr = (10 * can_hien_tai) + (6.25 * cao) - (5 * tuoi) - 161
    he_so = 1.2 if van_dong == "Ít (Không tập)" else (1.55 if van_dong == "Vừa (3-5 ngày/tuần)" else 1.725)
    tdee = bmr * he_so
    
    st.info(f"🔥 **Calo sinh tồn (BMR):** {bmr:.0f} Kcal/ngày")
    st.error(f"⚡ **Calo giữ cân (TDEE):** {tdee:.0f} Kcal/ngày")

# ==========================================
# 4. TRIỂN KHAI GIAO DIỆN CHỨC NĂNG FULL UNLIMITED
# ==========================================

# ------------------------------------------
# TRANG 1: DASHBOARD
# ------------------------------------------
if menu == "💎 Executive Dashboard":
    st.title("💎 TỔNG QUAN ĐẾ CHẾ")
    st.image("https://images.unsplash.com/photo-1549465220-1a8b9238cd48?auto=format&fit=crop&q=80&w=1600", use_container_width=True)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⚖️ Biến động Cân nặng", f"{df_gym['Cân nặng'].iloc[-1]} kg" if not df_gym.empty else "N/A")
    c2.metric("📚 Từ vựng tinh hoa", f"{len(df_eng)}")
    c3.metric("💸 Tổng giá trị Tủ đồ", f"{df_fash['Giá tiền'].sum():,.0f} đ" if not df_fash.empty else "0 đ")
    c4.metric("🎬 Phim đã xem", f"{len(df_mov[df_mov['Trạng thái'] == 'Đã xem'])}")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💪 Phân bổ hoạt động thể chất")
        if not df_gym.empty: st.bar_chart(df_gym['Môn tập'].value_counts(), color="#D4AF37")
    with col2:
        st.subheader("🎬 Thể loại phim yêu thích")
        if not df_mov.empty: st.bar_chart(df_mov['Thể loại'].value_counts(), color="#FCF6BA")

# ------------------------------------------
# TRANG 2: GYM & CAMERA & GIÁO ÁN (FULL)
# ------------------------------------------
elif menu == "🏋️ Premium Fitness":
    st.title("🏋️ ELITE FITNESS TRACKER")
    st.image("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&q=80&w=1600", use_container_width=True)
    
    t_nhap, t_giao_an = st.tabs(["📝 Lịch Tập & Biểu Đồ & Selfie", "💡 Giáo Án Luyện Tập Tối Ưu"])
    
    with t_nhap:
        with st.expander("➕ GHI NHẬN BUỔI TẬP & SELFIE", expanded=False):
            with st.form("gym_form"):
                col1, col2, col3 = st.columns(3)
                ngay_tap = col1.date_input("Ngày")
                can_nang = col2.number_input("Cân nặng hôm nay (kg)", 30.0, 150.0, float(df_gym['Cân nặng'].iloc[-1]) if not df_gym.empty else 65.0)
                mon_tap = col3.selectbox("Hoạt động", ["Gym (Tạ)", "Bơi lội", "Nhặt bóng / Tennis", "Chạy bộ", "Khác"])
                
                c1, c2, c3 = st.columns(3)
                bai_tap = c1.text_input("Tên bài (VD: Bench Press, Bơi ếch)")
                hiep = c2.number_input("Số hiệp / Phút", 1, 300, 4)
                reps = c3.number_input("Số lần (Reps) / Vòng", 1, 500, 10)
                
                c4, c5 = st.columns(2)
                khoi_luong = c4.number_input("Khối lượng tạ (kg) - Bỏ qua nếu bơi", 0.0, 500.0, 0.0)
                calo_dot = c5.number_input("Calo đốt (Kcal)", 0, 3000, 300)
                
                st.markdown("### 📸 Selfie Body Check (Mở camera)")
                anh_body = st.camera_input("Chụp body sau tập")
                
                if st.form_submit_button("LƯU THÀNH TÍCH", use_container_width=True):
                    vol = hiep * reps * khoi_luong if mon_tap == "Gym (Tạ)" else 0
                    moi = pd.DataFrame([{'Ngày': str(ngay_tap), 'Cân nặng': can_nang, 'Môn tập': mon_tap, 'Bài tập': bai_tap, 
                                         'Hiệp': hiep, 'Reps': reps, 'Khối lượng (kg)': khoi_luong, 'Volume': vol, 'Calo Đốt (Kcal)': calo_dot}])
                    df_gym = pd.concat([df_gym, moi], ignore_index=True)
                    save_db(df_gym, FILES['gym'])
                    st.success("Tuyệt vời Boss! Đã lưu.")
                    st.rerun()

        st.markdown("### 📈 Phân Tích Volume Tập Tạ (Sức Mạnh)")
        if not df_gym.empty and df_gym['Volume'].sum() > 0:
            chart_vol = df_gym.groupby('Ngày')['Volume'].sum().reset_index()
            st.area_chart(chart_vol.set_index('Ngày'), color="#D4AF37")
            
        st.markdown("### 🔥 Biểu đồ Calo Đốt")
        if not df_gym.empty:
            chart_calo = df_gym.groupby('Ngày')['Calo Đốt (Kcal)'].sum().reset_index()
            st.bar_chart(chart_calo.set_index('Ngày'), color="#BF953F")
            st.dataframe(df_gym.sort_values(by="Ngày", ascending=False), use_container_width=True)

    with t_giao_an:
        st.markdown("### 💡 GỢI Ý BÀI TẬP ĐỐT CALO / TĂNG CƠ TỐI ĐA")
        c1, c2, c3 = st.columns(3)
        c1.success("**🏋️ Giáo án Gym (Ngực - Tay sau)**\n\n1. Bench Press: 4 hiệp x 8-10 reps\n2. Incline Dumbbell Press: 3 hiệp x 10 reps\n3. Ép ngực cáp: 3 hiệp x 12 reps\n4. Đẩy tay sau (Tricep Pushdown): 4 hiệp x 12 reps\n\n*🔥 Đốt khoảng: 300 - 400 Kcal*")
        c2.info("**🏊‍♂️ Giáo án Bơi Lội (Cardio toàn thân)**\n\n1. Khởi động trên cạn: 10 phút\n2. Bơi ếch nhẹ nhàng: 5 vòng (Làm nóng)\n3. Bơi sải tốc độ cao: 10 vòng (Nghỉ 30s giữa mỗi vòng)\n4. Bơi thả lỏng: 2 vòng\n\n*🔥 Đốt khoảng: 500 - 600 Kcal/giờ*")
        c3.warning("**🎾 Chạy Nhặt Bóng / Tennis**\n\n1. Chạy bứt tốc nhặt bóng dọc sân: Đốt mỡ cực rát như HIIT.\n2. Luyện phản xạ di chuyển ngang.\n3. Duy trì nhịp tim ở vùng Zone 2-3 (120 - 150 nhịp/phút) suốt 1 tiếng.\n\n*🔥 Đốt khoảng: 400 - 700 Kcal/giờ*")

# ------------------------------------------
# TRANG 3: ENGLISH & THUẬT TOÁN TEST TỪ VỰNG
# ------------------------------------------
elif menu == "🇬🇧 Elite Vocabulary":
    st.title("📚 ROYAL VOCABULARY")
    st.image("https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&q=80&w=1600", use_container_width=True)
    
    with st.expander("➕ NẠP TỪ MỚI", expanded=False):
        with st.form("eng_form"):
            tu = st.text_input("Từ vựng")
            nghia = st.text_input("Nghĩa")
            vidu = st.text_area("Câu ví dụ")
            if st.form_submit_button("NẠP VÀO KHO TÀNG", use_container_width=True):
                moi = pd.DataFrame([{'Từ vựng': tu, 'Nghĩa': nghia, 'Ví dụ': vidu, 'Đúng': 0, 'Sai': 0, 'Ngày học cuối': str(datetime.now().date())}])
                df_eng = pd.concat([df_eng, moi], ignore_index=True)
                save_db(df_eng, FILES['eng'])
                st.success("Đã nạp!")
                st.rerun()

    st.markdown("### 🧠 Bài Test Trí Nhớ (Thuật Toán Thông Minh)")
    if df_eng.empty: st.info("Hãy thêm từ vựng để bắt đầu Test!")
    else:
        # Ưu tiên lấy từ hay làm sai
        if 'quiz_word' not in st.session_state:
            weights = df_eng['Sai'] + 1 
            st.session_state.quiz_idx = df_eng.sample(1, weights=weights).index[0]
        
        idx = st.session_state.quiz_idx
        card = df_eng.loc[idx]
        
        st.markdown(f"<h1 style='text-align:center; font-size:60px; text-shadow: 0 0 15px #D4AF37;'>{card['Từ vựng']}</h1>", unsafe_allow_html=True)
        
        if 'show_ans' not in st.session_state: st.session_state.show_ans = False
        
        if not st.session_state.show_ans:
            if st.button("Lật Thẻ Trả Lời", use_container_width=True):
                st.session_state.show_ans = True
                st.rerun()
        else:
            st.markdown(f"<h3 style='text-align:center; color:#D4AF37;'>👉 Nghĩa: {card['Nghĩa']}</h3>", unsafe_allow_html=True)
            st.write(f"📝 *Ví dụ: {card['Ví dụ']}*")
            
            c1, c2 = st.columns(2)
            if c1.button("✅ Mình Nhớ Từ Này", use_container_width=True):
                df_eng.at[idx, 'Đúng'] += 1
                df_eng.at[idx, 'Ngày học cuối'] = str(datetime.now().date())
                save_db(df_eng, FILES['eng'])
                st.session_state.show_ans = False
                del st.session_state.quiz_idx
                st.rerun()
                
            if c2.button("❌ Quên Mất Rồi", use_container_width=True):
                df_eng.at[idx, 'Sai'] += 1
                df_eng.at[idx, 'Ngày học cuối'] = str(datetime.now().date())
                save_db(df_eng, FILES['eng'])
                st.session_state.show_ans = False
                del st.session_state.quiz_idx
                st.rerun()
                
    st.markdown("### 📈 Biểu đồ nạp từ vựng")
    if not df_eng.empty:
        chart_eng = df_eng.groupby('Ngày học cuối').size().reset_index(name='Số từ')
        st.line_chart(chart_eng.set_index('Ngày học cuối'), color="#FCF6BA")
    st.dataframe(df_eng, use_container_width=True, hide_index=True)

# ------------------------------------------
# TRANG 4: TỦ ĐỒ CAMERA & MIX ĐỒ TỰ ĐỘNG (FULL)
# ------------------------------------------
elif menu == "🧢 Luxury Wardrobe":
    st.title("🧢 STREETWEAR COLLECTION")
    st.image("https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&q=80&w=1600", use_container_width=True)
    
    with st.expander("➕ MUA ĐỒ MỚI & CHỤP ẢNH", expanded=False):
        with st.form("fash_form"):
            c1, c2 = st.columns(2)
            ten = c1.text_input("Tên sản phẩm")
            brand = c2.selectbox("Thương hiệu", ["Dirty Coins", "Saigon Swagger", "SWE", "Nike", "Dior", "Gucci", "Khác"])
            loai = c1.selectbox("Phân loại", ["Áo", "Quần", "Giày", "Phụ kiện"])
            mau = c2.text_input("Màu sắc")
            gia = st.number_input("Giá mua (VNĐ)", 0, 100000000, 500000, step=50000)
            
            st.markdown("### 📸 Chụp ảnh món đồ mới")
            anh_do = st.camera_input("Đưa đồ vào khung hình")
            
            if st.form_submit_button("THÊM VÀO BỘ SƯU TẬP", use_container_width=True):
                moi = pd.DataFrame([{'Tên đồ': ten, 'Loại': loai, 'Thương hiệu': brand, 'Màu sắc': mau, 'Giá tiền': gia, 'Số lần mặc': 0}])
                df_fash = pd.concat([df_fash, moi], ignore_index=True)
                save_db(df_fash, FILES['fashion'])
                st.success("Tủ đồ sang trọng +1!")
                st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🎲 AI Mix Đồ Tự Động")
        if st.button("Mix Ngẫu Nhiên Outfit", use_container_width=True):
            aos = df_fash[df_fash['Loại'] == 'Áo']
            quans = df_fash[df_fash['Loại'] == 'Quần']
            if not aos.empty and not quans.empty:
                ao_chon = aos.sample(1).iloc[0]
                quan_chon = quans.sample(1).iloc[0]
                st.success(f"**👕 TOP:** {ao_chon['Tên đồ']} ({ao_chon['Thương hiệu']}) - Màu {ao_chon['Màu sắc']}")
                st.warning(f"**👖 BOTTOM:** {quan_chon['Tên đồ']} ({quan_chon['Thương hiệu']}) - Màu {quan_chon['Màu sắc']}")
                st.balloons()
            else:
                st.error("Tủ đồ chưa đủ Áo và Quần để Mix!")
    with c2:
        st.markdown("### 📊 Tổng vốn & Nhận diện Hàng Hiệu")
        if not df_fash.empty:
            chart_brand = df_fash.groupby('Thương hiệu')['Giá tiền'].sum().reset_index()
            st.bar_chart(chart_brand.set_index('Thương hiệu'), color="#D4AF37")
            
    st.markdown("### 🧥 Tính độ khấu hao (Cost Per Wear)")
    if not df_fash.empty:
        df_fash['Chi phí/Lần mặc'] = (df_fash['Giá tiền'] / df_fash['Số lần mặc'].replace(0, 1)).astype(int)
        st.dataframe(df_fash, use_container_width=True, hide_index=True)

# ------------------------------------------
# TRANG 5: ĐIỆN ẢNH FULL BẢN WATCHLIST
# ------------------------------------------
elif menu == "🎬 VIP Cinema":
    st.title("🍿 VIP CINEMA LOUNGE")
    st.image("https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?auto=format&fit=crop&q=80&w=1600", use_container_width=True)
    
    with st.expander("➕ LƯU NHẬT KÝ HOẶC WATCHLIST", expanded=False):
        with st.form("mov_form"):
            c1, c2 = st.columns(2)
            ten = c1.text_input("Tên bộ phim")
            the_loai = c2.selectbox("Thể loại", ["Hành động", "Tâm lý/Tình cảm", "Kinh dị", "Viễn tưởng", "Hoạt hình"])
            rap = c1.selectbox("Rạp / Nền tảng", ["Galaxy Sala", "CGV Gold Class", "Netflix Premium", "Khác"])
            trang_thai = c2.radio("Trạng thái", ["Đã xem", "Muốn xem (Watchlist)"], horizontal=True)
            diem = st.slider("Chấm điểm VVIP", 1.0, 10.0, 9.0)
            ngay = st.date_input("Ngày xem/Dự kiến")
            
            if st.form_submit_button("LƯU KÝ ỨC", use_container_width=True):
                moi = pd.DataFrame([{'Ngày': str(ngay), 'Tên phim': ten, 'Thể loại': the_loai, 'Rạp': rap, 'Điểm': diem if trang_thai=='Đã xem' else 0, 'Trạng thái': trang_thai}])
                df_mov = pd.concat([df_mov, moi], ignore_index=True)
                save_db(df_mov, FILES['movie'])
                st.success("Tuyệt đỉnh!")
                st.rerun()

    t_watched, t_watchlist = st.tabs(["✅ PHIM ĐÃ XEM", "📌 WATCHLIST (Đợi rạp)"])
    
    with t_watched:
        da_xem = df_mov[df_mov['Trạng thái'] == 'Đã xem']
        if not da_xem.empty:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### Tần suất các Rạp")
                chart_rap = da_xem.groupby('Rạp').size().reset_index(name='Số vé')
                st.bar_chart(chart_rap.set_index('Rạp'), color="#FCF6BA")
            with c2:
                st.markdown("### Thể loại ưa thích")
                chart_tl = da_xem.groupby('Thể loại').size().reset_index(name='Số bộ')
                st.bar_chart(chart_tl.set_index('Thể loại'), color="#D4AF37")
            st.dataframe(da_xem, use_container_width=True, hide_index=True)
        else: st.info("Chưa có phim nào được xem.")
            
    with t_watchlist:
        chua_xem = df_mov[df_mov['Trạng thái'] == 'Muốn xem (Watchlist)']
        st.dataframe(chua_xem[['Ngày', 'Tên phim', 'Thể loại', 'Rạp']], use_container_width=True, hide_index=True)
