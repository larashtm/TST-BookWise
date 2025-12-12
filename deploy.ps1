# Quick Deploy Script untuk Vercel
# Jalankan script ini untuk deploy ke Vercel dengan mudah

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🚀 BookWise API - Vercel Deployment Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path .git)) {
    Write-Host "❌ Git belum diinisialisasi" -ForegroundColor Red
    Write-Host "   Menginisialisasi git..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git initialized" -ForegroundColor Green
}

# Check if vercel CLI is installed
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue
if (-not $vercelInstalled) {
    Write-Host "⚠️  Vercel CLI belum terinstall" -ForegroundColor Yellow
    Write-Host "   Install dengan: npm install -g vercel" -ForegroundColor Yellow
    Write-Host ""
    $install = Read-Host "Install Vercel CLI sekarang? (y/n)"
    if ($install -eq "y") {
        npm install -g vercel
    } else {
        Write-Host "❌ Deployment dibatalkan" -ForegroundColor Red
        exit
    }
}

Write-Host ""
Write-Host "📋 Pilih metode deployment:" -ForegroundColor Cyan
Write-Host "   1. Deploy via GitHub (Recommended)" -ForegroundColor White
Write-Host "   2. Deploy via Vercel CLI" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Pilihan (1/2)"

if ($choice -eq "1") {
    Write-Host ""
    Write-Host "📦 Preparing untuk push ke GitHub..." -ForegroundColor Cyan
    
    # Check if remote exists
    $remote = git remote get-url origin 2>$null
    if (-not $remote) {
        Write-Host "⚠️  Remote repository belum diset" -ForegroundColor Yellow
        $repoUrl = Read-Host "Masukkan URL GitHub repository (contoh: https://github.com/username/TST-BookWise.git)"
        git remote add origin $repoUrl
    }
    
    Write-Host ""
    Write-Host "📝 Menambahkan file..." -ForegroundColor Cyan
    git add .
    
    Write-Host ""
    $commitMsg = Read-Host "Commit message (tekan Enter untuk default)"
    if ([string]::IsNullOrWhiteSpace($commitMsg)) {
        $commitMsg = "Prepare for Vercel deployment"
    }
    
    git commit -m $commitMsg
    
    Write-Host ""
    Write-Host "🚀 Pushing ke GitHub..." -ForegroundColor Cyan
    git push -u origin main
    
    Write-Host ""
    Write-Host "✅ Kode sudah di-push ke GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📖 Langkah selanjutnya:" -ForegroundColor Cyan
    Write-Host "   1. Buka https://vercel.com/new" -ForegroundColor White
    Write-Host "   2. Login dengan GitHub" -ForegroundColor White
    Write-Host "   3. Import repository TST-BookWise" -ForegroundColor White
    Write-Host "   4. Set Environment Variable: SECRET_KEY" -ForegroundColor Yellow
    Write-Host "      (Generate dengan: python generate_secret_key.py)" -ForegroundColor Yellow
    Write-Host "   5. Klik Deploy!" -ForegroundColor White
    Write-Host ""
    Write-Host "📚 Lihat DEPLOYMENT_GUIDE.md untuk detail lengkap" -ForegroundColor Cyan
    
} elseif ($choice -eq "2") {
    Write-Host ""
    Write-Host "🔐 Login ke Vercel..." -ForegroundColor Cyan
    vercel login
    
    Write-Host ""
    Write-Host "🚀 Deploying ke Vercel..." -ForegroundColor Cyan
    Write-Host ""
    
    $prodDeploy = Read-Host "Deploy ke production? (y/n, default: n)"
    if ($prodDeploy -eq "y") {
        vercel --prod
    } else {
        vercel
    }
    
    Write-Host ""
    Write-Host "✅ Deployment selesai!" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  Jangan lupa set Environment Variables:" -ForegroundColor Yellow
    Write-Host "   vercel env add SECRET_KEY" -ForegroundColor White
    Write-Host "   (Generate dengan: python generate_secret_key.py)" -ForegroundColor Yellow
    
} else {
    Write-Host "❌ Pilihan tidak valid" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🎉 Proses selesai!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan