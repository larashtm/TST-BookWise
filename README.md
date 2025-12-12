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

## Struktur Proyek
```
bookwise/
├── api/                    
│   └── loan_router.py
├── domain/                 
│   ├── loan.py           
│   ├── book_id.py
│   ├── user_id.py
│   ├── due_date.py
│   ├── loan_status.py
│   ├── loan_repository.py
│   └── loan_policy_service.py
├── infrastructure/
│   └── in_memory_loan_repository.py
├── schemas/
│   └── loan_schema.py
├── docs/
├── main.py
└── requirements.txt
```

## Testing Manual

### Menggunakan Swagger UI (Recommended)

1. Buka http://127.0.0.1:8000/docs
2. Klik **POST /loans** → **Try it out**
3. Masukkan JSON request
4. Klik **Execute**
5. Copy `loanId` dari response
6. Test **GET /loans/{loan_id}** dengan `loanId` tersebut

### Menggunakan cURL

**Create Loan:**
```bash
curl -X POST "http://127.0.0.1:8000/loans" \
  -H "Content-Type: application/json" \
  -d '{
    "bookId": "123e4567-e89b-12d3-a456-426614174000",
    "userId": "987fcdeb-51a2-43e7-9876-543210fedcba"
  }'
```

**Get Loan:**
```bash
curl -X GET "http://127.0.0.1:8000/loans/{loan_id}"
```

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

## Testing
  Setelah aplikasi berjalan, buka browser:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc




## Author

**Larashtm**
- GitHub: [@larashtm](https://github.com/larashtm)
- Mata Kuliah: II3160 - Teknologi Sistem Terintegrasi
- Dosen: Ir. Daniel Wiyogo Dwiputro, S.T., M.T.
