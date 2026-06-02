import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, timedelta
import altair as alt

# ==========================================
# 1. UI/UX MAX LEVEL (DARK MODE HIỆN ĐẠI)
# ==========================================
st.set_page_config(page_title="Boss Life OS Pro Max", page_icon="🔥", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    
    /* Giao diện nút bấm Gradient 3D */
    div.stButton > button {
        background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
        color: white !important; font-weight: 900; border-radius: 10px;
        border: none; padding: 12px 24px; transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.02); box-shadow: 0 10px 20px rgba(255,65,108,0.4);
    }
    
    /* Thẻ Card Hiển Thị */
    .st-emotion-cache-1r6slb0, [data-testid="stForm"] { 
        border-radius: 16px; border: 1px solid #333; 
        background-color: #1a1a24; box-shadow: 0 4px 15px rgba(0,0,0,0.3); 
    }
    
    /* Chỉnh màu Tab */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #2b2b3c; border-radius: 8px 8px 0px 0px; 
        padding: 10px 20px; font-weight: bold; 
    }
    .stTabs [aria-selected="true"] { background-color: #FF4B2B; color: white !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATABASE ENGINE (LÕI DỮ LIỆU NÂNG CẤP)
# ==========================================
FILES = {'gym': 'gym_v2.csv', 'eng': 'eng_v2.csv', 'fashion': 'fashion_v2.csv', 'movie': 'movie_v2.csv'}

def load_db(file_name, columns):
    if os.path.exists(file_name):
        try: 
            df = pd.read_csv(file_name)
            # Tự động cập nhật cột nếu file cũ thiếu
            for col in columns:
                if col not in df.columns: df[col] = 0 if 'Số' in col or 'Giá' in col else ''
            return df
        except: pass
    return pd.DataFrame(columns=columns)

def save_db(df, file_name):
    df.to_csv(file_name, index=False)

df_gym = load_db(FILES['gym'], ['Ngày', 'Môn tập', 'Bài tập', 'Hiệp', 'Số lần (Reps)', 'Khối lượng (kg)', 'Volume', 'Ghi chú'])
df_eng = load_db(FILES['eng'], ['Từ vựng', 'Nghĩa', 'Ví dụ', 'Đúng', 'Sai', 'Ngày học cuối'])
df_fash = load_db(FILES['fashion'], ['Tên đồ', 'Loại', 'Thương hiệu', 'Màu sắc', 'Giá tiền', 'Số lần mặc'])
df_mov = load_db(FILES['movie'], ['Tên phim', 'Thể loại', 'Rạp', 'Điểm', 'Trạng thái', 'Ngày'])

# ==========================================
# 3. SIDEBAR - BỘ CHỈ HUY
# ==========================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #FF4B2B;'>🔥 LIFE OS MAX</h1>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("ĐIỀU HƯỚNG:", 
                    ["📊 Dashboard Phân Tích", 
                     "🏋️ Gym & Thể Thao", 
                     "🇬🇧 Trạm Vocabulary", 
                     "🧢 Tủ Đồ Analytics", 
                     "🎬 Trạm Điện Ảnh"])
    st.markdown("---")
    
    # Tính toán Streak Tiếng Anh
    streak = 0
    if not df_eng.empty:
        dates = pd.to_datetime(df_eng['Ngày học cuối']).dt.date.sort_values().unique()
        today = datetime.now().date()
        for i in range(len(dates)):
            if today - timedelta(days=i) in dates: streak += 1
            else: break
            
    st.metric("🔥 English Streak", f"{streak} Ngày", "Don't break the chain!")

# ==========================================
# 4. GIAO DIỆN CHỨC NĂNG (THEO TAB)
# ==========================================

# ------------------------------------------
# TRANG 1: DASHBOARD
# ------------------------------------------
if menu == "📊 Dashboard Phân Tích":
    st.title("📊 TỔNG QUAN HỆ THỐNG")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🏋️ Buổi tập", f"{len(df_gym['Ngày'].unique()) if not df_gym.empty else 0}")
    c2.metric("📚 Từ vựng", f"{len(df_eng)}")
    c3.metric("🧢 Tủ đồ", f"{len(df_fash)}")
    c4.metric("🎬 Phim đã xem", f"{len(df_mov[df_mov['Trạng thái'] == 'Đã xem'])}")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💪 Môn thể thao yêu thích")
        if not df_gym.empty:
            st.bar_chart(df_gym['Môn tập'].value_counts())
        else: st.info("Chưa có dữ liệu")
    with col2:
        st.subheader("🎬 Thể loại phim yêu thích")
        if not df_mov.empty:
            st.bar_chart(df_mov['Thể loại'].value_counts())
        else: st.info("Chưa có dữ liệu")

# ------------------------------------------
# TRANG 2: GYM TRACKER PRO
# ------------------------------------------
elif menu == "🏋️ Gym & Thể Thao":
    st.title("🏋️ TRACKER THỂ CHẤT")
    
    with st.expander("➕ THÊM BÀI TẬP / HOẠT ĐỘNG", expanded=False):
        with st.form("gym_form"):
            col1, col2, col3 = st.columns(3)
            ngay_tap = col1.date_input("Ngày")
            mon_tap = col2.selectbox("Hoạt động", ["Tập Tạ (Gym)", "Bơi lội", "Nhặt bóng / Tennis", "Cardio", "Khác"])
            bai_tap = col3.text_input("Tên bài (VD: Bench Press, Bơi ếch)")
            
            c1, c2, c3 = st.columns(3)
            hiep = c1.number_input("Số hiệp (Sets)", 1, 20, 1)
            reps = c2.number_input("Số lần (Reps)", 1, 100, 1)
            khoi_luong = c3.number_input("Khối lượng (kg)", 0.0, 500.0, 0.0)
            
            if st.form_submit_button("LƯU KẾT QUẢ", use_container_width=True):
                volume = hiep * reps * khoi_luong
                moi = pd.DataFrame([{'Ngày': str(ngay_tap), 'Môn tập': mon_tap, 'Bài tập': bai_tap, 
                                     'Hiệp': hiep, 'Số lần (Reps)': reps, 'Khối lượng (kg)': khoi_luong, 
                                     'Volume': volume, 'Ghi chú': ''}])
                df_gym = pd.concat([df_gym, moi], ignore_index=True)
                save_db(df_gym, FILES['gym'])
                st.success("Đã lưu dữ liệu!")
                st.rerun()

    st.markdown("### 📈 Biểu Đồ Volume Luyện Tập (Sức Mạnh)")
    if not df_gym.empty and df_gym['Volume'].sum() > 0:
        chart_data = df_gym.groupby('Ngày')['Volume'].sum().reset_index()
        st.area_chart(chart_data.set_index('Ngày'))
    
    st.dataframe(df_gym.sort_values(by="Ngày", ascending=False), use_container_width=True, hide_index=True)

# ------------------------------------------
# TRANG 3: TRẠM TIẾNG ANH (SPACED REPETITION)
# ------------------------------------------
elif menu == "🇬🇧 Trạm Vocabulary":
    st.title("📚 TRẠM TỪ VỰNG CHUYÊN SÂU")
    
    with st.expander("➕ NẠP TỪ MỚI", expanded=False):
        with st.form("eng_form"):
            tu = st.text_input("Từ vựng")
            nghia = st.text_input("Nghĩa")
            vidu = st.text_area("Câu ví dụ")
            if st.form_submit_button("LƯU TỪ", use_container_width=True):
                moi = pd.DataFrame([{'Từ vựng': tu, 'Nghĩa': nghia, 'Ví dụ': vidu, 'Đúng': 0, 'Sai': 0, 'Ngày học cuối': str(datetime.now().date())}])
                df_eng = pd.concat([df_eng, moi], ignore_index=True)
                save_db(df_eng, FILES['eng'])
                st.success("Đã thêm!")
                st.rerun()

    st.markdown("### 🧠 Bài Test Trí Nhớ (Quizz Mode)")
    if df_eng.empty: st.info("Hãy thêm từ vựng để bắt đầu Test!")
    else:
        # Ưu tiên lấy những từ hay làm sai
        if 'quiz_word' not in st.session_state:
            weights = df_eng['Sai'] + 1  # Từ nào sai nhiều tỷ lệ ra càng cao
            st.session_state.quiz_idx = df_eng.sample(1, weights=weights).index[0]
        
        idx = st.session_state.quiz_idx
        card = df_eng.loc[idx]
        
        st.markdown(f"<h1 style='text-align:center; font-size:60px; color:#00C9FF;'>{card['Từ vựng']}</h1>", unsafe_allow_html=True)
        
        if 'show_ans' not in st.session_state: st.session_state.show_ans = False
        
        if not st.session_state.show_ans:
            if st.button("Lật Thẻ Trả Lời", use_container_width=True):
                st.session_state.show_ans = True
                st.rerun()
        else:
            st.markdown(f"<h3 style='text-align:center; color:#FF4B2B;'>👉 Nghĩa: {card['Nghĩa']}</h3>", unsafe_allow_html=True)
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

    st.markdown("### 🗂️ Kho Dữ Liệu Từ Vựng")
    st.dataframe(df_eng, use_container_width=True, hide_index=True)

# ------------------------------------------
# TRANG 4: TỦ ĐỒ (FASHION ANALYTICS)
# ------------------------------------------
elif menu == "🧢 Tủ Đồ Analytics":
    st.title("🧢 STREETWEAR WARDROBE")
    
    with st.expander("➕ MUA ĐỒ MỚI (THÊM VÀO TỦ)", expanded=False):
        with st.form("fash_form"):
            c1, c2 = st.columns(2)
            ten = c1.text_input("Tên sản phẩm")
            loai = c2.selectbox("Phân loại", ["Áo", "Quần", "Giày", "Phụ kiện"])
            brand = c1.selectbox("Thương hiệu", ["Dirty Coins", "Saigon Swagger", "Hades", "SWE", "Nike", "Khác"])
            gia = c2.number_input("Giá mua (VNĐ)", 0, 50000000, step=100000)
            mau = st.text_input("Màu sắc")
            
            if st.form_submit_button("CẤT VÀO TỦ", use_container_width=True):
                moi = pd.DataFrame([{'Tên đồ': ten, 'Loại': loai, 'Thương hiệu': brand, 'Màu sắc': mau, 'Giá tiền': gia, 'Số lần mặc': 0}])
                df_fash = pd.concat([df_fash, moi], ignore_index=True)
                save_db(df_fash, FILES['fashion'])
                st.success("Tủ đồ +1!")
                st.rerun()

    c1, c2, c3 = st.columns(3)
    if not df_fash.empty:
        tong_gt = df_fash['Giá tiền'].sum()
        c1.metric("Tổng giá trị tủ đồ", f"{tong_gt:,.0f} đ")
        
        # Bảng điều khiển Mặc Đồ
        with c2:
            st.markdown("### Hàng Mới Mặc")
            chon_do = st.selectbox("Chọn món đồ bạn vừa mặc:", df_fash['Tên đồ'])
            if st.button("Cộng 1 lần mặc", use_container_width=True):
                idx = df_fash[df_fash['Tên đồ'] == chon_do].index[0]
                df_fash.at[idx, 'Số lần mặc'] += 1
                save_db(df_fash, FILES['fashion'])
                st.success("Đã ghi nhận!")
                st.rerun()
                
    st.markdown("### 📊 Phân tích độ khấu hao (Cost Per Wear)")
    if not df_fash.empty:
        df_fash['Chi phí/Lần mặc'] = (df_fash['Giá tiền'] / df_fash['Số lần mặc'].replace(0, 1)).astype(int)
        st.dataframe(df_fash, use_container_width=True, hide_index=True)

# ------------------------------------------
# TRANG 5: NHẬT KÝ PHIM ẢNH (LETTERBOXD)
# ------------------------------------------
elif menu == "🎬 Trạm Điện Ảnh":
    st.title("🍿 ĐẾ CHẾ ĐIỆN ẢNH")
    
    with st.expander("➕ CẬP NHẬT PHIM MỚI", expanded=False):
        with st.form("mov_form"):
            c1, c2 = st.columns(2)
            ten = c1.text_input("Tên bộ phim")
            the_loai = c2.selectbox("Thể loại", ["Hành động", "Tâm lý", "Kinh dị", "Hài Hước", "Viễn tưởng"])
            rap = c1.selectbox("Rạp / Nền tảng", ["Galaxy Sala", "CGV", "Netflix", "Web lậu"])
            trang_thai = c2.radio("Trạng thái", ["Đã xem", "Muốn xem (Watchlist)"], horizontal=True)
            diem = st.slider("Chấm điểm", 1.0, 10.0, 8.0)
            ngay = st.date_input("Ngày xem/dự kiến")
            
            if st.form_submit_button("LƯU PHIM", use_container_width=True):
                moi = pd.DataFrame([{'Tên phim': ten, 'Thể loại': the_loai, 'Rạp': rap, 'Điểm': diem if trang_thai=='Đã xem' else 0, 'Trạng thái': trang_thai, 'Ngày': str(ngay)}])
                df_mov = pd.concat([df_mov, moi], ignore_index=True)
                save_db(df_mov, FILES['movie'])
                st.success("Tuyệt vời!")
                st.rerun()

    t_watched, t_watchlist = st.tabs(["✅ PHIM ĐÃ XEM", "📌 WATCHLIST (Đợi rạp)"])
    
    with t_watched:
        da_xem = df_mov[df_mov['Trạng thái'] == 'Đã xem']
        if not da_xem.empty:
            cols = st.columns(3)
            for i, row in da_xem.iloc[::-1].iterrows():
                col_idx = i % 3
                with cols[col_idx]:
                    st.markdown(f"""
                    <div class="st-emotion-cache-1r6slb0" style="border-left: 4px solid #FF4B2B;">
                        <h3 style="margin:0;">{row['Tên phim']}</h3>
                        <p style="margin:0; color:#888;">{row['Thể loại']} | {row['Rạp']}</p>
                        <h4 style="margin:5px 0 0 0; color:#FFD700;">{'⭐'*int(row['Điểm'])} {row['Điểm']}</h4>
                    </div>
                    <br>
                    """, unsafe_allow_html=True)
    
    with t_watchlist:
        chua_xem = df_mov[df_mov['Trạng thái'] == 'Muốn xem (Watchlist)']
        st.dataframe(chua_xem[['Ngày', 'Tên phim', 'Thể loại', 'Rạp']], use_container_width=True, hide_index=True)
