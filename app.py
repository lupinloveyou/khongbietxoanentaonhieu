import streamlit as st
import zipfile
import io

st.title("🔎 Multi Account Extractor (Web Version)")
st.write("Upload file `.txt` dạng `url:tk:mk` và nhập từ khóa để lọc. Kết quả sẽ xuất ra `tk:mk` (loại trùng).")

# Upload file
uploaded_file = st.file_uploader("📂 Chọn file .txt", type=["txt"])
# Input từ khóa
keywords_input = st.text_input("🔑 Nhập từ khóa (cách nhau bởi dấu phẩy)", "garena,roblox,epicgames")

if uploaded_file and keywords_input:
    keywords = [k.strip().lower() for k in keywords_input.split(",") if k.strip()]
    if st.button("🚀 Bắt đầu lọc"):
        lines = uploaded_file.getvalue().decode("utf-8", errors="ignore").splitlines()
        total_lines = len(lines)
        st.write(f"📊 Tổng số dòng: {total_lines:,}")

        # Chuẩn bị kết quả
        results = {k: set() for k in keywords}

        # Xử lý từng dòng
        for idx, line in enumerate(lines, start=1):
            line = line.strip().lower()
            for kw in keywords:
                if kw in line:
                    parts = line.split(":")
                    if len(parts) >= 3:
                        tk = parts[-2]
                        mk = parts[-1]
                        results[kw].add(f"{tk}:{mk}")
                    break  # 1 dòng chỉ lưu vào 1 keyword

            # Hiển thị tiến trình %
            if idx % max(1, total_lines // 100) == 0:
                percent = (idx / total_lines) * 100
                st.progress(int(percent))

        # Hiển thị kết quả
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for kw in keywords:
                accounts = sorted(results[kw])
                st.subheader(f"📌 {kw} ({len(accounts):,} dòng)")
                if accounts:
                    # Nút tải riêng
                    st.download_button(
                        label=f"⬇️ Tải {kw}_accounts.txt",
                        data="\n".join(accounts),
                        file_name=f"{kw}_accounts.txt",
                        mime="text/plain",
                    )
                    # Thêm vào ZIP
                    zip_file.writestr(f"{kw}_accounts.txt", "\n".join(accounts))
                else:
                    st.info(f"⚠️ Không tìm thấy tài khoản cho {kw}")
        zip_buffer.seek(0)

        # Nút tải tất cả (ZIP)
        if any(results[kw] for kw in keywords):
            st.download_button(
                label="📦 Tải tất cả kết quả (ZIP)",
                data=zip_buffer,
                file_name="all_accounts.zip",
                mime="application/zip",
            )
