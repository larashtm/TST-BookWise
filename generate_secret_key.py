"""
Generate a secure secret key for JWT authentication
Run this script to generate a new SECRET_KEY for production deployment
"""
import secrets

def generate_secret_key(length: int = 32) -> str:
    """
    Generate a cryptographically secure random string
    
    Args:
        length: Length of the key (default: 32)
    
    Returns:
        A URL-safe random string
    """
    return secrets.token_urlsafe(length)

if __name__ == "__main__":
    print("=" * 60)
    print("🔐 BookWise - Secret Key Generator")
    print("=" * 60)
    print()
    
    # Generate multiple keys for different purposes
    secret_key = generate_secret_key(32)
    
    print("Generated SECRET_KEY for production:")
    print(f"  {secret_key}")
    print()
    
    print("📝 Instructions:")
    print("  1. Copy the key above")
    print("  2. In Vercel Dashboard → Settings → Environment Variables")
    print("  3. Add or update SECRET_KEY with the generated value")
    print("  4. Select: Production, Preview, Development")
    print("  5. Save and redeploy")
    print()
    
    print("⚠️  IMPORTANT:")
    print("  - Never commit this key to Git")
    print("  - Keep it secret and secure")
    print("  - Use different keys for dev/staging/prod")
    print()
    print("=" * 60)