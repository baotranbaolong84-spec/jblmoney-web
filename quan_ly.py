import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, timedelta

# ==========================================
# 1. UI/UX LUXURY GOLD EDITION
# ==========================================
st.set_page_config(page_title="Boss VIP OS Ultimate", page_icon="👑", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp { background-color: #0a0a0a; color: #e0e0e0; }
    div.stButton > button {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        color: #000000 !important; font-weight: 900; border-radius: 8px;
        border: none; padding: 12px 24px; transition: all 0.4s ease;
        text-transform: uppercase; letter-spacing: 1px;
    }
    div.stButton > button:hover {
        transform: scale(1.05); box-shadow: 0 0 20px rgba(212, 175, 55, 0.6);
    }
    .st-emotion-cache-1r6slb0, [data-testid="stForm"] { 
        border-radius: 12px; border: 1px solid #D4AF37; 
        background-color: #111111; box-shadow: 0 8px 32px rgba(212, 175, 55, 0.15); 
    }
    h1, h2, h3, h4 { color: #D4AF37 !important; font-family: 'Georgia', serif; text-transform: uppercase; letter-spacing: 1.5px;}
    [data-testid="stMetricValue"] { color: #FCF6BA !important; font-weight: 800; text-shadow: 0 0 10px rgba(252,246,186,0.4); }
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
# 2. HỆ THỐNG DATABASE & FIX LỖI ÉP KIỂU
# ==========================================
# Tạo thư mục chứa ảnh Camera
THU_MUC_ANH = 'Vip_Gallery'
if not os.path.exists(THU_MUC_ANH): os.makedirs(THU_MUC_ANH)

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

df_gym = load_db(FILES['gym'], ['Ngày', 'Cân nặng', 'Môn tập', 'Bài tập', 'Hiệp', 'Reps', 'Khối lượng (kg)', 'Volume', 'Calo Đốt (Kcal)', 'Ảnh'])
df_eng = load_db(FILES['eng'], ['Từ vựng', 'Nghĩa', 'Ví dụ', 'Đúng', 'Sai', 'Ngày học cuối'])
df_fash = load_db(FILES['fashion'], ['Tên đồ', 'Loại', 'Thương hiệu', 'Màu sắc', 'Giá tiền', 'Số lần mặc', 'Ảnh'])
df_mov = load_db(FILES['movie'], ['Tên phim', 'Thể loại', 'Rạp', 'Điểm', 'Trạng thái', 'Ngày'])
df_pro = load_db(FILES['profile'], ['Tuổi', 'Chiều cao (cm)', 'Giới tính', 'Mức vận động'])

if df_pro.empty:
    df_pro = pd.DataFrame([{'Tuổi': 20, 'Chiều cao (cm)': 170, 'Giới tính': 'Nam', 'Mức vận động': 'Vừa (3-5 ngày/tuần)'}])

# Ép kiểu dữ liệu chống lỗi Crash App
df_gym['Cân nặng'] = pd.to_numeric(df_gym['Cân nặng'], errors='coerce').fillna(65.0)
df_gym['Volume'] = pd.to_numeric(df_gym['Volume'], errors='coerce').fillna(0)
df_gym['Calo Đốt (Kcal)'] = pd.to_numeric(df_gym['Calo Đốt (Kcal)'], errors='coerce').fillna(0)
df_eng['Đúng'] = pd.to_numeric(df_eng['Đúng'], errors='coerce').fillna(0)
df_eng['Sai'] = pd.to_numeric(df_eng['Sai'], errors='coerce').fillna(0)
df_fash['Giá tiền'] = pd.to_numeric(df_fash['Giá tiền'], errors='coerce').fillna(0)
df_fash['Số lần mặc'] = pd.to_numeric(df_fash['Số lần mặc'], errors='coerce').fillna(0)
df_mov['Điểm'] = pd.to_numeric(df_mov['Điểm'], errors='coerce').fillna(0)

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

    bmi = can_hien_tai / ((cao/100)**2)
    st.markdown(f"**Cân nặng hiện tại:** {can_hien_tai} kg")
    st.markdown(f"**Chỉ số BMI:** {bmi:.1f}")
    if bmi < 18.5: st.warning("⚠️ Thiếu cân")
    elif 18.5 <= bmi <= 24.9: st.success("✅ Chuẩn Body Fitness!")
    elif 25 <= bmi <= 29.9: st.warning("⚠️ Tiền béo phì")
    else: st.error("🚨 Béo phì")

    if gioi == "Nam": bmr = (10 * can_hien_tai) + (6.25 * cao) - (5 * tuoi) + 5
    else: bmr = (10 * can_hien_tai) + (6.25 * cao) - (5 * tuoi) - 161
    he_so = 1.2 if van_dong == "Ít (Không tập)" else (1.55 if van_dong == "Vừa (3-5 ngày/tuần)" else 1.725)
    tdee = bmr * he_so
    
    st.info(f"🔥 **Calo sinh tồn (BMR):** {bmr:.0f} Kcal")
    st.error(f"⚡ **Calo giữ cân (TDEE):** {tdee:.0f} Kcal")

# ==========================================
# 4. TRIỂN KHAI GIAO DIỆN CHỨC NĂNG
# ==========================================

# ------------------------------------------
# TRANG 1: DASHBOARD
# ------------------------------------------
if menu == "💎 Executive Dashboard":
    st.title("💎 TỔNG QUAN ĐẾ CHẾ")
    st.image("https://images.unsplash.com/photo-1549465220-1a8b9238cd48?auto=format&fit=crop&q=80&w=1600", use_container_width=True)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⚖️ Cân nặng", f"{df_gym['Cân nặng'].iloc[-1]} kg" if not df_gym.empty else "N/A")
    c2.metric("📚 Từ vựng tinh hoa", f"{len(df_eng)}")
    c3.metric("💸 Giá trị Tủ đồ", f"{df_fash['Giá tiền'].sum():,.0f} đ" if not df_fash.empty else "0 đ")
    c4.metric("🎬 Phim đã xem", f"{len(df_mov[df_mov['Trạng thái'] == 'Đã xem'])}")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💪 Môn tập ưa thích")
        if not df_gym.empty: st.bar_chart(df_gym['Môn tập'].value_counts(), color="#D4AF37")
    with col2:
        st.subheader("🎬 Thể loại phim")
        if not df_mov.empty: st.bar_chart(df_mov['Thể loại'].value_counts(), color="#FCF6BA")

# ------------------------------------------
# TRANG 2: GYM & CAMERA
# ------------------------------------------
elif menu == "🏋️ Premium Fitness":
    st.title("🏋️ ELITE FITNESS TRACKER")
    st.image("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&q=80&w=1600", use_container_width=True)
    
    t_nhap, t_giao_an = st.tabs(["📝 Lịch Tập & Camera", "💡 Giáo Án Luyện Tập"])
    
    with t_nhap:
        with st.expander("➕ GHI NHẬN BUỔI TẬP", expanded=False):
            # LƯU Ý QUAN TRỌNG: Đưa Camera ra ngoài form để không bị lỗi Streamlit
            st.markdown("### 📸 Selfie Body Check")
            anh_body = st.camera_input("Chụp ảnh body của Boss trước khi lưu!")
            
            with st.form("gym_form"):
                col1, col2, col3 = st.columns(3)
                ngay_tap = col1.date_input("Ngày")
                can_nang = col2.number_input("Cân nặng (kg)", 30.0, 150.0, float(df_gym['Cân nặng'].iloc[-1]) if not df_gym.empty else 65.0)
                mon_tap = col3.selectbox("Hoạt động", ["Gym (Tạ)", "Bơi lội", "Nhặt bóng / Tennis", "Chạy bộ", "Khác"])
                
                c1, c2, c3 = st.columns(3)
                bai_tap = c1.text_input("Tên bài (VD: Bench Press)")
                hiep = c2.number_input("Số hiệp", 1, 300, 4)
                reps = c3.number_input("Số lần (Reps)", 1, 500, 10)
                
                c4, c5 = st.columns(2)
                khoi_luong = c4.number_input("Tạ (kg)", 0.0, 500.0, 0.0)
                calo_dot = c5.number_input("Calo đốt (Kcal)", 0, 3000, 300)
                
                if st.form_submit_button("LƯU THÀNH TÍCH", use_container_width=True):
                    ten_anh = "Không có"
                    if anh_body:
                        ten_anh = f"body_{int(datetime.now().timestamp())}.jpg"
                        with open(os.path.join(THU_MUC_ANH, ten_anh), "wb") as f: f.write(anh_body.getbuffer())
                        
                    vol = hiep * reps * khoi_luong if mon_tap == "Gym (Tạ)" else 0
                    moi = pd.DataFrame([{'Ngày': str(ngay_tap), 'Cân nặng': can_nang, 'Môn tập': mon_tap, 'Bài tập': bai_tap, 
                                         'Hiệp': hiep, 'Reps': reps, 'Khối lượng (kg)': khoi_luong, 'Volume': vol, 'Calo Đốt (Kcal)': calo_dot, 'Ảnh': ten_anh}])
                    df_gym = pd.concat([df_gym, moi], ignore_index=True)
                    save_db(df_gym, FILES['gym'])
                    st.success("Tuyệt vời Boss! Đã lưu.")
                    st.rerun()

        st.markdown("### 🔥 Biểu đồ Calo Đốt")
        if not df_gym.empty:
            chart_calo = df_gym.groupby('Ngày')['Calo Đốt (Kcal)'].sum().reset_index()
            st.bar_chart(chart_calo.set_index('Ngày'), color="#BF953F")
            st.dataframe(df_gym.sort_values(by="Ngày", ascending=False), use_container_width=True)

    with t_giao_an:
        c1, c2, c3 = st.columns(3)
        c1.success("**🏋️ Giáo án Gym**\n\n1. Bench Press: 4 hiệp x 8-10 reps\n2. Incline Dumbbell Press: 3 hiệp x 10 reps\n3. Ép ngực cáp: 3 hiệp x 12 reps\n4. Đẩy tay sau: 4 hiệp x 12 reps\n\n*🔥 Đốt: 300 - 400 Kcal*")
        c2.info("**🏊‍♂️ Bơi Lội Cardio**\n\n1. Khởi động trên cạn: 10 phút\n2. Bơi ếch: 5 vòng\n3. Bơi sải tốc độ cao: 10 vòng\n4. Bơi thả lỏng: 2 vòng\n\n*🔥 Đốt: 500 - 600 Kcal/giờ*")
        c3.warning("**🎾 Tennis / Chạy bộ**\n\n1. Chạy bứt tốc dọc sân.\n2. Di chuyển ngang cường độ cao.\n3. Duy trì nhịp tim Zone 2-3 suốt 1 tiếng.\n\n*🔥 Đốt: 400 - 700 Kcal/giờ*")

# ------------------------------------------
# TRANG 3: ENGLISH 
# ------------------------------------------
elif menu == "🇬🇧 Elite Vocabulary":
    st.title("📚 ROYAL VOCABULARY")
    st.image("https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&q=80&w=1600", use_container_width=True)
    
    with st.expander("➕ NẠP TỪ MỚI", expanded=False):
        with st.form("eng_form"):
            tu = st.text_input("Từ vựng")
            nghia = st.text_input("Nghĩa")
            vidu = st.text_area("Câu ví dụ")
            if st.form_submit_button("NẠP VÀO KHO", use_container_width=True):
                moi = pd.DataFrame([{'Từ vựng': tu, 'Nghĩa': nghia, 'Ví dụ': vidu, 'Đúng': 0, 'Sai': 0, 'Ngày học cuối': str(datetime.now().date())}])
                df_eng = pd.concat([df_eng, moi], ignore_index=True)
                save_db(df_eng, FILES['eng'])
                st.success("Đã nạp!")
                st.rerun()

    st.markdown("### 🧠 Bài Test Trí Nhớ")
    if df_eng.empty: st.info("Hãy thêm từ vựng để test!")
    else:
        if 'quiz_idx' not in st.session_state:
            weights = df_eng['Sai'].astype(float) + 1 
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
            if c1.button("✅ Nhớ Rồi", use_container_width=True):
                df_eng.at[idx, 'Đúng'] += 1
                df_eng.at[idx, 'Ngày học cuối'] = str(datetime.now().date())
                save_db(df_eng, FILES['eng'])
                st.session_state.show_ans = False
                del st.session_state.quiz_idx
                st.rerun()
                
            if c2.button("❌ Quên Mất", use_container_width=True):
                df_eng.at[idx, 'Sai'] += 1
                df_eng.at[idx, 'Ngày học cuối'] = str(datetime.now().date())
                save_db(df_eng, FILES['eng'])
                st.session_state.show_ans = False
                del st.session_state.quiz_idx
                st.rerun()
                
    st.dataframe(df_eng, use_container_width=True, hide_index=True)

# ------------------------------------------
# TRANG 4: TỦ ĐỒ (CAMERA NẰM NGOÀI FORM)
# ------------------------------------------
elif menu == "🧢 Luxury Wardrobe":
    st.title("🧢 STREETWEAR COLLECTION")
    st.image("https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&q=80&w=1600", use_container_width=True)
    
    with st.expander("➕ MUA ĐỒ MỚI", expanded=False):
        st.markdown("### 📸 Chụp đồ trước khi lưu form")
        anh_do = st.camera_input("Đưa đồ vào khung hình!")
        
        with st.form("fash_form"):
            c1, c2 = st.columns(2)
            ten = c1.text_input("Tên sản phẩm")
            brand = c2.selectbox("Thương hiệu", ["Dirty Coins", "Saigon Swagger", "SWE", "Nike", "Dior", "Khác"])
            loai = c1.selectbox("Phân loại", ["Áo", "Quần", "Giày", "Phụ kiện"])
            mau = c2.text_input("Màu sắc")
            gia = st.number_input("Giá mua (VNĐ)", 0, 100000000, 500000, step=50000)
            
            if st.form_submit_button("THÊM VÀO TỦ", use_container_width=True):
                ten_anh = "Không có"
                if anh_do:
                    ten_anh = f"item_{int(datetime.now().timestamp())}.jpg"
                    with open(os.path.join(THU_MUC_ANH, ten_anh), "wb") as f: f.write(anh_do.getbuffer())
                    
                moi = pd.DataFrame([{'Tên đồ': ten, 'Loại': loai, 'Thương hiệu': brand, 'Màu sắc': mau, 'Giá tiền': gia, 'Số lần mặc': 0, 'Ảnh': ten_anh}])
                df_fash = pd.concat([df_fash, moi], ignore_index=True)
                save_db(df_fash, FILES['fashion'])
                st.success("Tủ đồ sang trọng +1!")
                st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🎲 AI Mix Đồ Tự Động")
        if st.button("Mix Ngẫu Nhiên", use_container_width=True):
            aos = df_fash[df_fash['Loại'] == 'Áo']
            quans = df_fash[df_fash['Loại'] == 'Quần']
            if not aos.empty and not quans.empty:
                ao_chon = aos.sample(1).iloc[0]
                quan_chon = quans.sample(1).iloc[0]
                st.success(f"**👕 TOP:** {ao_chon['Tên đồ']} ({ao_chon['Thương hiệu']})")
                st.warning(f"**👖 BOTTOM:** {quan_chon['Tên đồ']} ({quan_chon['Thương hiệu']})")
                st.balloons()
            else: st.error("Tủ đồ chưa đủ Áo và Quần!")
    with c2:
        st.markdown("### 📊 Tổng vốn đầu tư")
        if not df_fash.empty:
            chart_brand = df_fash.groupby('Thương hiệu')['Giá tiền'].sum().reset_index()
            st.bar_chart(chart_brand.set_index('Thương hiệu'), color="#D4AF37")
            
    if not df_fash.empty:
        df_fash['Chi phí/Lần mặc'] = (df_fash['Giá tiền'] / df_fash['Số lần mặc'].replace(0, 1)).astype(int)
        st.dataframe(df_fash, use_container_width=True, hide_index=True)

# ------------------------------------------
# TRANG 5: ĐIỆN ẢNH FULL
# ------------------------------------------
elif menu == "🎬 VIP Cinema":
    st.title("🍿 VIP CINEMA LOUNGE")
    st.image("https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?auto=format&fit=crop&q=80&w=1600", use_container_width=True)
    
    with st.expander("➕ LƯU PHIM / WATCHLIST", expanded=False):
        with st.form("mov_form"):
            c1, c2 = st.columns(2)
            ten = c1.text_input("Tên bộ phim")
            the_loai = c2.selectbox("Thể loại", ["Hành động", "Tâm lý/Tình cảm", "Kinh dị", "Viễn tưởng", "Khác"])
            rap = c1.selectbox("Rạp / Nền tảng", ["Galaxy Sala", "CGV", "Netflix", "Khác"])
            trang_thai = c2.radio("Trạng thái", ["Đã xem", "Muốn xem (Watchlist)"], horizontal=True)
            diem = st.slider("Chấm điểm VVIP", 1.0, 10.0, 9.0)
            ngay = st.date_input("Ngày xem/Dự kiến")
            
            if st.form_submit_button("LƯU KÝ ỨC", use_container_width=True):
                moi = pd.DataFrame([{'Ngày': str(ngay), 'Tên phim': ten, 'Thể loại': the_loai, 'Rạp': rap, 'Điểm': diem if trang_thai=='Đã xem' else 0, 'Trạng thái': trang_thai}])
                df_mov = pd.concat([df_mov, moi], ignore_index=True)
                save_db(df_mov, FILES['movie'])
                st.success("Tuyệt đỉnh!")
                st.rerun()

    t_watched, t_watchlist = st.tabs(["✅ PHIM ĐÃ XEM", "📌 WATCHLIST"])
    
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
            
    with t_watchlist:
        chua_xem = df_mov[df_mov['Trạng thái'] == 'Muốn xem (Watchlist)']
        st.dataframe(chua_xem[['Ngày', 'Tên phim', 'Thể loại', 'Rạp']], use_container_width=True, hide_index=True)
