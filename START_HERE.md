# START HERE — Hướng dẫn sử dụng project

## 1. File bài nghiên cứu hoàn chỉnh nằm ở đâu?

File dễ mở nhất:

```text
FINAL_PROJECT_PAPER.pdf
```

Bản gốc phục vụ submission nằm tại:

```text
paper/jcam/main.pdf
```

Mã nguồn LaTeX của bài báo:

```text
paper/jcam/main.tex
```

Bản Markdown dễ đọc và dễ chỉnh nội dung:

```text
paper/manuscript.md
```

## 2. Những file code chính dùng để làm gì?

### `run_all.py`

Đây là file chạy toàn bộ project bằng một lệnh.

Nó sẽ:

1. đọc nodes và weights trong `rules/published_n4_rules.json`;
2. tính lại moments;
3. tìm lại các điểm cực trị và alternation pattern;
4. tính centered Lorentzian errors;
5. tính structural errors;
6. tính Chebyshev transfer functions;
7. chạy selector spot checks;
8. kiểm tra shifted-Lorentzian family;
9. tạo lại bảng kết quả và hình;
10. chạy automated tests.

Chạy bằng:

```bash
python run_all.py
```

### `src/core.py`

Chứa các công thức toán học nền tảng:

- exact centered Lorentzian integral;
- quadrature response;
- relative và absolute errors;
- đạo hàm của error;
- tìm stationary points;
- Chebyshev defects;
- transfer function;
- exact shifted-Lorentzian integral.

### `src/reproduce.py`

Dùng các hàm trong `core.py` để:

- chạy toàn bộ phép tính;
- xuất các file CSV trong `results/`;
- tạo các hình trong `figures/`;
- tạo selector map;
- thực hiện shifted-family stress test.

### `tests/test_reproduction.py`

Kiểm tra tự động rằng:

- nodes và weights hợp lệ;
- alternation counts đúng;
- centered errors khớp kết quả đã đóng băng;
- structural errors nằm trong certified intervals;
- transfer functions được tái tạo;
- selector choices khớp;
- shifted-family test vẫn cho kết luận đúng.

### `rules/published_n4_rules.json`

Chứa các nodes và weights cuối cùng của năm rule:

```text
k = 0, 1, 2, 3, 4
```

Đây là đầu vào số quan trọng nhất của repository.

## 3. Các thư mục kết quả

### `results/`

Chứa các kết quả dạng bảng:

- `hierarchy_reproduction.csv`
- `moment_audit.csv`
- `alternation_points.csv`
- `structural_errors.csv`
- `transfer_functions.csv`
- `selector_spots.csv`
- `shifted_primary_box.csv`

### `figures/`

Chứa các hình được tạo lại từ code:

- hierarchy error;
- selector map;
- transfer functions;
- shifted-family comparison.

### `data/reference/`

Chứa frozen reference values chỉ dùng để đối chiếu sau khi code đã tính
xong. Code tính toán không lấy các giá trị này làm đáp án đầu vào.

## 4. Cách chạy trên Windows

Mở thư mục project bằng File Explorer.

Nhấn vào thanh địa chỉ, gõ:

```text
cmd
```

rồi Enter.

Sau đó chạy:

```bash
python -m pip install -r requirements.txt
python run_all.py
```

Nếu cuối màn hình hiện:

```text
Ran 7 tests
OK
Reproduction completed successfully.
```

thì project chạy đúng.

## 5. Cách đưa lên GitHub

1. Giải nén file ZIP.
2. Mở thư mục `partial-moment-stieltjes-quadrature`.
3. Tạo repository mới trên GitHub tên:

```text
partial-moment-stieltjes-quadrature
```

4. Không chọn tạo README, `.gitignore` hoặc license trên GitHub vì package
   đã có sẵn các file này.
5. Trong repository trống, chọn **uploading an existing file** hoặc
   **Add file → Upload files**.
6. Kéo toàn bộ file và thư mục bên trong project vào vùng upload.
7. Commit message:

```text
Initial research project release
```

8. Chọn **Commit changes**.

## 6. Chưa nên xóa các file nào?

Không xóa:

- `run_all.py`
- `src/`
- `tests/`
- `rules/`
- `data/reference/`
- `paper/`
- `requirements.txt`
- `CITATION.cff`
- `README.md`

## 7. File nào là bài project cuối cùng?

```text
FINAL_PROJECT_PAPER.pdf
```

Đây là file cần mở đầu tiên để đọc toàn bộ nghiên cứu.
