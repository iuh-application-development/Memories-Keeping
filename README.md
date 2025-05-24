# Memories-Keeping

## Mô tả đề tài
### Mô tả tổng quan

Trong cuộc sống hiện đại, nhu cầu lưu giữ và chia sẻ những khoảnh khắc ý nghĩa ngày càng trở nên thiết yếu. 

Tuy nhiên, việc quản lý và truy xuất các kỷ niệm (dưới dạng ảnh, văn bản) thường gặp khó khăn do thiếu công cụ hỗ trợ hiệu quả, thông minh và cá nhân hóa. Đề tài “Xây dựng ứng dụng website giúp mọi người lưu giữ kỷ niệm” ra đời nhằm giải quyết vấn đề đó bằng cách phát triển một nền tảng web thân thiện, hiện đại và tích hợp công nghệ AI.

Ý tưởng chính là xây dựng một hệ thống cho phép người dùng lưu trữ, tổ chức, tìm kiếm và tương tác với các kỷ niệm của mình thông qua hình ảnh và mô tả văn bản. Ứng dụng sử dụng mô hình học sâu OpenCLIP (ViT-L-14) để trích xuất đặc trưng từ ảnh và văn bản, kết hợp với FAISS nhằm tìm kiếm các ảnh tương đồng một cách nhanh chóng. Hệ thống còn hỗ trợ các tính năng cộng đồng như thích, bình luận, chia sẻ, đồng thời đảm bảo bảo mật với Knox token và hỗ trợ đăng nhập qua Google OAuth.

Lý do chọn đề tài xuất phát từ thực tiễn rằng hầu hết các nền tảng chia sẻ hiện nay đều thiên về mạng xã hội chung chung, thiếu đi khả năng tổ chức và truy xuất các kỷ niệm theo ngữ cảnh cá nhân hóa. Đề tài kỳ vọng sẽ góp phần lấp đầy khoảng trống này bằng một giải pháp vừa tiện ích vừa thông minh.

### Mục tiêu
Đề tài hướng đến các mục tiêu cụ thể sau:
- Xây dựng một nền tảng web cho phép người dùng lưu trữ, quản lý và chia sẻ các khoảnh khắc cá nhân một cách trực quan, hiệu quả.
- Tích hợp mô hình AI OpenCLIP để trích xuất đặc trưng ảnh và văn bản, đồng thời sử dụng FAISS cho tìm kiếm ảnh thông minh bằng văn bản hoặc ảnh tương tự.
- Phát triển giao diện người dùng thân thiện, hỗ trợ đầy đủ chức năng như quản lý ảnh, album, thùng rác, lịch sử tìm kiếm và tương tác cộng đồng (like, comment).
- Áp dụng các cơ chế xác thực bảo mật (Knox Token, OAuth 2.0), đảm bảo an toàn và quyền riêng tư cho người dùng.
- Xây dựng hệ thống phân quyền và quản trị nội dung giúp admin giám sát và điều phối nền tảng hiệu quả.


## Thông tin nhóm

- Trần Xuân Diện – MSSV: 22650601  
- Nguyễn Đăng Tuấn Huy – MSSV: 22658341

## Hướng dẫn cài đặt và chạy ứng dụng

### Yêu cầu hệ thống

- Python 3.8 hoặc cao hơn
- Git

### Cài đặt Backend

1. **Clone repository:**
```bash
git clone https://github.com/iuh-application-development/Memories-Keeping.git
cd Memories-Keeping/mori
```

2. **Tạo và kích hoạt môi trường ảo:**
```bash
python -m venv venv
# Trên Windows:
venv\Scripts\activate
# Trên Linux/Mac:
source venv/bin/activate
```

3. **Cài đặt các thư viện cần thiết:**
```bash
pip install -r requirements.txt
```

4. **Chạy migration:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Chạy server:**
```bash
python manage.py runserver
```

### Truy cập ứng dụng

Mở trình duyệt và truy cập:  
[http://localhost:8000](http://localhost:8000)

## Link video
- Link video sẽ được cập nhật trong thời gian tới.

## Screenshots
