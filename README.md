Tự động mở nhiều cửa sổ trình duyệt (song song bằng luồng — threads) và đăng ký nhiều tài khoản Instagram bằng email tạm thời.

Quy trình chính trong hàm create_account()

1. Khởi tạo Chrome với proxy (nếu có).

2.Đặt vị trí cửa sổ theo index để không đè nhau trên màn hình.

3.Truy cập trang đăng ký Instagram.

4.Điền form đăng ký:

Email
Họ tên
Tên người dùng
Mật khẩu

Chọn ngày sinh ngẫu nhiên.

5.Nhấn tiếp tục → Instagram gửi mã xác thực đến email.

6.Gọi API lấy mã xác thực.

7.Điền mã vào form xác minh.

8.Nếu thành công → lưu lại tài khoản.

9.Nếu thất bại (không lấy được mã) → tự động thử lại tạo nick mới.
<img width="1919" height="1149" alt="ảnh" src="https://github.com/user-attachments/assets/4de86bf5-5688-495b-a513-b3619ba0046f" />

Định dạng
Tài khoản | mật khẩu | năm sinh | mail | thời gian tạo acc thành công 
<img width="844" height="90" alt="ảnh" src="https://github.com/user-attachments/assets/4e01f2f1-2b37-45e3-9cff-33dc43c88f35" />


DONE BY NGUYEN THANH VINH !
