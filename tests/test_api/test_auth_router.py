import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


class TestLogin:
    """Test suite for POST /auth/login"""

    def test_login_success_peminjam(self):
        """Test successful login for peminjam"""
        response = client.post(
            "/auth/login",
            data={"username": "peminjam1", "password": "pinjam123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_success_pengguna(self):
        """Test successful login for pengguna"""
        response = client.post(
            "/auth/login",
            data={"username": "pengguna1", "password": "pengguna123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_login_wrong_password(self):
        """Test login with wrong password"""
        response = client.post(
            "/auth/login",
            data={"username": "peminjam1", "password": "wrongpassword"}
        )
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_wrong_username(self):
        """Test login with non-existent username"""
        response = client.post(
            "/auth/login",
            data={"username": "nonexistent", "password": "anypassword"}
        )
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_missing_username(self):
        """Test login without username"""
        response = client.post(
            "/auth/login",
            data={"password": "pinjam123"}
        )
        
        assert response.status_code == 422

    def test_login_missing_password(self):
        """Test login without password"""
        response = client.post(
            "/auth/login",
            data={"username": "peminjam1"}
        )
        
        assert response.status_code == 422

    def test_login_empty_credentials(self):
        """Test login with empty credentials"""
        response = client.post(
            "/auth/login",
            data={"username": "", "password": ""}
        )
        
        assert response.status_code == 401

    def test_login_case_sensitive_username(self):
        """Test that username is case sensitive"""
        response = client.post(
            "/auth/login",
            data={"username": "PEMINJAM1", "password": "pinjam123"}
        )
        
        assert response.status_code == 401

    def test_login_token_format(self):
        """Test that returned token is in correct format"""
        response = client.post(
            "/auth/login",
            data={"username": "peminjam1", "password": "pinjam123"}
        )
        
        data = response.json()
        # JWT tokens have 3 parts separated by dots
        assert data["access_token"].count('.') == 2


class TestRefreshToken:
    """Test suite for POST /auth/refresh"""

    def test_refresh_token_success(self):
        """Test successful token refresh"""
        # First login
        login_response = client.post(
            "/auth/login",
            data={"username": "peminjam1", "password": "pinjam123"}
        )
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh token
        response = client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        # New refresh token should be different
        assert data["refresh_token"] != refresh_token

    def test_refresh_with_invalid_token(self):
        """Test refresh with invalid token"""
        response = client.post(
            "/auth/refresh",
            json={"refresh_token": "invalid-token"}
        )
        
        assert response.status_code == 401
        assert "Invalid refresh token" in response.json()["detail"]

    def test_refresh_token_reuse_fails(self):
        """Test that used refresh token cannot be reused"""
        # Login
        login_response = client.post(
            "/auth/login",
            data={"username": "peminjam1", "password": "pinjam123"}
        )
        refresh_token = login_response.json()["refresh_token"]
        
        # Use refresh token once
        client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        # Try to use again
        response = client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == 401

    def test_refresh_missing_token(self):
        """Test refresh without token"""
        response = client.post(
            "/auth/refresh",
            json={}
        )
        
        assert response.status_code == 422


class TestLogout:
    """Test suite for POST /auth/logout"""

    def test_logout_success(self):
        """Test successful logout"""
        # Login first
        login_response = client.post(
            "/auth/login",
            data={"username": "peminjam1", "password": "pinjam123"}
        )
        refresh_token = login_response.json()["refresh_token"]
        
        # Logout
        response = client.post(
            "/auth/logout",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == 200
        assert "revoked" in response.json()["message"].lower()

    def test_logout_with_invalid_token(self):
        """Test logout with non-existent token"""
        response = client.post(
            "/auth/logout",
            json={"refresh_token": "non-existent-token"}
        )
        
        # Should still return success even if token doesn't exist
        assert response.status_code == 200

    def test_logout_prevents_refresh(self):
        """Test that logout prevents token refresh"""
        # Login
        login_response = client.post(
            "/auth/login",
            data={"username": "peminjam1", "password": "pinjam123"}
        )
        refresh_token = login_response.json()["refresh_token"]
        
        # Logout
        client.post(
            "/auth/logout",
            json={"refresh_token": refresh_token}
        )
        
        # Try to refresh
        response = client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == 401


class TestMe:
    """Test suite for GET /auth/me"""

    def test_me_with_valid_token(self):
        """Test getting user info with valid token"""
        # Login
        login_response = client.post(
            "/auth/login",
            data={"username": "peminjam1", "password": "pinjam123"}
        )
        access_token = login_response.json()["access_token"]
        
        # Get user info
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "peminjam1"
        assert data["role"] == "peminjam"
        assert data["disabled"] is False

    def test_me_without_token(self):
        """Test getting user info without token"""
        response = client.get("/auth/me")
        
        assert response.status_code == 401

    def test_me_with_invalid_token(self):
        """Test getting user info with invalid token"""
        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid-token"}
        )
        
        assert response.status_code == 401

    def test_me_for_pengguna(self):
        """Test getting user info for pengguna role"""
        # Login as pengguna
        login_response = client.post(
            "/auth/login",
            data={"username": "pengguna1", "password": "pengguna123"}
        )
        access_token = login_response.json()["access_token"]
        
        # Get user info
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "pengguna1"
        assert data["role"] == "pengguna"


class TestAuthIntegration:
    """Integration tests for authentication flow"""

    def test_complete_auth_flow(self):
        """Test complete authentication flow"""
        # 1. Login
        login_response = client.post(
            "/auth/login",
            data={"username": "peminjam1", "password": "pinjam123"}
        )
        assert login_response.status_code == 200
        
        access_token = login_response.json()["access_token"]
        refresh_token = login_response.json()["refresh_token"]
        
        # 2. Access protected resource
        me_response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert me_response.status_code == 200
        
        # 3. Refresh token
        refresh_response = client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        assert refresh_response.status_code == 200
        
        new_refresh_token = refresh_response.json()["refresh_token"]
        
        # 4. Logout
        logout_response = client.post(
            "/auth/logout",
            json={"refresh_token": new_refresh_token}
        )
        assert logout_response.status_code == 200

    def test_expired_token_handling(self):
        """Test handling of expired tokens"""
        login_response = client.post(
            "/auth/login",
            data={"username": "peminjam1", "password": "pinjam123"}
        )
        assert "access_token" in login_response.json()