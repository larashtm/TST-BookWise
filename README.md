# BookWise - Platform Peminjaman Buku Digital

Proyek Final Teknologi Sistem Terintegrasi (TST) - BookWise adalah platform peminjaman buku digital berbasis Domain-Driven Design (DDD) menggunakan FastAPI.

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

# Buat virtual environment (opsional tapi disarankan)
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

Aplikasi akan berjalan di: `http://localhost:8000`

### 4. Akses API Documentation

Setelah aplikasi berjalan, buka browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Create Loan (Pinjam Buku)
```bash
POST /loans
Content-Type: application/json

{
  "bookId": "123e4567-e89b-12d3-a456-426614174000",
  "userId": "987fcdeb-51a2-43e7-9876-543210fedcba"
}
```

**Response:**
```json
{
  "loanId": "uuid-generated",
  "bookId": "123e4567-e89b-12d3-a456-426614174000",
  "userId": "987fcdeb-51a2-43e7-9876-543210fedcba",
  "status": "borrowed",
  "createdAt": "2025-11-15T10:30:00",
  "dueDate": "2025-11-22"
}
```

### 2. Get Loan by ID
```bash
GET /loans/{loan_id}
```

**Response:** (sama seperti Create Loan)

## Struktur Proyek
```
bookwise/
├── api/                    # API Layer (Controllers/Routers)
│   └── loan_router.py
├── domain/                 # Domain Layer (Business Logic)
│   ├── loan.py            # Aggregate Root
│   ├── book_id.py         # Value Object
│   ├── user_id.py         # Value Object
│   ├── due_date.py        # Value Object
│   ├── loan_status.py     # Value Object (Enum)
│   ├── loan_repository.py # Repository Interface
│   └── loan_policy_service.py
├── infrastructure/         # Infrastructure Layer
│   └── in_memory_loan_repository.py
├── schemas/               # DTOs (Request/Response Models)
│   └── loan_schema.py
├── docs/                  # Dokumentasi Tugas
├── main.py               # Entry Point FastAPI
└── requirements.txt      # Dependencies
```

## Testing Manual

### Menggunakan cURL

**1. Create Loan:**
```bash
curl -X POST "http://localhost:8000/loans" \
  -H "Content-Type: application/json" \
  -d '{
    "bookId": "123e4567-e89b-12d3-a456-426614174000",
    "userId": "987fcdeb-51a2-43e7-9876-543210fedcba"
  }'
```

**2. Get Loan (ganti {loan_id} dengan ID dari response create):**
```bash
curl -X GET "http://localhost:8000/loans/{loan_id}"
```

### Menggunakan Postman/Thunder Client

1. Import collection dari Swagger UI: http://localhost:8000/docs
2. Test endpoints sesuai kebutuhan

## Konsep DDD yang Diterapkan

### 1. Strategic Design
- **Bounded Context**: Loan Management
- **Ubiquitous Language**: Loan, Borrow, Return, Overdue, Due Date

### 2. Tactical Design
- **Entity/Aggregate**: `Loan` sebagai aggregate root dengan identity `loanId`
- **Value Objects**: `BookId`, `UserId`, `DueDate`, `LoanStatus` (immutable, no identity)
- **Domain Service**: `LoanPolicyService` untuk business rule yang tidak fit di entity
- **Repository Pattern**: Abstraksi persistensi dengan interface

### 3. Layering
- **Domain Layer**: Pure business logic, tidak ada dependency eksternal
- **Application Layer**: Orchestration (via API router)
- **Infrastructure Layer**: Technical implementation (database, dll)

## Author

**Larashtm**
- GitHub: [@larashtm](https://github.com/larashtm)
- Mata Kuliah: II3160 - Teknologi Sistem Terintegrasi
- Dosen: Ir. Daniel Wiyogo Dwiputro, S.T., M.T.

## Status Tugas

- [x] Tugas 1: Analisis Domain (Deadline: 13 Okt 2025)
- [x] Tugas 2: Desain Batasan (Deadline: 20 Okt 2025)
- [x] Tugas 3: Desain Taktis (Deadline: 3 Nov 2025)
- [x] **Tugas 4: Implementasi Awal (Deadline: 17 Nov 2025)** ✅
- [ ] Tugas 5: Implementasi Lanjutan (Deadline: 1 Des 2025)
- [ ] Tugas 6: Finalisasi (Deadline: 12 Des 2025)
