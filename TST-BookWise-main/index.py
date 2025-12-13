from main import app

# Export app untuk Vercel
# Vercel akan otomatis detect ASGI app
__all__ = ["app"]
