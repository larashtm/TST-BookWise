"""
Test script untuk memverifikasi deployment Vercel
Jalankan setelah deployment untuk memastikan API berfungsi dengan baik
"""
import requests
import sys
from typing import Dict, Any

def test_endpoint(url: str, expected_status: int = 200) -> bool:
    """Test endpoint dan cek status code"""
    try:
        response = requests.get(url, timeout=10)
        success = response.status_code == expected_status
        print(f"  {'✅' if success else '❌'} {url}")
        print(f"     Status: {response.status_code}")
        if success and response.status_code == 200:
            try:
                print(f"     Response: {response.json()}")
            except:
                pass
        return success
    except Exception as e:
        print(f"  ❌ {url}")
        print(f"     Error: {str(e)}")
        return False

def test_auth_endpoint(base_url: str) -> bool:
    """Test authentication endpoints"""
    # Test register
    register_url = f"{base_url}/auth/register"
    register_data = {
        "username": f"testuser_{requests.utils.datetime.datetime.now().timestamp()}",
        "password": "testpass123",
        "role": "peminjam"
    }
    
    try:
        response = requests.post(register_url, json=register_data, timeout=10)
        success = response.status_code in [200, 201]
        print(f"  {'✅' if success else '❌'} POST {register_url}")
        print(f"     Status: {response.status_code}")
        return success
    except Exception as e:
        print(f"  ❌ POST {register_url}")
        print(f"     Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🧪 BookWise API - Deployment Verification")
    print("=" * 60)
    print()
    
    # Get base URL from user
    base_url = input("Masukkan URL deployment Vercel (contoh: https://tst-bookwise-xxx.vercel.app): ").strip()
    
    if not base_url:
        print("❌ URL tidak boleh kosong!")
        sys.exit(1)
    
    # Remove trailing slash
    base_url = base_url.rstrip('/')
    
    print()
    print(f"🔍 Testing API di: {base_url}")
    print()
    
    results = {}
    
    # Test 1: Root endpoint
    print("1️⃣ Testing root endpoint...")
    results['root'] = test_endpoint(base_url)
    print()
    
    # Test 2: Health check
    print("2️⃣ Testing health check...")
    results['health'] = test_endpoint(f"{base_url}/health")
    print()
    
    # Test 3: API docs
    print("3️⃣ Testing API documentation...")
    results['docs'] = test_endpoint(f"{base_url}/docs")
    print()
    
    # Test 4: Authentication
    print("4️⃣ Testing authentication...")
    results['auth'] = test_auth_endpoint(base_url)
    print()
    
    # Summary
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name.upper()}")
    
    print()
    print(f"Result: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("🎉 Semua test berhasil! API sudah siap digunakan.")
        print()
        print("📝 URL Penting:")
        print(f"   API Base: {base_url}")
        print(f"   Swagger UI: {base_url}/docs")
        print(f"   ReDoc: {base_url}/redoc")
    else:
        print("⚠️  Beberapa test gagal. Periksa konfigurasi deployment Anda.")
        print()
        print("💡 Tips:")
        print("   1. Pastikan Environment Variables sudah diset")
        print("   2. Cek logs di Vercel Dashboard")
        print("   3. Lihat DEPLOYMENT_GUIDE.md untuk troubleshooting")
    
    print()
    print("=" * 60)
    
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Test dibatalkan oleh user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        sys.exit(1)