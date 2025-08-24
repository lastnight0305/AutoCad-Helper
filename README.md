# AutoCAD Helper

Ứng dụng hỗ trợ hiển thị các lệnh AutoCAD thông dụng.

## Tính năng

- Hiển thị danh sách lệnh AutoCAD phổ biến theo từng nhóm
- Giao diện trong suốt, luôn hiển thị trên cùng
- Hỗ trợ phím tắt để điều hướng
- Tùy chỉnh:
  - Theme sáng/tối
  - Độ trong suốt
  - Cỡ chữ
  - Số dòng hiển thị mỗi trang
  - Phím tắt điều hướng
- Tự động khởi động cùng Windows

## Yêu cầu

- Windows 10/11
- Python 3.7 trở lên
- Các thư viện: tkinter, keyboard, pywin32, winshell

## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/lastnight0305/AutoCad-Helper.git
cd AutoCad-Helper
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

4. Chạy ứng dụng:
```bash
python main.py
```

## Hướng dẫn sử dụng

1. **Điều hướng**:
   - Sử dụng chuột hoặc phím tắt (mặc định: Ctrl+Left/Right) để chuyển trang
   - Click chuột phải để mở menu cài đặt

2. **Cài đặt**:
   - Theme: Chọn giao diện sáng hoặc tối
   - Độ trong suốt: Điều chỉnh độ trong suốt của cửa sổ
   - Cỡ chữ: Thay đổi kích thước chữ
   - Số dòng: Điều chỉnh số lệnh hiển thị trên mỗi trang
   - Phím tắt: Tùy chỉnh phím tắt điều hướng

3. **Tự động khởi động**:
   - Click chuột phải và chọn "Tự động khởi động" để bật/tắt

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo issue hoặc pull request.

## Giấy phép

MIT License - Xem file [LICENSE](LICENSE) để biết thêm chi tiết.
