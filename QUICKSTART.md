# Quick Start: Deploy ke Vercel

## Langkah Cepat (5 Menit)

### 1️. Push ke GitHub
```powershell
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### 2️. Deploy di Vercel
1. Buka: https://vercel.com/new
2. Login dengan GitHub
3. Import repository **TST-BookWise**
4. Klik **Deploy**

### 3️. Set Environment Variable (PENTING!)
1. Di Vercel Dashboard → Settings → Environment Variables
2. Tambahkan:
   - **Key**: `SECRET_KEY`
   - **Value**: Jalankan `python generate_secret_key.py` untuk generate

### 4️. Test API
URL Anda: `https://tst-bookwise-xxx.vercel.app`

Test:
- Health: https://your-app.vercel.app/health
- Docs: https://your-app.vercel.app/docs

---

## Atau Gunakan Script Otomatis
```powershell
.\deploy.ps1
```

---

## Butuh Bantuan?
📖 Lihat **DEPLOYMENT_GUIDE.md** untuk panduan lengkap