# ✅ Deployment Checklist

Gunakan checklist ini untuk memastikan semua persiapan deployment sudah lengkap.

## 📋 Pre-Deployment Checklist

### Kode & Konfigurasi
- [x] File `main.py` sebagai entry point
- [x] File `requirements.txt` dengan semua dependencies
- [x] File `vercel.json` dengan konfigurasi Vercel
- [x] File `runtime.txt` dengan versi Python 3.10
- [x] File `.vercelignore` untuk exclude files
- [x] File `.gitignore` untuk security

### Repository
- [ ] Kode sudah di-commit
- [ ] Repository sudah di-push ke GitHub
- [ ] Branch main sudah up-to-date
- [ ] Tidak ada file sensitif ter-commit (.env, secrets, dll)

### Security
- [ ] SECRET_KEY sudah di-generate dengan `generate_secret_key.py`
- [ ] SECRET_KEY tidak ter-commit di git
- [ ] Password default sudah diganti (jika ada)

---

## 🚀 Deployment Checklist

### Setup Vercel
- [ ] Akun Vercel sudah dibuat
- [ ] GitHub sudah di-connect ke Vercel
- [ ] Repository TST-BookWise sudah visible di Vercel

### Configuration
- [ ] Project sudah di-import ke Vercel
- [ ] Framework preset: Other
- [ ] Build command: (kosongkan)
- [ ] Output directory: (kosongkan)
- [ ] Install command: pip install -r requirements.txt

### Environment Variables
- [ ] SECRET_KEY sudah di-set
- [ ] Environment: Production dipilih
- [ ] Environment: Preview dipilih (opsional)
- [ ] Environment: Development dipilih (opsional)

### Deployment
- [ ] Build berhasil (tidak ada error)
- [ ] Deployment berhasil
- [ ] URL deployment sudah tersedia

---

## 🧪 Post-Deployment Checklist

### Testing Endpoints
- [ ] Root endpoint (/) berfungsi
- [ ] Health check (/health) berfungsi
- [ ] API docs (/docs) dapat dibuka
- [ ] ReDoc (/redoc) dapat dibuka

### Testing Features
- [ ] Register user berhasil
- [ ] Login berhasil
- [ ] JWT token ter-generate
- [ ] Create loan berfungsi
- [ ] Get loan berfungsi
- [ ] Extend loan berfungsi
- [ ] Return loan berfungsi

### Automated Test
- [ ] Jalankan `python test_deployment.py` dan semua pass

---

## 📊 Performance Check

- [ ] Response time < 2 detik
- [ ] API tidak timeout
- [ ] Tidak ada error 5xx

---

## 📝 Documentation

- [ ] README.md sudah update dengan URL deployment
- [ ] API documentation accessible
- [ ] Postman collection / API examples tersedia (opsional)

---

## 🔄 Auto Deployment

- [ ] Auto deployment dari GitHub enabled
- [ ] Test push ke GitHub dan verify auto-deploy
- [ ] Rollback mechanism dipahami

---

## 🎉 Final Steps

- [ ] URL deployment di-share ke team/dosen
- [ ] Dokumentasi deployment disimpan
- [ ] Monitoring setup (Vercel dashboard)
- [ ] Backup konfigurasi (env variables, dll)

---

## 📞 Support

Jika ada masalah:
1. Cek logs di Vercel Dashboard
2. Baca DEPLOYMENT_GUIDE.md
3. Cek GitHub Issues di repository

---

**Status**: [ ] Ready to Deploy | [ ] Deployed | [ ] Verified

**Deployment URL**: _____________________________________

**Deployed Date**: _____________________________________

**Deployed By**: _____________________________________
