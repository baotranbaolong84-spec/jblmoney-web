import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import time
from datetime import datetime
import streamlit.components.v1 as components

# =======================================
# 1. CẤU HÌNH TRANG WEB (BẮT BUỘC ĐẶT ĐẦU TIÊN)
# =======================================
st.set_page_config(page_title="JBLMONEY Ultimate", page_icon="💎", layout="centered")

# =======================================
# 2. CẤU HÌNH API AI GEMINI
# =======================================
# ⚠️ BOSS HÃY DÁN MÃ API CỦA BOSS VÀO GIỮA HAI DẤU NGOẶC KÉP Ở DÒNG DƯỚI NHÉ:
genai.configure(api_key="AQ.Ab8RN6I-0Iv3yI3lz0K_TBT9W1Z09NIeHUvDdR50_RKpr5iMaQ")
bo_nao_ai = genai.GenerativeModel('gemini-1.5-flash')

# =======================================
# 3. CẤU HÌNH KHO DỮ LIỆU & ẢNH HÓA ĐƠN
# =======================================
FILE_DATA = 'so_thu_chi.csv'
THU_MUC_ANH = 'Hoa_Don'
if not os.path.exists(THU_MUC_ANH): 
    os.makedirs(THU_MUC_ANH)

def tai_du_lieu():
    if os.path.exists(FILE_DATA):
        try:
            df = pd.read_csv(FILE_DATA)
            if 'Ví' not in df.columns: df['Ví'] = 'Tiền mặt'
            if 'Hóa đơn' not in df.columns: df['Hóa đơn'] = 'Không có'
            return df
        except:
            pass
    return pd.DataFrame(columns=['Ngày', 'Loại', 'Danh mục', 'Ví', 'Số tiền (VNĐ)', 'Ghi chú', 'Hóa đơn'])

df = tai_du_lieu()
# Chuẩn hóa dữ liệu an toàn
df['Số tiền (VNĐ)'] = pd.to_numeric(df['Số tiền (VNĐ)'], errors='coerce').fillna(0)
df['Tháng'] = pd.to_datetime(df['Ngày'], errors='coerce').dt.month
df['Tháng'] = df['Tháng'].fillna(datetime.now().month).astype(int)

# =======================================
# 4. CSS TÂN TRANG GIAO DIỆN & RESPONSIVE ĐIỆN THOẠI
# =======================================
st.markdown("""
<style>
    /* Định dạng các khối hiển thị tiền tệ dạng Hộp nổi */
    div[data-testid="metric-container"] {
        background-color: #1E1E2E !important; border-radius: 15px !important; padding: 20px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important; border: 1px solid #333 !important;
    }
    /* Đổi màu Nút bấm thành gradient */
    div.stButton > button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%) !important;
        color: black !important; font-weight: bold !important; border-radius: 8px !important; border: none !important;
    }
    div.stButton > button:hover { opacity: 0.8 !important; }
    /* Nút Đăng xuất màu đỏ */
    div[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%) !important; color: white !important;
    }

    /* Tự động thu nhỏ cân đối khi mở trên điện thoại */
    @media (max-width: 768px) {
        div[data-testid="metric-container"] { padding: 10px !important; margin-bottom: 10px !important; }
        div[data-testid="metric-container"] label { font-size: 12px !important; }
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] { font-size: 20px !important; }
        h1 { font-size: 22px !important; text-align: center !important; }
        div[data-testid="stTabs"] button { font-size: 12px !important; padding: 5px !important; }
    }
</style>
""", unsafe_allow_html=True)

# =======================================
# 5. HỆ THỐNG ĐĂNG NHẬP BẢO MẬT
# =======================================
if 'dang_nhap' not in st.session_state: st.session_state.dang_nhap = False
if not st.session_state.dang_nhap:
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<h2 style='text-align: center; color: #00C9FF; margin-top: 50px;'>💎 ĐĂNG NHẬP JBLMONEY</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Nhập mã PIN bảo mật (1234)", type="password")
        if st.button("🚀 Đăng Nhập", use_container_width=True):
            if pwd == "1234":
                st.session_state.dang_nhap = True
                st.rerun()
            else: st.error("Sai mã PIN!")
    st.stop()

# =======================================
# 6. SIDEBAR ĐIỀU KHIỂN & TRỢ LÝ AI GỐC
# =======================================
tong_thu_all = df[df['Loại'] == 'Thu nhập']['Số tiền (VNĐ)'].sum()
tong_chi_all = df[df['Loại'] == 'Chi tiêu']['Số tiền (VNĐ)'].sum()
so_du_all = tong_thu_all - tong_chi_all

with st.sidebar:
    st.markdown("### 💎 Menu Điều Khiển")
    if st.button("Đăng xuất"): 
        st.session_state.dang_nhap = False; st.rerun()
    
    st.markdown("---")
    thang_loc = st.selectbox("📅 Chọn Tháng Xem Báo Cáo", range(1, 13), index=int(datetime.now().month-1))
    
    st.markdown("---")
    st.markdown("### 🤖 Trợ lý AI Cấp cao")
    chat_box = st.container(height=350, border=True)
    if "chat" not in st.session_state: st.session_state.chat = [{"role": "assistant", "content": "Hệ thống sẵn sàng! Boss cần kiểm tra gì?"}]
    for msg in st.session_state.chat: chat_box.chat_message(msg["role"]).write(msg["content"])
    
    if q := st.chat_input("Hỏi AI..."):
        st.session_state.chat.append({"role": "user", "content": q})
        chat_box.chat_message("user").write(q)
        try:
            ans = bo_nao_ai.generate_content(f"Dữ liệu tổng: Thu {tong_thu_all}, Chi {tong_chi_all}, Dư {so_du_all}. Trả lời câu hỏi: {q}")
            chat_box.chat_message("assistant").write(ans.text)
            st.session_state.chat.append({"role": "assistant", "content": ans.text})
        except Exception as e: 
            st.error(f"Lỗi AI: Vui lòng kiểm tra lại mã API Key! ({e})")

# =======================================
# 7. MÀN HÌ
