import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. UI/UX LUXURY GOLD EDITION (MẠ VÀNG TOÀN BỘ)
# ==========================================
st.set_page_config(page_title="Boss VIP OS", page_icon="👑", layout="wide", initial_sidebar_state="expanded")

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
# 2. HỆ THỐNG DATABASE
# ==========================================
FILES = {'gym': 'gym_vip.csv', 'eng': 'eng_vip.csv', 'fashion': 'fashion_vip.csv', 'movie': 'movie_vip.csv', 'profile': 'profile_vip.csv'}

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

df_gym = load_db(FILES['gym'], ['Ngày', 'Cân nặng', 'Môn tập', 'Khối lượng (kg)', 'Calo Đốt (Kcal)'])
df_eng = load_db(FILES['eng'], ['Từ vựng', 'Nghĩa', 'Đúng', 'Sai'])
df_fash = load_db(FILES['fashion'], ['Tên đồ', 'Thương hiệu', 'Giá tiền', 'Số lần mặc'])
df_mov = load_db(FILES['movie'], ['Ngày', 'Tên phim', 'Rạp', 'Điểm'])

# ==========================================
# 3. ĐIỀU HƯỚNG BẢNG ĐIỀU KHIỂN
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

# ==========================================
# 4. GIAO DIỆN CHỨC NĂNG
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
    c3.metric("💸 Đầu tư trang phục", f"{df_fash['Giá tiền'].sum():,.0f} đ" if not df_fash.empty else "0 đ")
    c4.metric("🎬 Số vé VVIP", f"{len(df_mov)}")

# ------------------------------------------
# TRANG 2: GYM (TÍCH HỢP CAMERA SELFIE BODY)
# ------------------------------------------
elif menu == "🏋️ Premium Fitness":
    st.title("🏋️ ELITE FITNESS TRACKER")
    st.image("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&q=80&w=1600", use_container_width=True)
    
    with st.expander("➕ GHI NHẬN BUỔI TẬP & SELFIE", expanded=False):
        with st.form("gym_form"):
            col1, col2 = st.columns(2)
            ngay_tap = col1.date_input("Ngày")
            can_nang = col2.number_input("Cân nặng (kg)", 30.0, 150.0, float(df_gym['Cân nặng'].iloc[-1]) if not df_gym.empty else 65.0)
            mon_tap = col1.selectbox("Hoạt động", ["Gym", "Bơi lội", "Tennis", "Khác"])
            calo_dot = col2.number_input("Calo đốt (Kcal)", 0, 3000, 300)
            
            st.markdown("### 📸 Chụp ảnh Body Check")
            anh_body = st.camera_input("Selfie sau tập")
            
            if st.form_submit_button("LƯU THÀNH TÍCH", use_container_width=True):
                moi = pd.DataFrame([{'Ngày': str(ngay_tap), 'Cân nặng': can_nang, 'Môn tập': mon_tap, 'Khối lượng (kg)': 0, 'Calo Đốt (Kcal)': calo_dot}])
                df_gym = pd.concat([df_gym, moi], ignore_index=True)
                save_db(df_gym, FILES['gym'])
                st.success("Tuyệt vời Boss!")
                st.rerun()

    st.markdown("### 📈 Biểu đồ Calo Đốt")
    if not df_gym.empty:
        chart_calo = df_gym.groupby('Ngày')['Calo Đốt (Kcal)'].sum().reset_index()
        st.bar_chart(chart_calo.set_index('Ngày'), color="#D4AF37")
        st.dataframe(df_gym, use_container_width=True)

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
            if st.form_submit_button("NẠP VÀO KHO", use_container_width=True):
                moi = pd.DataFrame([{'Từ vựng': tu, 'Nghĩa': nghia, 'Đúng': 0, 'Sai': 0}])
                df_eng = pd.concat([df_eng, moi], ignore_index=True)
                save_db(df_eng, FILES['eng'])
                st.success("Đã lưu!")
                st.rerun()

    st.markdown("### 🧠 Kiểm Tra Trí Nhớ")
    if not df_eng.empty:
        idx = df_eng.sample(1).index[0]
        card = df_eng.loc[idx]
        st.markdown(f"<h1 style='text-align:center; font-size: 60px; text-shadow: 0 0 15px #D4AF37;'>{card['Từ vựng']}</h1>", unsafe_allow_html=True)
        with st.expander("👉 Bấm để xem nghĩa"):
            st.markdown(f"Nghĩa:")
    else: st.info("Thêm từ vựng để bắt đầu.")
    st.dataframe(df_eng, use_container_width=True, hide_index=True)

# ------------------------------------------
# TRANG 4: TỦ ĐỒ (TÍCH HỢP CAMERA CHỤP ĐỒ)
# ------------------------------------------
elif menu == "🧢 Luxury Wardrobe":
    st.title("🧢 STREETWEAR COLLECTION")
    st.image("https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&q=80&w=1600", use_container_width=True)
    
    with st.expander("➕ MUA ĐỒ MỚI & CHỤP ẢNH", expanded=False):
        with st.form("fash_form"):
            c1, c2 = st.columns(2)
            ten = c1.text_input("Tên sản phẩm")
            brand = c2.selectbox("Thương hiệu", ["Dirty Coins", "Saigon Swagger", "Nike", "Dior", "Gucci", "Khác"])
            gia = st.number_input("Giá mua (VNĐ)", 0, 100000000, 500000, step=50000)
            
            st.markdown("### 📸 Chụp ảnh món đồ mới")
            anh_do = st.camera_input("Đưa đồ vào khung hình")
            
            if st.form_submit_button("THÊM VÀO BỘ SƯU TẬP", use_container_width=True):
                moi = pd.DataFrame([{'Tên đồ': ten, 'Thương hiệu': brand, 'Giá tiền': gia, 'Số lần mặc': 0}])
                df_fash = pd.concat([df_fash, moi], ignore_index=True)
                save_db(df_fash, FILES['fashion'])
                st.success("Tủ đồ sang trọng +1!")
                st.rerun()

    if not df_fash.empty:
        st.markdown("### 📊 Tổng vốn đầu tư")
        chart_brand = df_fash.groupby('Thương hiệu')['Giá tiền'].sum().reset_index()
        st.bar_chart(chart_brand.set_index('Thương hiệu'), color="#D4AF37")
        st.dataframe(df_fash, use_container_width=True, hide_index=True)

# ------------------------------------------
# TRANG 5: ĐIỆN ẢNH
# ------------------------------------------
elif menu == "🎬 VIP Cinema":
    st.title("🍿 VIP CINEMA LOUNGE")
    st.image("https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?auto=format&fit=crop&q=80&w=1600", use_container_width=True)
    
    with st.expander("➕ LƯU NHẬT KÝ ĐIỆN ẢNH", expanded=False):
        with st.form("mov_form"):
            c1, c2 = st.columns(2)
            ten = c1.text_input("Tên bộ phim")
            rap = c2.selectbox("Rạp / Nền tảng", ["Galaxy Sala", "CGV Gold Class", "Netflix Premium", "Khác"])
            diem = st.slider("Chấm điểm VVIP", 1.0, 10.0, 9.0)
            ngay = st.date_input("Ngày xem")
            
            if st.form_submit_button("LƯU KÝ ỨC", use_container_width=True):
                moi = pd.DataFrame([{'Ngày': str(ngay), 'Tên phim': ten, 'Rạp': rap, 'Điểm': diem}])
                df_mov = pd.concat([df_mov, moi], ignore_index=True)
                save_db(df_mov, FILES['movie'])
                st.success("Tuyệt đỉnh!")
                st.rerun()

    if not df_mov.empty:
        chart_rap = df_mov.groupby('Rạp').size().reset_index(name='Số vé')
        st.bar_chart(chart_rap.set_index('Rạp'), color="#FCF6BA")
        st.dataframe(df_mov, use_container_width=True, hide_index=True)
