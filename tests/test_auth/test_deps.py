"""
Unit tests for authentication dependencies
"""
import pytest
from fastapi import HTTPException
from uuid import uuid4
from auth.deps import (
    get_current_active_user,
    require_role,
    allow_roles,
    oauth2_scheme
)
from auth.jwt_handler import create_access_token
from auth.users import User
from datetime import timedelta


class TestGetCurrentActiveUser:
    """Test suite for get_current_active_user dependency"""

    def test_get_current_user_with_valid_token(self):
        """Test getting current user with valid token"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        token = create_access_token(str(user.user_id), user.role)
        
        result = get_current_active_user(token)
        
        assert result is not None
        assert result.username == "peminjam1"
        assert result.role == "peminjam"

    def test_get_current_user_with_invalid_token(self):
        """Test getting current user with invalid token"""
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_user("invalid_token")
        
        assert exc_info.value.status_code == 401
        assert "Invalid or expired token" in str(exc_info.value.detail)

    def test_get_current_user_with_expired_token(self):
        """Test getting current user with expired token"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        
        # Create expired token
        token = create_access_token(
            str(user.user_id), 
            user.role, 
            expires_delta=timedelta(seconds=-1)
        )
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_user(token)
        
        assert exc_info.value.status_code == 401

    def test_get_current_user_with_non_existent_user_id(self):
        """Test getting current user with token containing non-existent user ID"""
        fake_id = str(uuid4())
        token = create_access_token(fake_id, "peminjam")
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_user(token)
        
        assert exc_info.value.status_code == 401
        assert "User not found" in str(exc_info.value.detail)

    def test_get_current_user_with_malformed_token(self):
        """Test getting current user with malformed token"""
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_user("not.a.valid.jwt")
        
        assert exc_info.value.status_code == 401

    def test_get_current_user_with_empty_token(self):
        """Test getting current user with empty token"""
        with pytest.raises(HTTPException):
            get_current_active_user("")


class TestRequireRole:
    """Test suite for require_role dependency"""

    def test_require_role_peminjam_with_peminjam_user(self):
        """Test require_role allows correct role"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        token = create_access_token(str(user.user_id), user.role)
        
        checker = require_role("peminjam")
        current_user = get_current_active_user(token)
        result = checker(current_user)
        
        assert result.role == "peminjam"

    def test_require_role_peminjam_with_pengguna_user(self):
        """Test require_role blocks wrong role"""
        from auth.users import get_user_by_username
        user = get_user_by_username("pengguna1")
        token = create_access_token(str(user.user_id), user.role)
        
        checker = require_role("peminjam")
        current_user = get_current_active_user(token)
        
        with pytest.raises(HTTPException) as exc_info:
            checker(current_user)
        
        assert exc_info.value.status_code == 403
        assert "insufficient role" in str(exc_info.value.detail)

    def test_require_role_pengguna_with_pengguna_user(self):
        """Test require_role allows pengguna role"""
        from auth.users import get_user_by_username
        user = get_user_by_username("pengguna1")
        token = create_access_token(str(user.user_id), user.role)
        
        checker = require_role("pengguna")
        current_user = get_current_active_user(token)
        result = checker(current_user)
        
        assert result.role == "pengguna"

    def test_require_role_returns_user_object(self):
        """Test that require_role returns the user object"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        token = create_access_token(str(user.user_id), user.role)
        
        checker = require_role("peminjam")
        current_user = get_current_active_user(token)
        result = checker(current_user)
        
        assert isinstance(result, User)
        assert result.username == "peminjam1"


class TestAllowRoles:
    """Test suite for allow_roles dependency"""

    def test_allow_roles_single_role_match(self):
        """Test allow_roles with single matching role"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        token = create_access_token(str(user.user_id), user.role)
        
        checker = allow_roles("peminjam")
        current_user = get_current_active_user(token)
        result = checker(current_user)
        
        assert result.role == "peminjam"

    def test_allow_roles_multiple_roles_match(self):
        """Test allow_roles with multiple roles, user matches one"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        token = create_access_token(str(user.user_id), user.role)
        
        checker = allow_roles("peminjam", "pengguna")
        current_user = get_current_active_user(token)
        result = checker(current_user)
        
        assert result.role == "peminjam"

    def test_allow_roles_multiple_roles_pengguna_match(self):
        """Test allow_roles with pengguna user"""
        from auth.users import get_user_by_username
        user = get_user_by_username("pengguna1")
        token = create_access_token(str(user.user_id), user.role)
        
        checker = allow_roles("peminjam", "pengguna")
        current_user = get_current_active_user(token)
        result = checker(current_user)
        
        assert result.role == "pengguna"

    def test_allow_roles_no_match(self):
        """Test allow_roles when user role doesn't match any allowed"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        token = create_access_token(str(user.user_id), user.role)
        
        checker = allow_roles("pengguna")
        current_user = get_current_active_user(token)
        
        with pytest.raises(HTTPException) as exc_info:
            checker(current_user)
        
        assert exc_info.value.status_code == 403

    def test_allow_roles_with_three_roles(self):
        """Test allow_roles with three different roles"""
        from auth.users import get_user_by_username
        user = get_user_by_username("pengguna1")
        token = create_access_token(str(user.user_id), user.role)
        
        checker = allow_roles("admin", "pengguna", "peminjam")
        current_user = get_current_active_user(token)
        result = checker(current_user)
        
        assert result.role == "pengguna"


class TestOAuth2Scheme:
    """Test suite for OAuth2 scheme"""

    def test_oauth2_scheme_exists(self):
        """Test that oauth2_scheme is properly configured"""
        assert oauth2_scheme is not None
        assert oauth2_scheme.scheme_name == "OAuth2PasswordBearer"

    def test_oauth2_scheme_token_url(self):
        """Test that oauth2_scheme has correct token URL"""
        assert oauth2_scheme.tokenUrl == "/auth/login"


class TestDepsIntegration:
    """Integration tests for authentication dependencies"""

    def test_full_auth_flow_peminjam(self):
        """Test complete auth flow for peminjam"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        token = create_access_token(str(user.user_id), user.role)
        
        # Get current user
        current_user = get_current_active_user(token)
        assert current_user.username == "peminjam1"
        
        # Check role requirement
        checker = require_role("peminjam")
        result = checker(current_user)
        assert result.role == "peminjam"

    def test_full_auth_flow_pengguna(self):
        """Test complete auth flow for pengguna"""
        from auth.users import get_user_by_username
        user = get_user_by_username("pengguna1")
        token = create_access_token(str(user.user_id), user.role)
        
        # Get current user
        current_user = get_current_active_user(token)
        assert current_user.username == "pengguna1"
        
        # Check role requirement
        checker = require_role("pengguna")
        result = checker(current_user)
        assert result.role == "pengguna"

    def test_allow_roles_accepts_both_roles(self):
        """Test that allow_roles works for multiple users"""
        from auth.users import get_user_by_username
        
        # Test with peminjam
        user1 = get_user_by_username("peminjam1")
        token1 = create_access_token(str(user1.user_id), user1.role)
        current_user1 = get_current_active_user(token1)
        
        checker = allow_roles("peminjam", "pengguna")
        result1 = checker(current_user1)
        assert result1.role == "peminjam"
        
        # Test with pengguna
        user2 = get_user_by_username("pengguna1")
        token2 = create_access_token(str(user2.user_id), user2.role)
        current_user2 = get_current_active_user(token2)
        
        result2 = checker(current_user2)
        assert result2.role == "pengguna"