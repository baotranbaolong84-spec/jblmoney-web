import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import time
from datetime import datetime
import streamlit.components.v1 as components

# =======================================
# 1. CẤU HÌNH TRANG WEB
# =======================================
st.set_page_config(page_title="JBLMONEY Ultimate", page_icon="💎", layout="centered")

# =======================================
# 2. CẤU HÌNH AI CHÍNH HÃNG (MÃ AIza)
# =======================================
# ⚠️ BOSS XÓA DÒNG CHỮ TRONG NGOẶC KÉP VÀ DÁN MÃ AIza... CỦA BOSS VÀO ĐÂY:
API_KEY_CUA_BOSS = "AQ.Ab8RN6LefgFjAvHsU8Nf5jLIRK2a8QxGFkG7I5kSKmmdCqqbYg"

try:
    genai.configure(api_key=API_KEY_CUA_BOSS)
    bo_nao_ai = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Lỗi cấu hình AI: {e}")

# =======================================
# 3. KHO DỮ LIỆU & CSS GIAO DIỆN
# =======================================
FILE_DATA = 'so_thu_chi.csv'
THU_MUC_ANH = 'Hoa_Don'
if not os.path.exists(THU_MUC_ANH): os.makedirs(THU_MUC_ANH)

def tai_du_lieu():
    if os.path.exists(FILE_DATA):
        try:
            df = pd.read_csv(FILE_DATA)
            if 'Ví' not in df.columns: df['Ví'] = 'Tiền mặt'
            if 'Hóa đơn' not in df.columns: df['Hóa đơn'] = 'Không có'
            return df
        except: pass
    return pd.DataFrame(columns=['Ngày', 'Loại', 'Danh mục', 'Ví', 'Số tiền (VNĐ)', 'Ghi chú', 'Hóa đơn'])

df = tai_du_lieu()
df['Số tiền (VNĐ)'] = pd.to_numeric(df['Số tiền (VNĐ)'], errors='coerce').fillna(0)
df['Tháng'] = pd.to_datetime(df['Ngày'], errors='coerce').dt.month
df['Tháng'] = df['Tháng'].fillna(datetime.now().month).astype(int)

st.markdown("""
<style>
    div[data-testid="metric-container"] { background-color: #1E1E2E !important; border-radius: 15px !important; padding: 20px !important; box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important; border: 1px solid #333 !important; }
    div.stButton > button { background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%) !important; color: black !important; font-weight: bold !important; border-radius: 8px !important; border: none !important; }
    div.stButton > button:hover { opacity: 0.8 !important; }
    div[data-testid="stSidebar"] div.stButton > button { background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%) !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# =======================================
# 4. HỆ THỐNG ĐĂNG NHẬP
# =======================================
if 'dang_nhap' not in st.session_state: st.session_state.dang_nhap = False
if not st.session_state.dang_nhap:
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<h2 style='text-align: center; color: #00C9FF; margin-top: 50px;'>💎 ĐĂNG NHẬP JBLMONEY</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Nhập mã PIN bảo mật (1234)", type="password", key="login_pin")
        if st.button("🚀 Đăng Nhập", use_container_width=True):
            if pwd == "1234":
                st.session_state.dang_nhap = True
                st.rerun()
            else: st.error("Sai mã PIN!")
    st.stop()

# =======================================
# 5. SIDEBAR & CHAT AI TRỰC TIẾP
# =======================================
tong_thu_all = df[df['Loại'] == 'Thu nhập']['Số tiền (VNĐ)'].sum()
tong_chi_all = df[df['Loại'] == 'Chi tiêu']['Số tiền (VNĐ)'].sum()
so_du_all = tong_thu_all - tong_chi_all

with st.sidebar:
    st.markdown("### 💎 Menu Điều Khiển")
    if st.button("Đăng xuất", key="logout"): 
        st.session_state.dang_nhap = False; st.rerun()
    st.markdown("---")
    thang_loc = st.selectbox("📅 Chọn Tháng", range(1, 13), index=int(datetime.now().month-1))
    st.markdown("---")
    st.markdown("### 🤖 Trợ lý AI (Đã găm sẵn khóa AIza)")
    chat_box = st.container(height=350, border=True)
    if "chat" not in st.session_state: st.session_state.chat = [{"role": "assistant", "content": "Khóa AIza đã kích hoạt! Hỏi em đi Boss!"}]
    for msg in st.session_state.chat: chat_box.chat_message(msg["role"]).write(msg["content"])
    
    if q := st.chat_input("Hỏi AI..."):
        st.session_state.chat.append({"role": "user", "content": q})
        chat_box.chat_message("user").write(q)
        
        try:
            lenh_ai = f"Dữ liệu của Boss: Thu {tong_thu_all}, Chi {tong_chi_all}, Dư {so_du_all}. Hãy trả lời: {q}"
            ans = bo_nao_ai.generate_content(lenh_ai)
            cau_tra_loi = ans.text
        except Exception as e:
            cau_tra_loi = f"Lỗi AI: {e}"
            
        chat_box.chat_message("assistant").write(cau_tra_loi)
        st.session_state.chat.append({"role": "assistant", "content": cau_tra_loi})

# =======================================
# 6. MÀN HÌNH CHÍNH & TABS CHỨC NĂNG
# =======================================
df_loc = df[df['Tháng'] == thang_loc]
tong_thu = df_loc[df_loc['Loại'] == 'Thu nhập']['Số tiền (VNĐ)'].sum()
tong_chi = df_loc[df_loc['Loại'] == 'Chi tiêu']['Số tiền (VNĐ)'].sum()

st.markdown(f"<h1>📊 Báo cáo Tài Chính (Tháng {thang_loc})</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric("💰 SỐ DƯ TÀI KHOẢN", f"{tong_thu - tong_chi:,.0f} ₫")
c2.metric("🟢 DÒNG TIỀN VÀO", f"{tong_thu:,.0f} ₫")
c3.metric("🔴 DÒNG TIỀN RA", f"{tong_chi:,.0f} ₫")
st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 GHI CHÉP", "💣 NGÂN SÁCH", "📈 AI BÓC PHỐT", "🧮 TIỆN ÍCH", "📋 SỔ EXCEL"])

# --- TAB 1: NHẬP LIỆU ---
with tab1:
    with st.form("form_nhap", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            loai = st.radio("Loại", ["Chi tiêu", "Thu nhập"], horizontal=True)
            ngay = st.date_input("Ngày")
            danh_muc = st.text_input("Danh mục")
        with col2:
            tien = st.number_input("Số tiền (VNĐ)", min_value=0, step=50000)
            vi_tien = st.selectbox("Ví", ["Tiền mặt", "Ngân hàng", "Thẻ Tín dụng"])
            ghi_chu = st.text_input("Ghi chú")
        
        file_anh = st.file_uploader("📸 Tải ảnh Hóa đơn", type=["jpg", "png"])
        if st.form_submit_button("LƯU GIAO DỊCH", use_container_width=True):
            ten_file = "Không có"
            if file_anh:
                ten_file = f"bill_{int(time.time())}.png"
                with open(os.path.join(THU_MUC_ANH, ten_file), "wb") as f: f.write(file_anh.getbuffer())
            dl_moi = pd.DataFrame([{'Ngày': str(ngay), 'Loại': loai, 'Danh mục': danh_muc, 'Ví': vi_tien, 'Số tiền (VNĐ)': tien, 'Ghi chú': ghi_chu, 'Hóa đơn': ten_file}])
            df = pd.concat([df.drop(columns=['Tháng'], errors='ignore'), dl_moi], ignore_index=True)
            df.to_csv(FILE_DATA, index=False)
            st.success("Lưu thành công!")
            st.rerun()

# --- TAB 2: QUẢ BOM ---
with tab2:
    han_muc = st.slider("Hạn mức chi tiêu:", 1000000, 50000000, 10000000, step=1000000)
    phan_tram = (tong_chi / han_muc) * 100 if han_muc > 0 else 0
    st.progress(min(phan_tram / 100, 1.0))
    st.write(f"Đã tiêu: **{tong_chi:,.0f} ₫** / **{han_muc:,.0f} ₫** ({phan_tram:.1f}%)")
    if tong_chi > han_muc: st.error("🚨 CẢNH BÁO: VƯỢT HẠN MỨC!")

# --- TAB 3: AI BÓC PHỐT ---
with tab3:
    df_chi = df_loc[df_loc['Loại'] == 'Chi tiêu']
    if not df_chi.empty:
        st.bar_chart(df_chi.groupby('Danh mục')['Số tiền (VNĐ)'].sum().reset_index(), x='Danh mục', y='Số tiền (VNĐ)', color="#00C9FF")
    
    if st.button("🔥 AI soi mói thói quen xài tiền!", type="primary", use_container_width=True):
        with st.spinner("AI đang check dữ liệu..."):
            try:
                ds_chi = df_chi[['Danh mục', 'Số tiền (VNĐ)']].to_string()
                lenh = f"Boss đã tiêu: {ds_chi}. Hãy đóng vai chuyên gia tài chính đanh đá, châm biếm thói tiêu hoang này. Cấm khen!"
                ket_qua = bo_nao_ai.generate_content(lenh)
                st.error(ket_qua.text)
            except Exception as e:
                st.warning(f"Lỗi AI: {e}")

# --- TAB 4: CHIA BILL ---
with tab4:
    c_b1, c_b2 = st.columns(2)
    tong_bill = c_b1.number_input("Tổng hóa đơn:", min_value=0, step=20000)
    so_nguoi = c_b2.number_input("Số người:", min_value=1, step=1, value=1)
    if tong_bill > 0: st.success(f"👉 Mỗi người: **{tong_bill / so_nguoi:,.0f} ₫**")

# --- TAB 5: SỔ EXCEL ---
with tab5:
    df_hien_thi = df.copy().drop(columns=['Tháng'], errors='ignore')
    df_da_sua = st.data_editor(df_hien_thi, num_rows="dynamic", use_container_width=True, key="excel_edit")
    if st.button("💾 LƯU THAY ĐỔI", use_container_width=True, type="primary"):
        df_da_sua.to_csv(FILE_DATA, index=False)
        st.success("Đã lưu vào cơ sở dữ liệu gốc!")
        st.rerun()
