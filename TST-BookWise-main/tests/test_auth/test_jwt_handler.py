import pytest
from datetime import timedelta, datetime
from uuid import uuid4
from auth.jwt_handler import (
    create_access_token,
    decode_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM
)
from jose import jwt

class TestCreateAccessToken:
    """Test suite for creating access tokens"""

    def test_create_access_token_with_valid_data(self):
        """Test creating access token with valid subject and role"""
        subject = str(uuid4())
        role = "peminjam"
        
        token = create_access_token(subject, role)
        
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_custom_expiry(self):
        """Test creating access token with custom expiration"""
        subject = str(uuid4())
        role = "pengguna"
        expires = timedelta(minutes=30)
        
        token = create_access_token(subject, role, expires_delta=expires)
        
        assert isinstance(token, str)

    def test_create_access_token_contains_subject(self):
        """Test that token contains subject in payload"""
        subject = str(uuid4())
        role = "peminjam"
        
        token = create_access_token(subject, role)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        assert payload["sub"] == subject

    def test_create_access_token_contains_role(self):
        """Test that token contains role in payload"""
        subject = str(uuid4())
        role = "pengguna"
        
        token = create_access_token(subject, role)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        assert payload["role"] == role

    def test_create_access_token_contains_iat(self):
        """Test that token contains issued at timestamp"""
        subject = str(uuid4())
        role = "peminjam"
        
        token = create_access_token(subject, role)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        assert "iat" in payload
        assert isinstance(payload["iat"], int)

    def test_create_access_token_contains_exp(self):
        """Test that token contains expiration timestamp"""
        subject = str(uuid4())
        role = "peminjam"
        
        token = create_access_token(subject, role)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        assert "exp" in payload
        assert isinstance(payload["exp"], int)

    def test_create_access_token_expiry_time_correct(self):
        """Test that token expiry is set correctly"""
        subject = str(uuid4())
        role = "peminjam"
        expires = timedelta(minutes=15)
        
        before = datetime.utcnow()
        token = create_access_token(subject, role, expires_delta=expires)
        after = datetime.utcnow()
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_time = datetime.utcfromtimestamp(payload["exp"])
        
        # Should be approximately 15 minutes from now
        expected_min = before + expires
        expected_max = after + expires
        
        assert expected_min <= exp_time <= expected_max

    def test_create_access_token_different_roles(self):
        """Test creating tokens with different roles"""
        subject = str(uuid4())
        
        token_peminjam = create_access_token(subject, "peminjam")
        token_pengguna = create_access_token(subject, "pengguna")
        
        payload_peminjam = jwt.decode(token_peminjam, SECRET_KEY, algorithms=[ALGORITHM])
        payload_pengguna = jwt.decode(token_pengguna, SECRET_KEY, algorithms=[ALGORITHM])
        
        assert payload_peminjam["role"] == "peminjam"
        assert payload_pengguna["role"] == "pengguna"


class TestDecodeAccessToken:
    """Test suite for decoding access tokens"""

    def test_decode_valid_token(self):
        """Test decoding a valid token"""
        subject = str(uuid4())
        role = "peminjam"
        
        token = create_access_token(subject, role)
        payload = decode_access_token(token)
        
        assert payload is not None
        assert payload["sub"] == subject
        assert payload["role"] == role

    def test_decode_token_returns_dict(self):
        """Test that decode returns a dictionary"""
        subject = str(uuid4())
        role = "peminjam"
        
        token = create_access_token(subject, role)
        payload = decode_access_token(token)
        
        assert isinstance(payload, dict)

    def test_decode_invalid_token(self):
        """Test decoding an invalid token"""
        invalid_token = "invalid.token.here"
        
        payload = decode_access_token(invalid_token)
        
        assert payload is None

    def test_decode_tampered_token(self):
        """Test decoding a tampered token"""
        subject = str(uuid4())
        role = "peminjam"
        
        token = create_access_token(subject, role)
        # Tamper with token
        tampered_token = token[:-5] + "aaaaa"
        
        payload = decode_access_token(tampered_token)
        
        assert payload is None

    def test_decode_expired_token(self):
        """Test decoding an expired token"""
        subject = str(uuid4())
        role = "peminjam"
        # Create token that expires immediately
        expires = timedelta(seconds=-1)
        
        token = create_access_token(subject, role, expires_delta=expires)
        payload = decode_access_token(token)
        
        # Should return None for expired token
        assert payload is None

    def test_decode_token_with_wrong_secret(self):
        """Test that token with wrong secret fails to decode"""
        subject = str(uuid4())
        role = "peminjam"
        
        # Create token with different secret
        wrong_token = jwt.encode(
            {"sub": subject, "role": role},
            "wrong_secret",
            algorithm=ALGORITHM
        )
        
        payload = decode_access_token(wrong_token)
        
        assert payload is None

    def test_decode_empty_token(self):
        """Test decoding empty token"""
        payload = decode_access_token("")
        
        assert payload is None

    def test_decode_none_token(self):
        """Test decoding None as token"""
        with pytest.raises((TypeError, AttributeError)):
            decode_access_token(None)


class TestCreateRefreshToken:
    """Test suite for creating refresh tokens"""

    def test_create_refresh_token_returns_string(self):
        """Test that refresh token is a string"""
        token = create_refresh_token()
        
        assert isinstance(token, str)

    def test_create_refresh_token_not_empty(self):
        """Test that refresh token is not empty"""
        token = create_refresh_token()
        
        assert len(token) > 0

    def test_create_refresh_token_unique(self):
        """Test that multiple refresh tokens are unique"""
        tokens = [create_refresh_token() for _ in range(10)]
        
        unique_tokens = set(tokens)
        assert len(unique_tokens) == 10

    def test_create_refresh_token_is_uuid_format(self):
        """Test that refresh token is in UUID format"""
        token = create_refresh_token()
        
        # Should be able to parse as UUID
        from uuid import UUID
        try:
            UUID(token)
            is_valid_uuid = True
        except ValueError:
            is_valid_uuid = False
        
        assert is_valid_uuid

    def test_refresh_token_different_from_access_token(self):
        """Test that refresh token is different from access token"""
        subject = str(uuid4())
        role = "peminjam"
        
        access_token = create_access_token(subject, role)
        refresh_token = create_refresh_token()
        
        assert access_token != refresh_token


class TestTokenIntegration:
    """Integration tests for token operations"""

    def test_create_and_decode_token_flow(self):
        """Test complete flow of creating and decoding token"""
        subject = str(uuid4())
        role = "peminjam"
        
        # Create token
        token = create_access_token(subject, role)
        
        # Decode token
        payload = decode_access_token(token)
        
        # Verify payload
        assert payload is not None
        assert payload["sub"] == subject
        assert payload["role"] == role

    def test_token_with_all_roles(self):
        """Test creating and decoding tokens for all roles"""
        subject = str(uuid4())
        roles = ["peminjam", "pengguna"]
        
        for role in roles:
            token = create_access_token(subject, role)
            payload = decode_access_token(token)
            
            assert payload["role"] == role

    def test_multiple_tokens_same_user(self):
        """Test creating multiple tokens for same user"""
        subject = str(uuid4())
        role = "peminjam"
        
        token1 = create_access_token(subject, role)
        token2 = create_access_token(subject, role)
        
        # Tokens should be different (different iat)
        assert token1 != token2
        
        # But both should decode to same subject
        payload1 = decode_access_token(token1)
        payload2 = decode_access_token(token2)
        
        assert payload1["sub"] == payload2["sub"]

    def test_token_lifecycle(self):
        """Test token from creation to expiration"""
        subject = str(uuid4())
        role = "peminjam"
        
        # Create token with short expiry
        token = create_access_token(
            subject, 
            role, 
            expires_delta=timedelta(seconds=1)
        )
        
        # Should be valid immediately
        payload = decode_access_token(token)
        assert payload is not None
        
        # Wait for expiration (in real test, you might mock time)
        import time
        time.sleep(2)
        
        # Should be invalid after expiration
        payload = decode_access_token(token)
        assert payload is None