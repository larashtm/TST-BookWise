# 🚀 Panduan Deployment BookWise API ke Vercel

## 📋 Prasyarat

1. **Akun Vercel** - Daftar di [vercel.com](https://vercel.com) (gratis)
2. **Git** - Pastikan terinstall di komputer Anda
3. **Repository GitHub** - Proyek harus di-push ke GitHub
4. **Vercel CLI** (Opsional) - Untuk deployment via command line

---

## 🔧 Persiapan Sebelum Deploy

### 1. File yang Sudah Disiapkan ✅

Proyek Anda sudah memiliki file-file berikut yang dibutuhkan Vercel:

- ✅ `vercel.json` - Konfigurasi Vercel
- ✅ `requirements.txt` - Dependencies Python
- ✅ `runtime.txt` - Versi Python (3.10)
- ✅ `.vercelignore` - File yang diabaikan saat deployment
- ✅ `main.py` - Entry point API

### 2. Push Kode ke GitHub

```powershell
# Inisialisasi git (jika belum)
git init

# Tambahkan semua file
git add .

# Commit perubahan
git commit -m "Prepare for Vercel deployment"

# Tambahkan remote repository (ganti dengan URL repo Anda)
git remote add origin https://github.com/username/TST-BookWise.git

# Push ke GitHub
git push -u origin main
```

---

## 🌐 Metode 1: Deploy via Vercel Dashboard (Paling Mudah)

### Langkah 1: Login ke Vercel
1. Buka [vercel.com](https://vercel.com)
2. Klik **"Sign Up"** atau **"Log In"**
3. Login dengan akun GitHub Anda

### Langkah 2: Import Project
1. Di dashboard Vercel, klik **"Add New..."** → **"Project"**
2. Pilih **"Import Git Repository"**
3. Cari dan pilih repository **TST-BookWise**
4. Klik **"Import"**

### Langkah 3: Configure Project
Vercel akan otomatis mendeteksi konfigurasi dari `vercel.json`, tapi pastikan:

- **Framework Preset**: Other
- **Root Directory**: `./` (atau kosongkan)
- **Build Command**: Kosongkan (tidak perlu)
- **Output Directory**: Kosongkan
- **Install Command**: `pip install -r requirements.txt`

### Langkah 4: Environment Variables (PENTING! 🔐)
1. Klik **"Environment Variables"**
2. Tambahkan variabel berikut:

   ```
   Key: SECRET_KEY
   Value: CHANGE_THIS_SECRET_KEY_BOOKWISE_2025
   ```

   > ⚠️ **PENTING**: Untuk production, ganti dengan secret key yang lebih aman!
   > Generate dengan: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

3. (Opsional) Tambahkan variabel lain jika diperlukan:
   ```
   Key: ENVIRONMENT
   Value: production
   ```

### Langkah 5: Deploy!
1. Klik **"Deploy"**
2. Tunggu proses deployment (2-5 menit)
3. Setelah selesai, Anda akan mendapat URL: `https://tst-bookwise-xxx.vercel.app`

---

## 💻 Metode 2: Deploy via Vercel CLI

### Langkah 1: Install Vercel CLI
```powershell
npm install -g vercel
```

### Langkah 2: Login
```powershell
vercel login
```

### Langkah 3: Deploy
```powershell
# Navigasi ke folder proyek
cd C:\Users\ASUS\OneDrive\Documents\TST-BookWise\TST-BookWise

# Deploy (development)
vercel

# Deploy ke production
vercel --prod
```

### Langkah 4: Set Environment Variables
```powershell
vercel env add SECRET_KEY
# Masukkan nilai: CHANGE_THIS_SECRET_KEY_BOOKWISE_2025
# Pilih environment: Production, Preview, Development
```

---

## 🧪 Testing Deployment

Setelah deployment berhasil, test API Anda:

### 1. Health Check
```powershell
# Ganti dengan URL Vercel Anda
curl https://your-app.vercel.app/health
```

Respons:
```json
{
  "status": "ok"
}
```

### 2. Root Endpoint
```powershell
curl https://your-app.vercel.app/
```

Respons:
```json
{
  "message": "BookWise API is running",
  "status": "healthy",
  "endpoints": {
    "docs": "/docs",
    "redoc": "/redoc",
    "auth": "/auth/*",
    "loans": "/loans/*"
  }
}
```

### 3. API Documentation
Buka di browser:
- Swagger UI: `https://your-app.vercel.app/docs`
- ReDoc: `https://your-app.vercel.app/redoc`

### 4. Test Authentication
```powershell
# Register user baru
curl -X POST https://your-app.vercel.app/auth/register `
  -H "Content-Type: application/json" `
  -d '{
    "username": "testuser",
    "password": "testpass123",
    "role": "peminjam"
  }'

# Login
curl -X POST https://your-app.vercel.app/auth/login `
  -H "Content-Type: application/json" `
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

---

## 📝 Update Deployment

### Auto Deploy (Recommended)
Setiap kali Anda push ke GitHub, Vercel otomatis men-deploy ulang:

```powershell
git add .
git commit -m "Update API"
git push origin main
```

### Manual Deploy via CLI
```powershell
vercel --prod
```

---

## ⚙️ Konfigurasi Lanjutan

### 1. Custom Domain
1. Di Vercel Dashboard → Project Settings → Domains
2. Klik "Add"
3. Masukkan domain Anda
4. Ikuti instruksi DNS configuration

### 2. Environment Variables per Environment
```powershell
# Production
vercel env add SECRET_KEY production

# Preview (untuk PR)
vercel env add SECRET_KEY preview

# Development
vercel env add SECRET_KEY development
```

### 3. Logs & Monitoring
1. Buka Vercel Dashboard
2. Pilih project Anda
3. Tab "Deployments" → Klik deployment terakhir
4. Tab "Functions" atau "Logs" untuk melihat logs

---

## 🔒 Security Best Practices

### 1. Generate Secret Key yang Aman
```powershell
# Generate secret key baru
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Update di Vercel:
1. Dashboard → Project → Settings → Environment Variables
2. Edit `SECRET_KEY` dengan nilai baru
3. Redeploy

### 2. Jangan Commit Secrets
Pastikan `.env` ada di `.gitignore` (sudah ada di `.vercelignore`)

### 3. CORS Configuration (Jika Diperlukan)
Edit `main.py` untuk menambahkan CORS:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🐛 Troubleshooting

### Error: "Build Failed"
- **Solusi**: Periksa `requirements.txt` - pastikan semua dependencies valid
- Lihat build logs di Vercel Dashboard

### Error: "Module Not Found"
- **Solusi**: Pastikan `PYTHONPATH` sudah benar
- File `vercel.json` sudah di-configure dengan benar

### Error: 500 Internal Server Error
- **Solusi**: Cek logs di Vercel Dashboard → Functions
- Mungkin ada error di kode Python Anda

### API Lambat / Timeout
- **Solusi**: Vercel free tier memiliki cold start
- Upgrade ke plan berbayar untuk performa lebih baik

---

## 📊 Limitasi Vercel Free Tier

- ⏱️ **Function Timeout**: 10 detik
- 💾 **Function Memory**: 1024 MB
- 📦 **Deployment Size**: 250 MB
- 🔄 **Builds per Day**: 100
- 📈 **Bandwidth**: 100 GB/month
- 🌐 **Serverless Functions**: 12 per deployment

---

## 📚 Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/vercel/)
- [Vercel CLI Documentation](https://vercel.com/docs/cli)

---

## ✅ Checklist Deploy

- [ ] Kode sudah di-push ke GitHub
- [ ] File `vercel.json` sudah ada dan benar
- [ ] File `requirements.txt` sudah lengkap
- [ ] Secret key sudah di-set di Environment Variables
- [ ] Project sudah di-import di Vercel Dashboard
- [ ] Deployment berhasil
- [ ] API endpoint dapat diakses
- [ ] `/docs` dapat dibuka
- [ ] Authentication berfungsi
- [ ] Domain custom sudah dikonfigurasi (opsional)

---

## 🎉 Selesai!

URL API Anda akan seperti: `https://tst-bookwise-xxx.vercel.app`

Jangan lupa update URL ini di dokumentasi dan aplikasi frontend Anda!
