# Bản vá GitHub Actions cho v1.0.0-rc1

Bản vá sửa hai nguyên nhân khiến `Public package quick verification` thất bại:

1. `SHA256_MANIFEST.csv` trước đây dùng raw bytes nên CRLF/LF khác nhau giữa Windows và Ubuntu làm checksum sai.
2. `.gitignore` có mẫu `main.pdf`, khiến bốn PDF lịch sử trong `archive/round46`–`round49` không được Git theo dõi.

## Cách áp dụng

Copy **toàn bộ nội dung bên trong thư mục bản vá** vào thư mục repository local, chọn **Replace the files in the destination**.

Sau đó trong GitHub Desktop:

1. Kiểm tra vẫn ở branch `release-v1.0.0-rc1`.
2. Commit với summary: `Fix cross-platform manifest verification`.
3. Push origin.
4. Chờ GitHub Actions tự chạy lại trên Pull Request #1.

Không cần tạo Pull Request mới.
