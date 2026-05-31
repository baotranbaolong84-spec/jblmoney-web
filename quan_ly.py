import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import time
from datetime import datetime
import streamlit.components.v1 as components

# =======================================
# 1. CẤU HÌNH API AI GEMINI
# =======================================
# ⚠️ BOSS DÁN MÃ "AIza..." VÀO ĐÂY NHÉ:
genai.configure(api_key="AQ.Ab8RN6I-0Iv3yI3lz0K_TBT9W1Z09NIeHUvDdR5O_RKpr5iMaQ")
bo_nao_ai = genai.GenerativeModel('gemini-2.5-flash')

# =======================================
# 2. CẤU HÌNH KHO DỮ LIỆU & ẢNH HÓA ĐƠN
# =======================================
FILE_DATA = 'so_thu_chi.csv'
THU_MUC_ANH = 'Hoa_Don'
if not os.path.exists(THU_MUC_ANH): 
    os.makedirs(THU_MUC_ANH)

def tai_du_lieu():
    if os.path.exists(FILE_DATA):
        df = pd.read_csv(FILE_DATA)
        if 'Ví' not in df.columns: df['Ví'] = 'Tiền mặt'
        if 'Hóa đơn' not in df.columns: df['Hóa đơn'] = 'Không có'
        return df
    return pd.DataFrame(columns=['Ngày', 'Loại', 'Danh mục', 'Ví', 'Số tiền (VNĐ)', 'Ghi chú', 'Hóa đơn'])

df = tai_du_lieu()
df['Tháng'] = pd.to_datetime(df['Ngày']).dt.month

# ĐỔI THÀNH CENTERED ĐỂ HIỂN THỊ CÂN ĐỐI TRÊN ĐIỆN THOẠI
st.set_page_config(page_title="JBLMONEY Ultimate", page_icon="💎", layout="centered")

# =======================================
# 3. CSS TỐI ƯU HÓA RESPONSIVE CHO ĐIỆN THOẠI
# =======================================
st.markdown("""
<style>
    /* 1. Giao diện mặc định (Máy tính) */
    div[data-testid="metric-container"] {
        background-color: #1E1E2E; border-radius: 15px; padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); border: 1px solid #333;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%) !important;
        color: black !important; font-weight: bold !important; border-radius: 8px !important; border: none !important;
    }
    div.stButton > button:hover { opacity: 0.8; }
    div[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%) !important; color: white !important;
    }

    /* 2. MA THUẬT TỰ ĐỘNG THU NHỎ KHI LÊN ĐIỆN THOẠI (Mobile Responsive) */
    @media (max-width: 768px) {
        /* Thu nhỏ hộp số liệu (Metrics) */
        div[data-testid="metric-container"] {
            padding: 10px !important;
            margin-bottom: -15px !important; /* Ép các hộp gần nhau hơn */
        }
        /* Thu nhỏ chữ tiêu đề trong hộp */
        div[data-testid="metric-container"] label {
            font-size: 13px !important;
        }
        /* Thu nhỏ số tiền hiển thị */
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            font-size: 22px !important; 
        }
        /* Căn giữa tiêu đề trang */
        h1 {
            font-size: 24px !important;
            text-align: center !important;
            margin-top: -20px !important;
        }
        /* Chỉnh lại Tab trên điện thoại cho gọn */
        div[data-testid="stTabs"] button {
            font-size: 13px !important;
            padding-left: 10px !important;
            padding-right: 10px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# =======================================
# 4. HỆ THỐNG ĐĂNG NHẬP BẢO MẬT
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
# 5. SIDEBAR ĐIỀU KHIỂN & TRỢ LÝ AI
# =======================================
tong_thu_all = df[df['Loại'] == 'Thu nhập']['Số tiền (VNĐ)'].sum() if not df.empty else 0
tong_chi_all = df[df['Loại'] == 'Chi tiêu']['Số tiền (VNĐ)'].sum() if not df.empty else 0
so_du_all = tong_thu_all - tong_chi_all

with st.sidebar:
    st.markdown("### 💎 Menu Điều Khiển")
    if st.button("Đăng xuất"): 
        st.session_state.dang_nhap = False; st.rerun()
    
    st.markdown("---")
    thang_loc = st.selectbox("📅 Chọn Tháng Xem Báo Cáo", range(1, 13), index=datetime.now().month-1)
    
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
            st.error(f"Lỗi AI: {e}") # Bắt lỗi AI rõ ràng để dễ sửa

# =======================================
# 6. MÀN HÌNH CHÍNH & KPI SỐ LIỆU
# =======================================
df_loc = df[df['Tháng'] == thang_loc]
tong_thu = df_loc[df_loc['Loại'] == 'Thu nhập']['Số tiền (VNĐ)'].sum() if not df_loc.empty else 0
tong_chi = df_loc[df_loc['Loại'] == 'Chi tiêu']['Số tiền (VNĐ)'].sum() if not df_loc.empty else 0

st.markdown(f"<h1>📊 Báo cáo Tháng {thang_loc}</h1>", unsafe_allow_html=True)

# Hiển thị 3 hộp số liệu
c1, c2, c3 = st.columns(3)
c1.metric("💰 SỐ DƯ TÀI KHOẢN", f"{tong_thu - tong_chi:,.0f} ₫", "An toàn" if (tong_thu - tong_chi) >= 0 else "Báo động")
c2.metric("🟢 DÒNG TIỀN VÀO (THU)", f"{tong_thu:,.0f} ₫")
c3.metric("🔴 DÒNG TIỀN RA (CHI)", f"{tong_chi:,.0f} ₫")
st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 GHI CHÉP", "💣 NGÂN SÁCH", "📈 AI PHÂN TÍCH", "🧮 TIỆN ÍCH", "📋 SỔ EXCEL"])

# --- TAB 1: NHẬP LIỆU ---
with tab1:
    st.subheader("📝 Thêm giao dịch mới vào sổ")
    with st.form("form_nhap_du_lieu", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            loai = st.radio("Loại", ["Chi tiêu", "Thu nhập"], horizontal=True)
            ngay = st.date_input("Ngày")
            danh_muc = st.text_input("Danh mục (Ăn uống, Di chuyển...)")
        with col2:
            tien = st.number_input("Số tiền (VNĐ)", min_value=0, step=50000)
            vi_tien = st.selectbox("Ví sử dụng", ["Tiền mặt", "Ngân hàng", "Thẻ Tín dụng"])
            ghi_chu = st.text_input("Ghi chú")
        
        file_anh = st.file_uploader("📸 Tải ảnh Giấy thanh toán / Hóa đơn đính kèm", type=["jpg", "png"])
        if st.form_submit_button("LƯU VÀO HỆ THỐNG", use_container_width=True):
            ten_file = "Không có"
            if file_anh:
                ten_file = f"bill_{int(time.time())}.png"
                with open(os.path.join(THU_MUC_ANH, ten_file), "wb") as f: f.write(file_anh.getbuffer())
            
            dl_moi = pd.DataFrame([{'Ngày': str(ngay), 'Loại': loai, 'Danh mục': danh_muc, 'Ví': vi_tien, 'Số tiền (VNĐ)': tien, 'Ghi chú': ghi_chu, 'Hóa đơn': ten_file}])
            df = pd.concat([df.drop(columns=['Tháng'], errors='ignore'), dl_moi], ignore_index=True)
            df.to_csv(FILE_DATA, index=False)
            st.success("Lưu thành công!")
            st.rerun()

# --- TAB 2: QUẢ BOM ĐẾM NGƯỢC ---
with tab2:
    st.subheader("💣 Kiểm soát rủi ro ngân sách")
    han_muc = st.slider("Đặt hạn mức chi tiêu tháng này:", 1000000, 50000000, 10000000, step=1000000)
    phan_tram = (tong_chi / han_muc) * 100 if han_muc > 0 else 0
    st.progress(min(phan_tram / 100, 1.0))
    st.write(f"Đã tiêu: **{tong_chi:,.0f} ₫** / **{han_muc:,.0f} ₫** ({phan_tram:.1f}%)")
    
    if tong_chi > han_muc:
        st.error("🚨 CẢNH BÁO ĐỎ: BẠN ĐÃ TIÊU VƯỢT HẠN MỨC CHO PHÉP!")
        countdown_html = """
        <div style="text-align: center; background-color: #ff4b4b; padding: 20px; border-radius: 10px; color: white;">
            <h1 style="margin:0; font-size: 24px;">💣 BOM NỔ SAU: <span id="timer">15</span>S</h1>
        </div>
        <script>
            var timeLeft = 15;
            var timerId = setInterval(countdown, 1000);
            function countdown() {
                if (timeLeft == -1) {
                    clearTimeout(timerId);
                    document.getElementById('timer').innerHTML = "BÙM!!! BẠN ĐÃ PHÁ SẢN!";
                    document.body.style.backgroundColor = "#5a0000";
                } else {
                    document.getElementById('timer').innerHTML = timeLeft;
                    timeLeft--;
                }
            }
        </script>
        """
        components.html(countdown_html, height=120)
        if st.button("🛑 TÔI XIN HỨA SẼ THẮT LƯNG BUỘC BỤNG!"):
            st.success("Hệ thống đã ghi nhận lời hứa!")

# --- TAB 3: PHÂN TÍCH BIỂU ĐỒ & BÓC PHỐT ---
with tab3:
    st.subheader("📈 Biểu đồ cơ cấu chi tiêu")
    if not df_loc[df_loc['Loại'] == 'Chi tiêu'].empty:
        st.bar_chart(df_loc[df_loc['Loại'] == 'Chi tiêu'].groupby('Danh mục')['Số tiền (VNĐ)'].sum().reset_index(), x='Danh mục', y='Số tiền (VNĐ)', color="#00C9FF")
    else: st.info("Chưa có dữ liệu chi tiêu tháng này.")
        
    st.markdown("---")
    st.subheader("🔮 Chế độ: AI Bóc Phốt")
    if st.button("🔥 Soi mói thói quen xài tiền của tôi!", type="primary", use_container_width=True):
        with st.spinner("Đang soi sổ sách..."):
            try:
                ds_chi = df_loc[df_loc['Loại'] == 'Chi tiêu'][['Danh mục', 'Số tiền (VNĐ)']].to_string()
                lenh = f"Boss đã tiêu: {ds_chi}. Hãy đóng vai một chuyên gia tài chính đanh đá, dùng từ ngữ mỉa mai, châm biếm thói tiêu hoang này cho vui. Cấm khen!"
                phot = bo_nao_ai.generate_content(lenh)
                st.error(phot.text)
            except: st.warning("Ví sạch quá chưa có gì để bóc phốt Boss ơi!")

# --- TAB 4: CHIA BILL & ỐNG HEO ---
with tab4:
    st.subheader("🍻 Máy Tính Chia Bill")
    col_b1, col_b2 = st.columns(2)
    tong_bill = col_b1.number_input("Tổng hóa đơn (VNĐ):", min_value=0, step=20000)
    so_nguoi = col_b2.number_input("Số người chia tiền:", min_value=1, step=1, value=1)
    if tong_bill > 0: 
        st.success(f"👉 Campuchia đều: **{tong_bill / so_nguoi:,.0f} ₫ / người**")
    
    st.markdown("---")
    st.subheader("🐷 Ống Heo Tích Lũy")
    tien_muc_tieu = st.number_input("Mục tiêu cần đạt (VNĐ):", min_value=1, value=30000000, step=1000000)
    tien_tiet_kiem = max(float(tong_thu_all - tong_chi_all), 0.0) 
    phan_tram = (tien_tiet_kiem / float(tien_muc_tieu)) * 100.0
    st.progress(float(max(0.0, min(phan_tram / 100.0, 1.0))))
    st.write(f"Đã gom: **{tien_tiet_kiem:,.0f} ₫** / **{tien_muc_tieu:,.0f} ₫** (Đạt {phan_tram:.1f}%)")

# --- TAB 5: SỔ CÁI EXCEL ---
with tab5:
    st.subheader("📋 Bảng quản lý dữ liệu gốc")
    st.info("Nhấp đúp vào ô để sửa. Chọn ô đầu dòng bấm Delete để xóa dòng.")
    df_hien_thi = df.copy().drop(columns=['Tháng'], errors='ignore')
    df_da_sua = st.data_editor(df_hien_thi, num_rows="dynamic", use_container_width=True)
    if st.button("💾 LƯU MỌI THAY ĐỔI VÀO SỔ CÁI", use_container_width=True, type="primary"):
        df_da_sua.to_csv(FILE_DATA, index=False)
        st.success("Đã cập nhật cơ sở dữ liệu thành công!")
        st.rerun()
