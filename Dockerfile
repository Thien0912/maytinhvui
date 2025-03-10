# Sử dụng Python base image
FROM python:3.10-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy file yêu cầu vào container
COPY requirements.txt .

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Mở cổng cho container
EXPOSE 8000

# Chạy ứng dụng Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
