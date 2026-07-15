# Hướng dẫn upload repository lên GitHub

## Lưu ý quan trọng

GitHub **không tự giải nén ZIP khi em upload ZIP vào phần code của repository**. Vì vậy:

- để đưa mã nguồn lên repository: giải nén ZIP rồi upload/push **toàn bộ nội dung bên trong thư mục**;
- để lưu ZIP nguyên vẹn cho người khác tải: upload ZIP đó ở mục **Releases** sau khi repository đã được cập nhật.

## Cách khuyến nghị: GitHub Desktop

Cách này phù hợp nhất vì repository có nhiều file.

### A. Cập nhật repository đang có

Repository dự kiến:

```text
https://github.com/TurkeyOp/partial-moment-stieltjes-quadrature
```

1. Cài và đăng nhập **GitHub Desktop**.
2. Trên GitHub Desktop, chọn **File → Clone repository**.
3. Chọn repository `partial-moment-stieltjes-quadrature` và clone về máy.
4. Tạo nhánh mới: **Branch → New branch**, đặt tên:

   ```text
   release-v1.0.0-rc1
   ```

5. Giải nén file ZIP GitHub-ready.
6. Mở thư mục repository đã clone bằng File Explorer.
7. Sao lưu thư mục cũ nếu cần.
8. Xóa các file dự án cũ trong thư mục clone, nhưng **không xóa thư mục ẩn `.git`**.
9. Copy **toàn bộ nội dung bên trong** thư mục `partial-moment-stieltjes-quadrature` vừa giải nén vào thư mục clone.
10. Quay lại GitHub Desktop; kiểm tra danh sách file thay đổi.
11. Ở ô Summary, nhập:

    ```text
    Publish v1.0.0-rc1 reproducibility repository
    ```

12. Nhấn **Commit to release-v1.0.0-rc1**.
13. Nhấn **Push origin**.
14. Mở GitHub, tạo Pull Request từ `release-v1.0.0-rc1` vào `main`.
15. Kiểm tra GitHub Actions có hiện dấu xanh trước khi merge.

### B. Tạo repository mới

1. Giải nén ZIP.
2. Mở GitHub Desktop → **File → Add local repository**.
3. Chọn thư mục `partial-moment-stieltjes-quadrature`.
4. Nếu GitHub Desktop báo thư mục chưa phải Git repository, chọn **Create a repository**.
5. Nhấn **Publish repository**.
6. Đặt repository là **Public** khi em đã sẵn sàng công khai.

## Kiểm tra sau khi upload

Trang chính GitHub phải hiển thị ít nhất:

```text
README.md
LICENSE
CITATION.cff
requirements-lock.txt
paper/
src/
certificates/
data/
results/
```

Sau đó kiểm tra:

1. GitHub nhận diện nhãn **MIT license**.
2. `README.md` hiển thị đúng.
3. Tab **Actions** chạy `Public package quick verification` và có dấu xanh.
4. File manuscript mở được tại:

   ```text
   paper/current/MANUSCRIPT_VERSION_2_5.pdf
   ```

5. Không có thư mục `submission/`, cover letter hoặc số điện thoại cá nhân.

## Tạo Release

Sau khi merge vào `main`:

1. Vào trang repository → **Releases** → **Draft a new release**.
2. Tạo tag:

   ```text
   v1.0.0-rc1
   ```

3. Release title:

   ```text
   Model-Aware Positive Stieltjes Quadrature v1.0.0-rc1
   ```

4. Dán nội dung từ `RELEASE_NOTES_v1.0.0-rc1.md`.
5. Upload chính file ZIP GitHub-ready làm release asset.
6. Chọn **Set as a pre-release**, vì đây là release candidate trước khi có DOI/submission freeze cuối.
7. Nhấn **Publish release**.
