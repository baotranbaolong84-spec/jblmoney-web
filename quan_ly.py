import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import time
from datetime import datetime

# =======================================
# 1. CẤU HÌNH BỘ NÃO AI GEMINI
# =======================================
# ⚠️ BOSS NHỚ DÁN LẠI MÃ "AQ..." VÀO ĐÂY NHÉ:
genai.configure(api_key="AQ.Ab8RN6KskRvN83YreVDYYG8bM0ThevqFgl40qKKT4r8OFTIIUw")
bo_nao_ai = genai.GenerativeModel('gemini-2.5-flash')

# =======================================
# 2. CẤU HÌNH KHO DỮ LIỆU & ẢNH HÓA ĐƠN
# =======================================
FILE_DATA = 'C:/Users/tranb/OneDrive/so_thu_chi.csv'
THU_MUC_ANH = 'C:/Users/tranb/OneDrive/Hoa_Don'

# Tự động tạo thư mục nếu chưa có
if not os.path.exists(THU_MUC_ANH): 
    os.makedirs(THU_MUC_ANH)

def tai_du_lieu():
    if os.path.exists(FILE_DATA):
        df = pd.read_csv(FILE_DATA)
        # Bổ sung các cột nếu sổ cũ bị thiếu
        if 'Ví' not in df.columns: df['Ví'] = 'Tiền mặt'
        if 'Hóa đơn' not in df.columns: df['Hóa đơn'] = 'Không có'
        return df
    else:
        return pd.DataFrame(columns=['Ngày', 'Loại', 'Danh mục', 'Ví', 'Số tiền (VNĐ)', 'Ghi chú', 'Hóa đơn'])

df = tai_du_lieu()
df['Tháng'] = pd.to_datetime(df['Ngày']).dt.month

st.set_page_config(page_title="JBLMONEY - Boss Long", page_icon="🔥", layout="wide")

# =======================================
# 3. CỔNG ĐĂNG NHẬP (BẢO MẬT)
# =======================================
if 'dang_nhap_thanh_cong' not in st.session_state: 
    st.session_state.dang_nhap_thanh_cong = False

if not st.session_state.dang_nhap_thanh_cong:
    st.markdown("<h1 style='text-align: center;'>🔐 CỔNG ĐĂNG NHẬP JBLMONEY</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        mat_khau = st.text_input("Nhập mã PIN bảo mật (Gợi ý: 1234)", type="password")
        if st.button("Đăng nhập vào Hệ thống", use_container_width=True):
            if mat_khau == "1234":
                st.session_state.dang_nhap_thanh_cong = True
                st.rerun()
            else: 
                st.error("Mã PIN sai! Boss nhập lại đi.")
    st.stop() # Dừng chạy code bên dưới nếu chưa đăng nhập

# =======================================
# 4. SIDEBAR - BỘ LỌC & AI TRỢ LÝ
# =======================================
tong_thu_all = df[df['Loại'] == 'Thu nhập']['Số tiền (VNĐ)'].sum() if not df.empty else 0
tong_chi_all = df[df['Loại'] == 'Chi tiêu']['Số tiền (VNĐ)'].sum() if not df.empty else 0
so_du_all = tong_thu_all - tong_chi_all

with st.sidebar:
    st.title("🔥 JBLMONEY ULTIMATE")
    if st.button("🚪 Đăng xuất"): 
        st.session_state.dang_nhap_thanh_cong = False
        st.rerun()
        
    st.markdown("---")
    thang_loc = st.selectbox("📅 Chọn Tháng Báo Cáo", range(1, 13), index=datetime.now().month-1)
    vi_loc = st.selectbox("💳 Lọc Theo Ví", ["Tất cả", "Tiền mặt", "Ngân hàng", "Thẻ Tín dụng"])
    
    st.markdown("---")
    st.header("🤖 Trợ Lý AI")
    cua_so_chat = st.container(height=350, border=True)
    if "lich_su_chat" not in st.session_state:
        st.session_state.lich_su_chat = [{"role": "assistant", "content": "Dạ em chào Boss! Em đã xem sổ sách rồi, Boss cần tư vấn gì ạ?"}]
        
    for tin_nhan in st.session_state.lich_su_chat:
        with cua_so_chat.chat_message(tin_nhan["role"]): 
            st.markdown(tin_nhan["content"])
            
    cau_hoi = st.chat_input("Hỏi AI (VD: Tôi đang dư bao nhiêu?)...")
    if cau_hoi:
        st.session_state.lich_su_chat.append({"role": "user", "content": cau_hoi})
        with cua_so_chat.chat_message("user"): 
            st.markdown(cau_hoi)
        with cua_so_chat.chat_message("assistant"):
            try:
                bo_canh = f"DỮ LIỆU HIỆN TẠI: Tổng thu: {tong_thu_all}đ, Tổng chi: {tong_chi_all}đ, Số dư tổng: {so_du_all}đ."
                tra_loi = bo_nao_ai.generate_content(f"Bạn là AI của Boss Long trên App JBLMONEY. {bo_canh} Trả lời: {cau_hoi}")
                st.markdown(tra_loi.text)
                st.session_state.lich_su_chat.append({"role": "assistant", "content": tra_loi.text})
            except Exception as e: 
                st.error("Lỗi AI. Boss nhớ dán API Key vào dòng 12 nhé!")

# =======================================
# 5. MÀN HÌNH CHÍNH & KPI THỐNG KÊ
# =======================================
df_loc = df[df['Tháng'] == thang_loc]
if vi_loc != "Tất cả": 
    df_loc = df_loc[df_loc['Ví'] == vi_loc]

st.title(f"📊 Bảng Điều Khiển - Tháng {thang_loc}")

tong_thu = df_loc[df_loc['Loại'] == 'Thu nhập']['Số tiền (VNĐ)'].sum() if not df_loc.empty else 0
tong_chi = df_loc[df_loc['Loại'] == 'Chi tiêu']['Số tiền (VNĐ)'].sum() if not df_loc.empty else 0

c1, c2, c3 = st.columns(3)
c1.metric("💰 SỐ DƯ KÉT (Tháng này)", f"{tong_thu - tong_chi:,.0f} đ", delta="An toàn" if (tong_thu - tong_chi) >= 0 else "Báo động!", delta_color="normal")
c2.metric("🟢 Tổng Thu Nhập", f"{tong_thu:,.0f} đ")
c3.metric("🔴 Tổng Chi Tiêu", f"{tong_chi:,.0f} đ")
st.markdown("---")

# CHIA 5 TABS CHỨC NĂNG
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Ghi Chép", "💣 Ngân Sách", "📈 Phân Tích & AI", "🧮 Tiện Ích", "📋 Sổ Excel (Sửa/Xóa)"])

# --- TAB 1: NHẬP LIỆU ---
with tab1:
    with st.form("form_nhap", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            loai_gd = st.radio("Loại", ["Chi tiêu", "Thu nhập"], horizontal=True)
            ngay = st.date_input("Ngày giao dịch")
            danh_muc = st.text_input("Danh mục (Ví dụ: Ăn uống, Mua sắm...)")
        with col2:
            so_tien = st.number_input("Số tiền (VNĐ)", min_value=0, step=50000)
            vi_tien = st.selectbox("Ví", ["Tiền mặt", "Ngân hàng", "Thẻ Tín dụng"])
            ghi_chu = st.text_input("Ghi chú")
        
        file_anh = st.file_uploader("📸 Tải ảnh Giấy thanh toán / Hóa đơn (Tùy chọn)", type=["jpg", "png"])
        if st.form_submit_button("Lưu Giao Dịch 💾", use_container_width=True):
            ten_file = "Không có"
            if file_anh:
                ten_file = f"bill_{int(time.time())}.png"
                with open(os.path.join(THU_MUC_ANH, ten_file), "wb") as f: 
                    f.write(file_anh.getbuffer())
            
            dl_moi = pd.DataFrame([{'Ngày': str(ngay), 'Loại': loai_gd, 'Danh mục': danh_muc, 'Ví': vi_tien, 'Số tiền (VNĐ)': so_tien, 'Ghi chú': ghi_chu, 'Hóa đơn': ten_file}])
            df = pd.concat([df.drop(columns=['Tháng'], errors='ignore'), dl_moi], ignore_index=True)
            df.to_csv(FILE_DATA, index=False)
            st.success("Giao dịch đã được lưu vào két an toàn!")
            st.rerun()

# --- TAB 2: BOM NGÂN SÁCH ---
with tab2:
    han_muc = st.slider("Cài đặt hạn mức chi tiêu tháng này:", 1000000, 50000000, 10000000, step=1000000)
    phan_tram = (tong_chi / han_muc) * 100 if han_muc > 0 else 0
    st.progress(min(phan_tram / 100, 1.0))
    st.write(f"Đã tiêu: **{tong_chi:,.0f} đ** / Ngân sách: **{han_muc:,.0f} đ** ({phan_tram:.1f}%)")
    
    if phan_tram >= 100:
        if 'da_hua' not in st.session_state: st.session_state.da_hua = False
        if not st.session_state.da_hua:
            st.error("🚨 VƯỢT QUÁ CHI TIÊU! HỆ THỐNG CHUẨN BỊ NỔ TUNG!")
            st.image("https://media.giphy.com/media/HhTXt43pk1I1W/giphy.gif", width=300)
            if st.button("🛑 TÔI XIN HỨA SẼ KHÔNG TIÊU HOANG NỮA!", type="primary"):
                st.session_state.da_hua = True
                st.rerun()
            st.warning("⚠️ Nếu Boss không ấn nút trên, hệ thống sẽ từ chối hoạt động!")
        else:
            st.success("Tạm tha cho Boss lần này! Ráng ăn mì tôm tới cuối tháng đi nha!")
            st.image("https://media.giphy.com/media/ZfK4cXKJTTay1Ava29/giphy.gif", width=200)

# --- TAB 3: PHÂN TÍCH & AI BÓC PHỐT ---
with tab3:
    col_pt1, col_pt2 = st.columns([2, 1])
    with col_pt1:
        st.subheader("📈 Biểu đồ chi tiêu")
        if not df_loc[df_loc['Loại'] == 'Chi tiêu'].empty:
            st.bar_chart(df_loc[df_loc['Loại'] == 'Chi tiêu'].groupby('Danh mục')['Số tiền (VNĐ)'].sum().reset_index(), x='Danh mục', y='Số tiền (VNĐ)', color="#FF4B4B")
        else: 
            st.info("Chưa có dữ liệu để vẽ biểu đồ.")
            
    with col_pt2:
        st.subheader("🔮 AI Bóc Phốt")
        st.write("JBLMONEY sẽ 'tế' thói quen tiêu tiền của bạn!")
        if st.button("🔥 Bóc phốt tôi đi!", type="primary", use_container_width=True):
            with st.spinner("AI đang soi mói..."):
                try:
                    danh_sach_chi = df_loc[df_loc['Loại'] == 'Chi tiêu'][['Danh mục', 'Số tiền (VNĐ)']].to_string()
                    lenh = f"Boss Long đã tiêu: {danh_sach_chi}. Đóng vai chuyên gia tài chính cực đanh đá, dùng từ ngữ Gen Z châm biếm thói tiêu hoang này. Cấm khen!"
                    phot = bo_nao_ai.generate_content(lenh)
                    st.error(phot.text)
                except:
                    st.warning("Lỗi mạng hoặc chưa có chi tiêu để bóc phốt!")

# --- TAB 4: TIỆN ÍCH ---
with tab4:
    st.subheader("🍻 Máy Tính Chia Bill (Đi Nhậu/Cafe)")
    col_b1, col_b2 = st.columns(2)
    tong_bill = col_b1.number_input("Tổng tiền Bill (VNĐ):", min_value=0, step=10000)
    so_nguoi = col_b2.number_input("Số anh em tham gia:", min_value=1, step=1, value=1)
    if tong_bill > 0:
        st.success(f"👉 Mỗi người cần chuyển khoản: **{tong_bill / so_nguoi:,.0f} đ**")
    
    st.markdown("---")
    st.subheader("🐷 Ống Heo Mục Tiêu (Mua iPhone/Xe...)")
    tien_muc_tieu = st.number_input("Số tiền cần đạt được:", min_value=0, value=30000000, step=1000000)
    if tien_muc_tieu > 0:
        tien_tiet_kiem = max(tong_thu_all - tong_chi_all, 0) 
        phan_tram_hoan_thanh = (tien_tiet_kiem / tien_muc_tieu) * 100
        st.progress(min(phan_tram_hoan_thanh / 100, 1.0))
        st.write(f"Đã gom được: **{tien_tiet_kiem:,.0f} đ** / **{tien_muc_tieu:,.0f} đ** (Đạt {phan_tram_hoan_thanh:.1f}%)")

# --- TAB 5: SỔ EXCEL (SỬA & XÓA) ---
with tab5:
    st.subheader("📋 Quản lý sổ sách trực tiếp")
    st.info("💡 **Hướng dẫn:** Tick vào ô vuông ngoài cùng bên trái của dòng bị sai và bấm **Delete** để xóa. Nhấp đúp vào ô để sửa chữ. Sửa xong nhớ bấm nút Cập Nhật bên dưới!")
    
    df_hien_thi = df.copy().drop(columns=['Tháng'], errors='ignore')
    
    # Bảng dữ liệu chuẩn Excel
    df_da_sua = st.data_editor(df_hien_thi, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 Lưu thay đổi vào Két Sắt", type="primary"):
        df_da_sua.to_csv(FILE_DATA, index=False)
        st.success("Đã đồng bộ dữ liệu sửa/xóa thành công!")
        st.rerun()