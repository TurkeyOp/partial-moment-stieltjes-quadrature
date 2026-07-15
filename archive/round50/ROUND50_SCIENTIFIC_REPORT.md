# ROUND 50 SCIENTIFIC REPORT

## 1. Kết luận điều hành

Round 50 đã hoàn thành thành công cho cả sáu bài toán upper-half:

| `(n,k)` | Unknowns = equations | Internal extrema | Krawczyk verdict | Global level verdict |
|---|---:|---:|---|---|
| `(2,3)` | 5 | 0 | Certified | Certified |
| `(3,4)` | 8 | 1 | Certified | Certified |
| `(3,5)` | 7 | 0 | Certified | Certified |
| `(4,5)` | 11 | 2 | Certified | Certified |
| `(4,6)` | 10 | 1 | Certified | Certified |
| `(4,7)` | 9 | 0 | Certified | Certified |

Kết quả mạnh nhất của round này không còn là “floating-point solution có residual nhỏ”. Với mỗi hệ, certificate chứng minh có đúng một nghiệm chính xác của hệ vuông fixed-sign trong một box bán kính tuyệt đối `1e-12` quanh tâm độ chính xác cao.

Một audit interval thứ hai chứng minh dấu của đạo hàm trên các khoảng giữa các extrema và dấu của đạo hàm bậc hai quanh extrema nội. Vì vậy mức xen kẽ `E` là chuẩn sai số tương đối đều toàn cục trên `b in [0.08,0.12]`, không chỉ là giá trị tại một số điểm lấy mẫu.

## 2. Source of truth đã dùng

Các tâm ban đầu và dấu xen kẽ được lấy trực tiếp từ:

- `data/round43_full_hierarchy_nodes_weights.csv`;
- `data/round43_full_hierarchy_alternation.csv`.

Các file Round 45 chỉ được dùng để đối chiếu sensitivity, không được xem là independent implementation hoặc formal certificate.

## 3. Audit hệ vuông

Đặt `d = 2n-k`. Hệ dùng:

- `k` moment equations;
- `d+1` equal-error equations tại hai endpoint và các extrema nội;
- `d-1` stationarity equations.

Số unknowns và equations đều bằng `4n-k`. Audit chi tiết nằm trong `results/round50_system_audit.csv`.

Unknown vector gồm squared nodes `y_j`, pair weights `w_j`, các internal widths `b_i`, và minimax level `E`.

## 4. Audit analytic Jacobian

Jacobian analytic được kiểm tra độc lập ở mức số học độ chính xác cao bằng đạo hàm số của từng component. Sai khác scaled lớn nhất trong sáu bài toán là khoảng `1.37e-99`. Tất cả verdict trong `results/round50_jacobian_audit.csv` đều là `PASS`.

Audit này kiểm tra tính đúng của công thức Jacobian; nó không thay thế interval proof.

## 5. Krawczyk certificate

Cấu hình:

- Newton center: 180 decimal digits;
- interval backend: Python-Flint/Arb;
- Arb precision: 180 decimal digits;
- coordinate box radius: `1e-12`;
- point preconditioner: numerical inverse của Jacobian tại tâm.

Các upper bounds của `||I-YJ(X)||_infinity` nằm từ `1.74e-9` đến `5.83e-7`, đều nhỏ hơn 1 rất xa. Minimum componentwise inclusion margin của từng bài toán xấp xỉ `1e-12` và dương nghiêm ngặt.

Do đó:

1. `K(z0,X)` nằm nghiêm ngặt trong interior của `X`;
2. tồn tại một exact zero trong `X`;
3. exact zero đó là duy nhất trong box;
4. interval Jacobian không suy biến trên box theo Neumann bound;
5. box giữ node ordering, positive weights, ordered internal extrema và `E>0`.

Chi tiết nằm trong:

- `results/round50_certificate.json`;
- `results/round50_certificate_summary.csv`;
- `results/round50_verified_boxes.csv`;
- `results/round50_residual_intervals.csv`.

## 6. Global alternation/minimax-level audit

Krawczyk proof một mình chỉ chứng minh nghiệm của hệ. Để đóng điều kiện `E = ||epsilon||_infinity`, Round 50 thực hiện thêm:

- interval proof cho dấu của `epsilon_b` trên các khoảng nằm giữa các extremum neighborhoods;
- interval proof cho dấu của `epsilon_bb` trên neighborhood bán kính `1e-5` quanh mỗi internal extremum;
- adaptive subdivision khi natural interval extension chưa đủ hẹp.

Bài toán khó nhất là `(4,5)`, với 6697 interval subproblems được thăm. Minimum signed derivative margin vẫn dương (`7.55e-8`) và minimum curvature margin là khoảng `3.39`.

Kết hợp với các equal-error và stationarity equations đúng tại exact root, điều này chứng minh toàn bộ error curve đơn điệu đúng hướng giữa các extrema và không vượt quá `E`. Vì vậy sáu exact rules thỏa điều kiện alternation toàn cục của theorem hiện hành.

Chi tiết nằm trong:

- `results/round50_global_minimax_audit.json`;
- `results/round50_global_minimax_summary.csv`;
- `results/round50_monotonicity_segments.csv`;
- `results/round50_curvature_neighborhoods.csv`.

## 7. Phạm vi claim được phép

Sau Round 50 có thể phát biểu:

- tồn tại duy nhất một exact zero của fixed-sign square system trong từng certified box;
- sáu upper-half rules có ordered positive realization;
- mức xen kẽ là global uniform relative-error norm trên structural interval;
- theo alternation theorem, không có strictly better competitor trong `A_{n,k}`.

Không được suy ra:

- global uniqueness giữa mọi equal-norm minimizers;
- uniqueness ngoài certified boxes;
- independent replication;
- interval root certificate cho lower-half rules;
- universal superiority hoặc global novelty.

## 8. Manuscript Version 2.4

Manuscript Version 2.4 đã được biên dịch thành công, gồm 25 trang, không có undefined citations/references và không có overfull boxes trong final compile log.

Bản mới thêm một section riêng về:

- reconstructed square systems;
- Krawczyk operator;
- bảng certificate;
- global derivative/curvature audit;
- computer-assisted proposition và proof;
- limitations được cập nhật đúng phạm vi.

## 9. Trạng thái Round 50

**ROUND 50: COMPLETED.**

Không có problem nào cần failure report kỹ thuật. File `results/round50_failure_diagnostics.csv` ghi rõ `None` cho cả sáu bài toán.

Blocker khoa học còn lại chuyển sang Round 51:

- independent reproduction path;
- repository-wide one-command regression;
- dependency lock và clean-environment audit;
- đối chiếu tự động mọi số manuscript với generated artifacts.
