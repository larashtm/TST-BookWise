<div align="center">
  <img src="https://github.com/larashtm/TST-BookWise/blob/main/logo.png" alt="BelajarIndo Logo" width="7600/>
    
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)
![Tests](https://img.shields.io/badge/tests-passing-success)
![License](https://img.shields.io/badge/license-MIT-blue)

</div>

---
> BookWise adalah API backend untuk sistem peminjaman buku digital yang menerapkan prinsip Domain-Driven Design (DDD). Sistem ini mengelola proses peminjaman buku dari request hingga pengembalian dengan workflow yang terstruktur melibatkan dua role: Peminjam (borrower) dan Pengguna (admin/librarian).

## Deskripsi Bounded Context

**Loan Management Context** - Mengelola proses peminjaman buku dari request hingga pengembalian.

### Core Domain Model
- **Aggregate Root**: `Loan` - Entity utama yang mengatur lifecycle peminjaman
- **Value Objects**: `BookId`, `UserId`, `DueDate`, `LoanStatus`
- **Domain Service**: `LoanPolicyService` - Menghitung due date berdasarkan policy bisnis
- **Repository**: `LoanRepository` - Interface untuk persistensi data

## Cara Menjalankan

### 1. Prerequisites
- Python 3.10 atau lebih baru
- pip (Python package manager)

### 2. Setup Environment
```bash
# Clone repository
git clone https://github.com/larashtm/TST-BookWise.git
cd TST-BookWise

# Buat virtual environment
python -m venv .venv

# Aktifkan virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Menjalankan Aplikasi
```bash
uvicorn main:app --reload
```

Aplikasi akan berjalan di: `http://127.0.0.1:8000`

### 4. Akses API Documentation

Setelah aplikasi berjalan, buka browser:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### User Default untuk Testing

**Peminjam**:
- Username: `peminjam1`
- Password: `pinjam123`

**Pengguna (Admin)**:
- Username: `pengguna1`
- Password: `pengguna123`

## API Endpoints

### Authentication

| Method | Endpoint | Deskripsi | Role |
|--------|----------|-----------|------|
| POST | `/auth/login` | Login dan dapatkan token | Public |
| POST | `/auth/refresh` | Refresh access token | Public |
| POST | `/auth/logout` | Logout (revoke refresh token) | Public |
| GET | `/auth/me` | Get user info | Authenticated |
### Loan Management

| Method | Endpoint | Deskripsi | Role |
|--------|----------|-----------|------|
| POST | `/loans` | Buat request peminjaman | Peminjam |
| GET | `/loans/my` | List peminjaman saya | Peminjam |
| GET | `/loans/all` | List semua peminjaman | Pengguna |
| GET | `/loans/{id}` | Detail peminjaman | Peminjam/Pengguna |
| POST | `/loans/{id}/verify` | Verifikasi request | Pengguna |
| POST | `/loans/{id}/approve` | Setujui peminjaman | Pengguna |
| POST | `/loans/{id}/return` | Inisiasi pengembalian | Peminjam |
| POST | `/loans/{id}/finalize-return` | Finalisasi pengembalian | Pengguna |
| POST | `/loans/{id}/extend` | Perpanjang peminjaman | Peminjam |
### General

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |

## Struktur Proyek
```
TST-BookWise/
├── api/                        # API routers yang menangani HTTP requests dan responses
├── auth/                       # Module autentikasi lengkap dengan JWT token management, user database, dan role-based access control dependencies
├── domain/                     # Core business logic aplikasi. Berisi entities, value objects, domain services, dan repository interfaces
├── infrastructure/             # Infrastructure Layer
├── schemas/                    # Pydantic Schemas untuk API
├── tests/                      # Unit & Integration Tests
```

## Flow 
| Activity Peminjam | Activity Pengguna |
| :---: | :---: |
| <img src="https://raw.githubusercontent.com/larashtm/TST-BookWise/feature/activity_peminjam.png" width="300"> | <img src="https://raw.githubusercontent.com/larashtm/TST-BookWise/feature/activity_pengguna.png" width="300"> |
> Diagram aktivitas BookWise disusun berdasarkan peran (role) dalam sistem, yaitu peminjam dan pengguna. Peminjam memiliki akses untuk melakukan peminjaman buku, melihat status peminjaman (my loan), melakukan pengembalian, serta mengajukan perpanjangan. Sementara itu, pengguna berperan dalam melihat daftar peminjaman, melakukan verifikasi, serta menyetujui permintaan peminjaman.