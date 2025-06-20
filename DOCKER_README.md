# CVE Tools Flask - Docker Deployment Guide

## 📋 Tổng quan

Project này đã được containerized với Docker để dễ dàng triển khai và chạy. Bao gồm:

- **Flask Application**: Ứng dụng web chính
- **MySQL Database**: Cơ sở dữ liệu
- **Nginx**: Reverse proxy và static file server

## 🔧 Yêu cầu hệ thống

- Docker Desktop (Windows/Mac) hoặc Docker Engine (Linux)
- Docker Compose
- Ít nhất 2GB RAM trống
- Port 80, 5000, 3306 chưa được sử dụng

## 🚀 Cách chạy

### Option 1: Sử dụng Docker Compose (Khuyến nghị)

```powershell
# Chạy script PowerShell (Windows)
.\build_and_run.ps1

# Hoặc chạy trực tiếp
docker-compose up -d
```

```bash
# Chạy script Bash (Linux/Mac)
./build_and_run.sh

# Hoặc chạy trực tiếp
docker-compose up -d
```

### Option 2: Chạy standalone container

```powershell
# Windows
.\build_and_run.ps1 -Standalone
```

```bash
# Linux/Mac
./build_and_run.sh --standalone
```

### Option 3: Build image only

```powershell
# Windows
.\build_and_run.ps1 -BuildOnly
```

```bash
# Linux/Mac
./build_and_run.sh --build-only
```

## 🌐 Truy cập ứng dụng

Sau khi chạy thành công:

- **Ứng dụng Flask**: http://localhost:5000
- **Nginx Proxy**: http://localhost:80  
- **MySQL Database**: localhost:3306

## 📊 Monitoring & Logs

```bash
# Xem logs tất cả services
docker-compose logs -f

# Xem logs chỉ Flask app
docker-compose logs -f web

# Xem logs MySQL
docker-compose logs -f mysql

# Kiểm tra trạng thái containers
docker-compose ps

# Health check
curl http://localhost:5000/health
```

## 🛑 Dừng services

```bash
# Dừng và xóa containers
docker-compose down

# Dừng và xóa containers + volumes
docker-compose down -v

# Dừng standalone container
docker stop cve-flask-app
```

## 🔄 Cập nhật code

Khi có thay đổi code:

```bash
# Rebuild và restart
docker-compose up -d --build

# Hoặc
docker-compose down
docker-compose build
docker-compose up -d
```

## 🗄️ Database

Database MySQL sẽ được tự động khởi tạo với:
- **Database**: cve_tool
- **User**: user
- **Password**: password
- **Root Password**: rootpassword

Data được persist trong Docker volume `mysql_data`.

## 🐛 Troubleshooting

### Container không start được
```bash
# Kiểm tra logs
docker-compose logs

# Kiểm tra port conflicts
netstat -tulpn | grep :5000
netstat -tulpn | grep :3306
```

### Database connection lỗi
```bash
# Kiểm tra MySQL container
docker-compose exec mysql mysql -u user -p cve_tool

# Reset database
docker-compose down -v
docker-compose up -d
```

### Memory issues
```bash
# Kiểm tra resource usage
docker stats

# Giảm số workers trong Dockerfile
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", ...]
```

## 📁 Cấu trúc file Docker

```
flask_project/
├── Dockerfile              # Image definition
├── docker-compose.yml      # Multi-service setup
├── .dockerignore           # Files to ignore
├── nginx.conf              # Nginx configuration  
├── build_and_run.ps1       # Windows build script
├── build_and_run.sh        # Linux/Mac build script
└── requirements.txt        # Python dependencies
```

## 🔒 Security Notes

- Container chạy với non-root user
- Database passwords nên được thay đổi trong production
- Static files được serve bởi Nginx
- Health checks được enable

## 📝 Environment Variables

Có thể customize qua environment variables:

```yaml
# Trong docker-compose.yml
environment:
  - FLASK_ENV=production
  - DATABASE_URL=mysql+pymysql://user:password@mysql:3306/cve_tool
  - MYSQL_ROOT_PASSWORD=your_secure_password
```

## 🚀 Production Deployment

Cho production, nên:

1. Thay đổi database passwords
2. Sử dụng external database
3. Enable HTTPS trong Nginx
4. Sử dụng Docker secrets
5. Configure logging và monitoring
6. Set up backup strategy
